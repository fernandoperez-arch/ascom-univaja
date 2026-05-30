"""
MONITOR UNIVAJA — Plataforma de notícias e tendências
Coleta automatizada de notícias (RSS) + monitor de trends para a ASCOM UNIVAJA.
Fontes RSS e temas/palavras-chave totalmente customizáveis.
Identidade visual: Manual de Marca UNIVAJA (grafismos dos povos do Vale do Javari).
"""

import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus
import re
import json

from univaja_brand import (
    css_global, header, divisor, section_title,
    PRIMARIA, VERDE_PRETO, VERDE, CINZA,
)

st.set_page_config(
    page_title="Monitor UNIVAJA — Notícias & Trends",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(css_global(), unsafe_allow_html=True)
st.markdown(
    header(
        "MONITOR UNIVAJA",
        "Notícias & tendências · ASCOM",
        "Atualizado em tempo real · 2026",
    ),
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  DEFAULTS (customizáveis na aba ⚙️ Configurações)
# ══════════════════════════════════════════════════════════════════════════════
FONTES_DEFAULT = {
    "Amazônia Real": "https://amazoniareal.com.br/feed/",
    "ISA — Socioambiental": "https://www.socioambiental.org/noticias-socioambientais/feed",
    "CIMI": "https://cimi.org.br/feed/",
    "APIB": "https://apiboficial.org/feed/",
    "Sumaúma": "https://sumauma.com/feed/",
    "Mongabay Brasil": "https://brasil.mongabay.com/feed/",
    "Brasil de Fato": "https://www.brasildefato.com.br/rss2.xml",
    "G1 Amazonas": "https://g1.globo.com/rss/g1/am/amazonas/",
    "Agência Pública": "https://apublica.org/feed/",
    "Repórter Brasil": "https://reporterbrasil.org.br/feed/",
    "Google Notícias — Vale do Javari": "https://news.google.com/rss/search?q=%22Vale+do+Javari%22&hl=pt-BR&gl=BR&ceid=BR:pt-BR",
    "Google Notícias — UNIVAJA": "https://news.google.com/rss/search?q=UNIVAJA&hl=pt-BR&gl=BR&ceid=BR:pt-BR",
    "Google Notícias — Povos isolados": "https://news.google.com/rss/search?q=%22povos+isolados%22+Amaz%C3%B4nia&hl=pt-BR&gl=BR&ceid=BR:pt-BR",
}

TEMAS_DEFAULT = {
    "🎯 Vale do Javari (prioritário)": [
        "vale do javari", "javari", "atalaia do norte", "univaja", "vale javari"
    ],
    "👤 Povos isolados": [
        "povos isolados", "isolados", "contato", "indígenas isolados", "funai isolados"
    ],
    "⛏️ Garimpo e invasão": [
        "garimpo", "invasão", "invasor", "mineração ilegal", "madeireira", "pesca ilegal"
    ],
    "📜 Direitos indígenas": [
        "marco temporal", "demarcação", "direitos indígenas", "constituição", "stf indígena"
    ],
    "🏛️ FUNAI e políticas": [
        "funai", "ministério dos povos", "sonia guajajara", "política indigenista"
    ],
    "🚨 Violência e ameaças": [
        "assassinato", "violência", "ameaça", "conflito", "morte indígena"
    ],
    "💛 Bruno e Dom": [
        "bruno pereira", "dom phillips", "bruno e dom"
    ],
    "🌳 Meio ambiente": [
        "desmatamento", "amazônia", "floresta", "biodiversidade", "clima"
    ],
    "🏥 Saúde indígena": [
        "sesai", "saúde indígena", "dsei", "malária aldeia"
    ],
    "📚 Educação indígena": [
        "educação indígena", "escola indígena", "educação bilíngue"
    ],
    "🌍 Internacional / COP": [
        "cop", "clima global", "biodiversidade global", "amazon week"
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
#  ESTADO
# ══════════════════════════════════════════════════════════════════════════════
if "monitor_config" not in st.session_state:
    st.session_state.monitor_config = {
        "fontes": dict(FONTES_DEFAULT),
        "temas": {k: list(v) for k, v in TEMAS_DEFAULT.items()},
    }
if "salvas" not in st.session_state:
    st.session_state.salvas = {}
if "fontes_ativas" not in st.session_state:
    st.session_state.fontes_ativas = list(st.session_state.monitor_config["fontes"].keys())

mcfg = st.session_state.monitor_config


# ─── Funções ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=900)
def carregar_feed(nome_fonte, url):
    try:
        feed = feedparser.parse(url)
        entradas = []
        for e in feed.entries[:40]:
            titulo = getattr(e, "title", "").strip()
            link = getattr(e, "link", "")
            resumo = re.sub(r"<[^>]+>", "", getattr(e, "summary", "") or "").strip()
            if len(resumo) > 280:
                resumo = resumo[:280].rsplit(" ", 1)[0] + "…"
            data = None
            for attr in ("published_parsed", "updated_parsed"):
                t = getattr(e, attr, None)
                if t:
                    try:
                        data = datetime(*t[:6], tzinfo=timezone.utc); break
                    except Exception: pass
            entradas.append({"fonte": nome_fonte, "titulo": titulo, "link": link,
                             "resumo": resumo, "data": data})
        return entradas
    except Exception as ex:
        return [{"_erro": str(ex), "fonte": nome_fonte}]

def carregar_todas(fontes_selecionadas):
    todas, erros = [], []
    for nome in fontes_selecionadas:
        url = mcfg["fontes"].get(nome)
        if not url: continue
        for it in carregar_feed(nome, url):
            if "_erro" in it: erros.append((it["fonte"], it["_erro"]))
            else: todas.append(it)
    todas.sort(key=lambda x: x["data"] or datetime(1970,1,1, tzinfo=timezone.utc), reverse=True)
    return todas, erros

def filtrar_por_palavras(itens, palavras):
    if not palavras: return itens
    p_lower = [p.lower() for p in palavras]
    return [it for it in itens if any(p in (it["titulo"]+" "+it["resumo"]).lower() for p in p_lower)]

def filtrar_por_data(itens, dias):
    if dias is None: return itens
    corte = datetime.now(timezone.utc) - timedelta(days=dias)
    return [it for it in itens if it["data"] and it["data"] >= corte]

def fmt_data(d):
    if not d: return "sem data"
    delta = datetime.now(timezone.utc) - d
    if delta.days >= 1: return f"há {delta.days} dia{'s' if delta.days > 1 else ''}"
    h = delta.seconds // 3600
    if h >= 1: return f"há {h} hora{'s' if h > 1 else ''}"
    m = max(1, delta.seconds // 60)
    return f"há {m} min"

def identificar_tags(item):
    tags = []
    texto = (item["titulo"] + " " + item["resumo"]).lower()
    for tema, palavras in mcfg["temas"].items():
        if any(p.lower() in texto for p in palavras):
            tags.append(tema)
    return tags


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filtros")

    periodo_label = st.selectbox("Período",
        ["Últimas 24h", "Últimos 3 dias", "Última semana", "Últimas 2 semanas", "Sem filtro"],
        index=2)
    periodo_map = {"Últimas 24h": 1, "Últimos 3 dias": 3, "Última semana": 7,
                   "Últimas 2 semanas": 14, "Sem filtro": None}
    dias = periodo_map[periodo_label]

    st.markdown("**Temas de interesse**")
    temas_sel = []
    for tema in mcfg["temas"].keys():
        if st.checkbox(tema, value=("Vale do Javari" in tema), key=f"t_{tema}"):
            temas_sel.append(tema)

    palavras_extra_raw = st.text_input("Palavras extras (separadas por vírgula)",
        placeholder="ex: marubo, kanamari, korubo")
    palavras_extra = [p.strip() for p in palavras_extra_raw.split(",") if p.strip()]

    st.markdown("---")
    st.markdown("**Fontes ativas**")
    fontes_ativas = []
    for nome in mcfg["fontes"].keys():
        ativo = nome in st.session_state.fontes_ativas
        if st.checkbox(nome, value=ativo, key=f"f_{nome}"):
            fontes_ativas.append(nome)
    st.session_state.fontes_ativas = fontes_ativas

    st.markdown("---")
    if st.button("🔄 Atualizar agora", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    st.caption("Cache de 15 min.")

    st.markdown("---")
    st.markdown("### 💾 Backup config")
    cfg_export = json.dumps(mcfg, ensure_ascii=False, indent=2)
    st.download_button("📥 Baixar config", cfg_export,
        file_name=f"monitor_config_{datetime.now().date().isoformat()}.json",
        mime="application/json", use_container_width=True)

    arq = st.file_uploader("📤 Importar config", type=["json"], label_visibility="collapsed")
    if arq is not None:
        try:
            data = json.loads(arq.read())
            if isinstance(data, dict) and "fontes" in data and "temas" in data:
                if st.button("Confirmar importação", type="primary"):
                    st.session_state.monitor_config = data
                    st.session_state.fontes_ativas = list(data["fontes"].keys())
                    st.success("✅ Configuração importada!")
                    st.rerun()
            else:
                st.error("JSON inválido — precisa ter chaves 'fontes' e 'temas'.")
        except Exception as ex:
            st.error(f"Erro: {ex}")


palavras_filtro = []
for tema in temas_sel:
    palavras_filtro.extend(mcfg["temas"].get(tema, []))
palavras_filtro.extend(palavras_extra)


# ══════════════════════════════════════════════════════════════════════════════
#  ABAS — Como usar PRIMEIRO
# ══════════════════════════════════════════════════════════════════════════════
aba_h, aba_n, aba_t, aba_s, aba_e, aba_cfg = st.tabs([
    "ℹ️ Como usar",
    "📰 Notícias",
    "📈 Trends",
    "⭐ Salvas para reunião",
    "📤 Exportar",
    "⚙️ Configurações",
])

# ──────────────────────────────────────────────────────────────────────────────
#  ABA — COMO USAR
# ──────────────────────────────────────────────────────────────────────────────
with aba_h:
    st.markdown(section_title("Como usar o Monitor", "padrao"), unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown(f"""
        ### 🎯 Para que serve
        O **Monitor UNIVAJA** coleta automaticamente notícias de **mídia indígena, ambiental
        e geral**, filtra pelos temas de interesse da UNIVAJA e ajuda os comunicadores a
        preparar pautas para a reunião de segunda.

        ### 📋 Fluxo recomendado

        <div class="card card-vermelho">
            <strong style="color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">1. Domingo / Segunda cedo</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Comunicador da semana abre a aba <strong>📰 Notícias</strong>, marca os temas de interesse
            na sidebar, define o período e percorre as matérias mais relevantes.
            Salva 5–10 com a estrelinha ☆.
            </p>
        </div>

        <div class="card card-verde">
            <strong style="color:{VERDE};text-transform:uppercase;letter-spacing:0.5px">2. Reunião de segunda</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Vai em <strong>⭐ Salvas</strong>, mostra na tela e propõe as pautas. Em
            <strong>📤 Exportar</strong>, baixa o documento em TXT ou Markdown e cola no grupo ASCOM.
            </p>
        </div>

        <div class="card card-azul">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">3. Durante a produção</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Use a aba <strong>📈 Trends</strong> para entender o que está em alta no Brasil e
            justificar a escolha de pauta. Use as notícias salvas para embasar cards e roteiros.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 💡 Dicas")
        dicas = [
            ("⚙️ Tudo é customizável",
             "Na aba <strong>⚙️ Configurações</strong> você adiciona/remove fontes RSS e temas com suas próprias palavras-chave."),
            ("🔄 Cache de 15 min",
             "As notícias ficam em cache por 15 minutos para o app ser rápido. Use <strong>🔄 Atualizar agora</strong> na sidebar se precisar forçar."),
            ("⭐ Salvar é só para você",
             "As estrelinhas são guardadas no seu navegador. Para compartilhar, use <strong>📤 Exportar</strong>."),
            ("🎯 Tag prioritária",
             "Quando uma notícia toca em <strong>Vale do Javari</strong>, a tag aparece em vermelho — atenção máxima."),
            ("➕ Palavras extras",
             "Use o campo na sidebar para refinar a busca com termos pontuais (ex: nome de uma liderança, lugar específico)."),
        ]
        for titulo, desc in dicas:
            st.markdown(f"""
            <div class="card-grafismo" style="margin-bottom:10px">
                <div class="card-grafismo-conteudo">
                    <strong style="font-size:13px;color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">{titulo}</strong>
                    <p style="font-size:12px;margin-top:6px;line-height:1.5;color:{CINZA}">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(divisor("marubo"), unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — NOTÍCIAS
# ──────────────────────────────────────────────────────────────────────────────
with aba_n:
    st.markdown(section_title("Últimas notícias coletadas", "padrao"), unsafe_allow_html=True)

    if not fontes_ativas:
        st.markdown("""
        <div class="alerta alerta-vermelho">
            ⚠️ Nenhuma fonte selecionada. Marque ao menos uma na barra lateral.
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner(f"Coletando notícias de {len(fontes_ativas)} fontes…"):
            itens, erros = carregar_todas(fontes_ativas)

        itens_periodo = filtrar_por_data(itens, dias)
        itens_filtrados = filtrar_por_palavras(itens_periodo, palavras_filtro)

        col1, col2, col3, col4 = st.columns(4)
        for col, val, label in [
            (col1, len(itens), "Total coletado"),
            (col2, len(itens_periodo), "No período"),
            (col3, len(itens_filtrados), "Após filtros"),
            (col4, len(st.session_state.salvas), "Salvas"),
        ]:
            with col:
                st.markdown(f"""<div class="stat-card"><div class="stat-num">{val}</div>
                    <div class="stat-label">{label}</div></div>""", unsafe_allow_html=True)

        st.markdown(divisor("marubo"), unsafe_allow_html=True)

        if erros:
            with st.expander(f"⚠️ {len(erros)} fonte(s) com erro"):
                for fonte, msg in erros:
                    st.markdown(f"- **{fonte}**: `{msg[:120]}`")

        if not itens_filtrados:
            st.markdown("""
            <div class="alerta">
                📭 Nenhuma notícia corresponde aos filtros atuais.
                Amplie o período, marque mais temas ou adicione palavras-chave.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"### 📰 {len(itens_filtrados)} notícias encontradas")
            st.caption(f"Ordenadas por data · período: {periodo_label.lower()}")

            por_pagina = 20
            total_paginas = max(1, (len(itens_filtrados) + por_pagina - 1) // por_pagina)
            pagina = st.selectbox("Página", list(range(1, total_paginas + 1)), key="pag_n") if total_paginas > 1 else 1
            ini = (pagina - 1) * por_pagina
            fim = ini + por_pagina

            for it in itens_filtrados[ini:fim]:
                tags = identificar_tags(it)
                tags_html = ""
                for tag in tags[:3]:
                    cls = "news-tag news-tag-prio" if "Vale do Javari" in tag else "news-tag"
                    tags_html += f'<span class="{cls}">{tag}</span>'

                card_id = it["link"]
                salva = card_id in st.session_state.salvas

                col_card, col_btn = st.columns([10, 1])
                with col_card:
                    st.markdown(f"""
                    <div class="news-card">
                        <a class="news-titulo" href="{it['link']}" target="_blank">{it['titulo']}</a>
                        <div class="news-resumo">{it['resumo'] or '<em>sem resumo</em>'}</div>
                        <div class="news-meta">
                            <span class="news-fonte">{it['fonte']}</span>
                            <span>🕐 {fmt_data(it['data'])}</span>
                            {tags_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    label = "★" if salva else "☆"
                    if st.button(label, key=f"star_{hash(card_id)}", help="Salvar para reunião"):
                        if salva: st.session_state.salvas.pop(card_id, None)
                        else: st.session_state.salvas[card_id] = it
                        st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — TRENDS
# ──────────────────────────────────────────────────────────────────────────────
with aba_t:
    st.markdown(section_title("O que está em alta no Brasil", "verde"), unsafe_allow_html=True)
    st.caption("Use o Google Trends para priorizar pautas em alta.")

    termos_trends = []
    for tema in temas_sel:
        palavras = mcfg["temas"].get(tema, [])
        if palavras:
            termos_trends.append(palavras[0])
    termos_trends.extend(palavras_extra)
    termos_trends = list(dict.fromkeys(termos_trends))[:5]

    if not termos_trends:
        termos_trends = ["Vale do Javari", "povos indígenas", "UNIVAJA"]
        st.markdown("""
        <div class="alerta">
            💡 Nenhum tema selecionado. Usando padrão: <strong>Vale do Javari, povos indígenas, UNIVAJA</strong>.
        </div>
        """, unsafe_allow_html=True)

    pills = " ".join([f'<span class="termo-pill">{t}</span>' for t in termos_trends])
    st.markdown(f"<div style='margin:10px 0'><strong style='color:{VERDE_PRETO}'>Termos no comparativo:</strong><br>{pills}</div>",
                unsafe_allow_html=True)

    periodo_trends_map = {
        "Últimas 24h": "now 1-d", "Últimos 3 dias": "now 7-d",
        "Última semana": "now 7-d", "Últimas 2 semanas": "today 1-m", "Sem filtro": "today 12-m",
    }
    periodo_tr = periodo_trends_map.get(periodo_label, "today 1-m")

    q_trends = ",".join(termos_trends)
    url_compare = f"https://trends.google.com/trends/explore?q={quote_plus(q_trends)}&geo=BR&date={quote_plus(periodo_tr)}&hl=pt-BR"
    url_explore = f"https://trends.google.com/trends/explore?q={quote_plus(termos_trends[0])}&geo=BR&hl=pt-BR"
    url_diaria  = "https://trends.google.com/trends/trendingsearches/daily?geo=BR&hl=pt-BR"
    url_realtime= "https://trends.google.com/trends/trendingsearches/realtime?geo=BR&category=all&hl=pt-BR"

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <a href="{url_compare}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">📊 Comparativo entre termos →</div>
            <div class="link-busca-desc">Veja qual dos termos selecionados teve mais buscas no Brasil no período.</div>
        </a>
        <a href="{url_explore}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">🔬 Explorar "{termos_trends[0]}" →</div>
            <div class="link-busca-desc">Análise profunda do primeiro termo: regiões, buscas relacionadas e evolução.</div>
        </a>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <a href="{url_diaria}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">🔥 Tendências do dia (Brasil) →</div>
            <div class="link-busca-desc">Top buscas do dia no Brasil. Útil para identificar oportunidades de pauta.</div>
        </a>
        <a href="{url_realtime}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">⚡ Em tempo real (Brasil) →</div>
            <div class="link-busca-desc">Histórias em ascensão agora — bom para reações rápidas a fatos recentes.</div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown(section_title("Buscas em portais de notícia", "vermelho"), unsafe_allow_html=True)

    q_news = " OR ".join([f'"{t}"' for t in termos_trends[:3]])
    qdr_map = {"Últimas 24h": "d", "Últimos 3 dias": "w", "Última semana": "w",
               "Últimas 2 semanas": "m", "Sem filtro": "y"}
    qdr = qdr_map.get(periodo_label, "w")
    url_gnews = f"https://news.google.com/search?q={quote_plus(q_news)}&hl=pt-BR&gl=BR&ceid=BR:pt-BR&as_qdr={qdr}"
    url_gsearch = f"https://www.google.com/search?q={quote_plus(q_news)}&tbm=nws&hl=pt-BR&tbs=qdr:{qdr}"

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown(f"""
        <a href="{url_gnews}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">📰 Google Notícias →</div>
            <div class="link-busca-desc">Manchetes recentes com os termos selecionados.</div>
        </a>
        """, unsafe_allow_html=True)
    with col_d:
        st.markdown(f"""
        <a href="{url_gsearch}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">🔎 Google Search News →</div>
            <div class="link-busca-desc">Busca filtrada por período. Complementa o Google Notícias.</div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown(divisor("pontos"), unsafe_allow_html=True)
    st.markdown("""
    <div class="alerta alerta-azul">
        💡 <strong>Como usar na reunião de segunda:</strong> abra os 4 links acima, anote 3–5 temas que aparecem
        com força e leve como sugestão de pauta com justificativa ("tema X subiu Y% esta semana").
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — SALVAS
# ──────────────────────────────────────────────────────────────────────────────
with aba_s:
    st.markdown(section_title("Notícias salvas para a reunião", "vermelho"), unsafe_allow_html=True)
    st.caption("Itens marcados com ☆ na aba Notícias.")

    if not st.session_state.salvas:
        st.markdown("""
        <div class="alerta">
            📌 Nenhuma notícia salva ainda. Vá em <strong>📰 Notícias</strong> e clique em ☆.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"**{len(st.session_state.salvas)} notícia(s) salva(s)**")
        if st.button("🗑️ Limpar todas", type="secondary"):
            st.session_state.salvas = {}; st.rerun()

        for link, it in list(st.session_state.salvas.items()):
            st.markdown(f"""
            <div class="salva-card">
                <a class="news-titulo" href="{it['link']}" target="_blank">{it['titulo']}</a>
                <div class="news-resumo">{it['resumo'] or '<em>sem resumo</em>'}</div>
                <div class="news-meta">
                    <span class="news-fonte">{it['fonte']}</span>
                    <span>🕐 {fmt_data(it['data'])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"❌ Remover", key=f"rem_{hash(link)}"):
                st.session_state.salvas.pop(link, None); st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — EXPORTAR
# ──────────────────────────────────────────────────────────────────────────────
with aba_e:
    st.markdown(section_title("Exportar pauta para a reunião", "padrao"), unsafe_allow_html=True)

    if not st.session_state.salvas:
        st.markdown("""
        <div class="alerta">
            ⚠️ Nenhuma notícia salva. Salve ao menos uma para gerar o relatório.
        </div>
        """, unsafe_allow_html=True)
    else:
        hoje = datetime.now().strftime("%d/%m/%Y")
        linhas = [
            "📋 PAUTAS SUGERIDAS — UNIVAJA ASCOM",
            f"Reunião de segunda · {hoje}",
            f"Total de matérias: {len(st.session_state.salvas)}",
            "",
        ]
        for i, (link, it) in enumerate(st.session_state.salvas.items(), 1):
            linhas.append(f"{i}. {it['titulo']}")
            linhas.append(f"   Fonte: {it['fonte']} · {fmt_data(it['data'])}")
            if it["resumo"]: linhas.append(f"   Resumo: {it['resumo']}")
            linhas.append(f"   Link: {it['link']}"); linhas.append("")
        texto = "\n".join(linhas)

        md_linhas = [
            "# 📋 Pautas sugeridas — UNIVAJA ASCOM",
            f"**Reunião de segunda · {hoje}**  ",
            f"_{len(st.session_state.salvas)} matérias_", "", "---",
        ]
        for i, (link, it) in enumerate(st.session_state.salvas.items(), 1):
            md_linhas.append(f"## {i}. [{it['titulo']}]({it['link']})")
            md_linhas.append(f"**{it['fonte']}** · _{fmt_data(it['data'])}_  ")
            if it["resumo"]: md_linhas.append(f"> {it['resumo']}")
            md_linhas.append("")
        md = "\n".join(md_linhas)

        export_json = json.dumps(
            [{"fonte": it["fonte"], "titulo": it["titulo"], "link": it["link"],
              "resumo": it["resumo"], "data": it["data"].isoformat() if it["data"] else None}
             for it in st.session_state.salvas.values()],
            ensure_ascii=False, indent=2,
        )

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button("📄 Baixar TXT", texto,
                file_name=f"pautas_univaja_{hoje.replace('/','-')}.txt",
                mime="text/plain", use_container_width=True)
        with col_d2:
            st.download_button("📝 Baixar Markdown", md,
                file_name=f"pautas_univaja_{hoje.replace('/','-')}.md",
                mime="text/markdown", use_container_width=True)
        with col_d3:
            st.download_button("🗂️ Baixar JSON", export_json,
                file_name=f"pautas_univaja_{hoje.replace('/','-')}.json",
                mime="application/json", use_container_width=True)

        st.markdown("#### 👁️ Pré-visualização")
        st.text_area("", texto, height=400, label_visibility="collapsed")


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — CONFIGURAÇÕES
# ──────────────────────────────────────────────────────────────────────────────
with aba_cfg:
    st.markdown(section_title("Configurações do Monitor", "padrao"), unsafe_allow_html=True)
    st.caption("Tudo é customizável. Adicione/remova fontes RSS e temas com suas próprias palavras-chave.")

    st.markdown(f"""
    <div class="alerta alerta-azul">
        💡 <strong>Atenção:</strong> as mudanças valem para a sessão atual. Baixe o JSON na sidebar
        para preservar suas configurações entre acessos.
    </div>
    """, unsafe_allow_html=True)

    # FONTES RSS
    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown("### 📡 Fontes RSS")
    st.caption("Cada linha: NOME | URL — separados pelo caractere `|`.")

    fontes_txt_default = "\n".join([f"{nome} | {url}" for nome, url in mcfg["fontes"].items()])
    fontes_txt = st.text_area("Fontes (NOME | URL por linha)",
        value=fontes_txt_default, height=320, label_visibility="collapsed", key="cfg_fontes")

    with st.expander("➕ Adicionar uma nova fonte rapidamente"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            novo_nome = st.text_input("Nome da fonte", placeholder="ex: Folha de SP")
        with col_f2:
            novo_url = st.text_input("URL do feed RSS",
                placeholder="ex: https://feeds.folha.uol.com.br/poder/rss091.xml")
        if st.button("Adicionar fonte", use_container_width=True):
            if novo_nome and novo_url:
                mcfg["fontes"][novo_nome.strip()] = novo_url.strip()
                if novo_nome.strip() not in st.session_state.fontes_ativas:
                    st.session_state.fontes_ativas.append(novo_nome.strip())
                st.success(f"✅ Fonte '{novo_nome}' adicionada!")
                st.rerun()

    # TEMAS
    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown("### 🎯 Temas e palavras-chave")
    st.caption("Para cada tema, defina as palavras-chave que disparam o reconhecimento. Use o formato `TEMA: palavra1, palavra2, palavra3`.")

    temas_txt_default = "\n".join([
        f"{tema}: {', '.join(palavras)}" for tema, palavras in mcfg["temas"].items()
    ])
    temas_txt = st.text_area("Temas (TEMA: palavra1, palavra2 por linha)",
        value=temas_txt_default, height=380, label_visibility="collapsed", key="cfg_temas")

    with st.expander("➕ Adicionar um novo tema rapidamente"):
        novo_tema = st.text_input("Nome do tema (com emoji opcional)",
            placeholder="ex: 🏞️ Áreas protegidas")
        novas_palavras = st.text_input("Palavras-chave (separadas por vírgula)",
            placeholder="ex: unidade de conservação, reserva extrativista")
        if st.button("Adicionar tema", use_container_width=True):
            if novo_tema and novas_palavras:
                mcfg["temas"][novo_tema.strip()] = [p.strip() for p in novas_palavras.split(",") if p.strip()]
                st.success(f"✅ Tema '{novo_tema}' adicionado!")
                st.rerun()

    st.markdown(divisor("pontos"), unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        if st.button("💾 Salvar todas as configurações", type="primary", use_container_width=True):
            # Parsear fontes
            novas_fontes = {}
            for linha in fontes_txt.split("\n"):
                if "|" in linha:
                    nome, url = linha.split("|", 1)
                    nome, url = nome.strip(), url.strip()
                    if nome and url:
                        novas_fontes[nome] = url
            # Parsear temas
            novos_temas = {}
            for linha in temas_txt.split("\n"):
                if ":" in linha:
                    tema, palavras = linha.split(":", 1)
                    tema = tema.strip()
                    pal_list = [p.strip() for p in palavras.split(",") if p.strip()]
                    if tema and pal_list:
                        novos_temas[tema] = pal_list

            mcfg["fontes"] = novas_fontes
            mcfg["temas"] = novos_temas
            # Atualiza fontes ativas
            st.session_state.fontes_ativas = [n for n in st.session_state.fontes_ativas if n in novas_fontes]
            for n in novas_fontes:
                if n not in st.session_state.fontes_ativas:
                    st.session_state.fontes_ativas.append(n)
            st.cache_data.clear()
            st.success("✅ Configurações salvas! Baixe o JSON na sidebar para preservar.")
            st.rerun()

    with col_s2:
        if st.button("↺ Resetar aos padrões", use_container_width=True):
            st.session_state.monitor_config = {
                "fontes": dict(FONTES_DEFAULT),
                "temas": {k: list(v) for k, v in TEMAS_DEFAULT.items()},
            }
            st.session_state.fontes_ativas = list(FONTES_DEFAULT.keys())
            st.cache_data.clear()
            st.rerun()

    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.caption("Monitor UNIVAJA · ASCOM · 2026 — uso interno · Identidade visual baseada no Manual de Marca UNIVAJA")
