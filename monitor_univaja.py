"""
MONITOR UNIVAJA — Plataforma de notícias e tendências
Coleta automatizada de notícias (RSS) + monitor de trends para a ASCOM UNIVAJA.
Publicação: Streamlit Community Cloud.
"""

import streamlit as st
import feedparser
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus
import re
import json
import io

# ─── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Monitor UNIVAJA — Notícias & Trends",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');
html, body, [class*="css"] { font-family: 'Archivo', 'Segoe UI', Arial, sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.header-univaja {
    background: linear-gradient(135deg, #DC3637 0%, #780B0B 100%);
    color: white;
    padding: 20px 26px;
    border-radius: 12px;
    margin-bottom: 18px;
    display: flex; justify-content: space-between; align-items: center;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px; border-bottom: 2px solid #DC3637; padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: #f5f5f5; border-radius: 8px 8px 0 0;
    padding: 8px 18px; font-weight: 500; font-size: 14px; color: #494949;
    border: 1px solid #ddd; border-bottom: none;
}
.stTabs [aria-selected="true"] {
    background: #DC3637 !important; color: white !important; border-color: #DC3637 !important;
}

/* Card de notícia */
.news-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-left: 5px solid #DC3637;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    transition: box-shadow .15s, transform .1s;
}
.news-card:hover { box-shadow: 0 4px 14px rgba(220,54,55,.12); }
.news-titulo {
    font-size: 15px; font-weight: 700; color: #222221; line-height: 1.4;
    text-decoration: none; display: block; margin-bottom: 6px;
}
.news-titulo:hover { color: #DC3637; }
.news-resumo { font-size: 13px; color: #494949; line-height: 1.55; margin-bottom: 8px; }
.news-meta {
    display: flex; gap: 12px; flex-wrap: wrap;
    font-size: 11px; color: #6b7280; align-items: center;
}
.news-fonte {
    background: #DC3637; color: white; padding: 2px 9px; border-radius: 10px;
    font-weight: 600; font-size: 11px;
}
.news-tag {
    background: #f0f5f1; color: #384E3A; padding: 2px 8px; border-radius: 10px;
    font-size: 11px; font-weight: 500; border: 1px solid #99E19E;
}
.news-tag-prio {
    background: #fce8e8; color: #780B0B; border-color: #E58D8D;
}

/* Stats */
.stat-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
}
.stat-num { font-size: 28px; font-weight: 700; color: #DC3637; line-height: 1; }
.stat-label { font-size: 12px; color: #6b7280; margin-top: 6px; text-transform: uppercase; letter-spacing: .5px; }

/* Alerts */
.alerta {
    background: #fdf6e3; border: 1px solid #B6352E; border-left: 5px solid #B6352E;
    border-radius: 8px; padding: 12px 16px; font-size: 13px; color: #780B0B; margin: 12px 0;
}
.alerta-verde { background: #f0f5f1; border-color: #547658; border-left-color: #547658; color: #1F2A21; }
.alerta-azul  { background: #f0f5f1; border-color: #384E3A; border-left-color: #384E3A; color: #1F2A21; }

/* Link buscas */
.link-busca {
    display: block; background: white; border: 1px solid #e0e0e0; border-radius: 8px;
    padding: 12px 16px; text-decoration: none; color: #222221; margin-bottom: 8px;
    transition: border-color .15s;
}
.link-busca:hover { border-color: #DC3637; }
.link-busca-titulo { font-weight: 600; font-size: 14px; color: #DC3637; }
.link-busca-desc { font-size: 12px; color: #6b7280; margin-top: 3px; }

/* Salvas */
.salva-card {
    background: #fdf2f2; border: 1px solid #E58D8D; border-left: 5px solid #B6352E;
    border-radius: 10px; padding: 12px 16px; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-univaja">
    <div>
        <div style="font-size:22px;font-weight:700;letter-spacing:1px">🌿 MONITOR UNIVAJA</div>
        <div style="font-size:13px;opacity:.9;margin-top:2px">Notícias & tendências para a ASCOM</div>
    </div>
    <div style="font-size:12px;opacity:.85;text-align:right">
        Atualizado em tempo real<br>Uso interno · 2026
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  FONTES DE NOTÍCIAS (RSS)
# ══════════════════════════════════════════════════════════════════════════════
FONTES = {
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

# ─── Palavras-chave por tema (filtros) ───────────────────────────────────────
TEMAS_PALAVRAS = {
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

# ─── Funções ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=900)  # 15 minutos
def carregar_feed(nome_fonte, url):
    """Baixa um RSS e devolve entradas normalizadas."""
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
                        data = datetime(*t[:6], tzinfo=timezone.utc)
                        break
                    except Exception:
                        pass
            entradas.append({
                "fonte": nome_fonte,
                "titulo": titulo,
                "link": link,
                "resumo": resumo,
                "data": data,
            })
        return entradas
    except Exception as ex:
        return [{"_erro": str(ex), "fonte": nome_fonte}]

def carregar_todas(fontes_selecionadas):
    todas = []
    erros = []
    for nome in fontes_selecionadas:
        url = FONTES[nome]
        itens = carregar_feed(nome, url)
        for it in itens:
            if "_erro" in it:
                erros.append((it["fonte"], it["_erro"]))
            else:
                todas.append(it)
    # ordena por data (mais recentes primeiro); itens sem data vão pro fim
    todas.sort(key=lambda x: x["data"] or datetime(1970,1,1, tzinfo=timezone.utc), reverse=True)
    return todas, erros

def filtrar_por_palavras(itens, palavras):
    """Retorna itens que contêm pelo menos uma das palavras (no título ou resumo)."""
    if not palavras:
        return itens
    palavras_lower = [p.lower() for p in palavras]
    out = []
    for it in itens:
        texto = (it["titulo"] + " " + it["resumo"]).lower()
        if any(p in texto for p in palavras_lower):
            out.append(it)
    return out

def filtrar_por_data(itens, dias):
    if dias is None:
        return itens
    corte = datetime.now(timezone.utc) - timedelta(days=dias)
    return [it for it in itens if it["data"] and it["data"] >= corte]

def fmt_data(d):
    if not d:
        return "sem data"
    agora = datetime.now(timezone.utc)
    delta = agora - d
    if delta.days >= 1:
        return f"há {delta.days} dia{'s' if delta.days > 1 else ''}"
    h = delta.seconds // 3600
    if h >= 1:
        return f"há {h} hora{'s' if h > 1 else ''}"
    m = max(1, delta.seconds // 60)
    return f"há {m} min"

def identificar_tags(item):
    """Identifica quais temas o item toca."""
    tags = []
    texto = (item["titulo"] + " " + item["resumo"]).lower()
    for tema, palavras in TEMAS_PALAVRAS.items():
        if any(p in texto for p in palavras):
            tags.append(tema)
    return tags

# ─── Estado de sessão ────────────────────────────────────────────────────────
if "salvas" not in st.session_state:
    st.session_state.salvas = {}  # link → item
if "fontes_ativas" not in st.session_state:
    st.session_state.fontes_ativas = list(FONTES.keys())

# ─── Sidebar — filtros ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filtros")

    periodo_label = st.selectbox(
        "Período",
        ["Últimas 24h", "Últimos 3 dias", "Última semana", "Últimas 2 semanas", "Sem filtro"],
        index=2,
    )
    periodo_map = {
        "Últimas 24h": 1, "Últimos 3 dias": 3, "Última semana": 7,
        "Últimas 2 semanas": 14, "Sem filtro": None,
    }
    dias = periodo_map[periodo_label]

    st.markdown("**Temas de interesse**")
    temas_sel = []
    for tema in TEMAS_PALAVRAS.keys():
        if st.checkbox(tema, value=("Vale do Javari" in tema), key=f"t_{tema}"):
            temas_sel.append(tema)

    palavras_extra_raw = st.text_input(
        "Palavras extras (separadas por vírgula)",
        placeholder="ex: marubo, kanamari, korubo"
    )
    palavras_extra = [p.strip() for p in palavras_extra_raw.split(",") if p.strip()]

    st.markdown("---")
    st.markdown("**Fontes ativas**")
    fontes_ativas = []
    for nome in FONTES.keys():
        if st.checkbox(nome, value=(nome in st.session_state.fontes_ativas), key=f"f_{nome}"):
            fontes_ativas.append(nome)
    st.session_state.fontes_ativas = fontes_ativas

    st.markdown("---")
    if st.button("🔄 Atualizar agora", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("Cache de 15 min. Use o botão para forçar atualização.")

# ─── Reúne palavras-chave selecionadas ───────────────────────────────────────
palavras_filtro = []
for tema in temas_sel:
    palavras_filtro.extend(TEMAS_PALAVRAS[tema])
palavras_filtro.extend(palavras_extra)

# ══════════════════════════════════════════════════════════════════════════════
#  ABAS
# ══════════════════════════════════════════════════════════════════════════════
aba_n, aba_t, aba_s, aba_e, aba_a = st.tabs([
    "📰 Notícias",
    "📈 Trends",
    "⭐ Salvas para reunião",
    "📤 Exportar",
    "ℹ️ Sobre",
])

# ══════════════════════════════════════════════════════════════════════════════
#  ABA — NOTÍCIAS
# ══════════════════════════════════════════════════════════════════════════════
with aba_n:
    if not fontes_ativas:
        st.warning("Nenhuma fonte selecionada. Marque ao menos uma na barra lateral.")
    else:
        with st.spinner(f"Coletando notícias de {len(fontes_ativas)} fontes…"):
            itens, erros = carregar_todas(fontes_ativas)

        # filtros
        itens_periodo = filtrar_por_data(itens, dias)
        itens_filtrados = filtrar_por_palavras(itens_periodo, palavras_filtro)

        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{len(itens)}</div>
                <div class="stat-label">Total coletado</div></div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{len(itens_periodo)}</div>
                <div class="stat-label">No período</div></div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{len(itens_filtrados)}</div>
                <div class="stat-label">Após filtros</div></div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{len(st.session_state.salvas)}</div>
                <div class="stat-label">Salvas</div></div>""", unsafe_allow_html=True)

        if erros:
            with st.expander(f"⚠️ {len(erros)} fonte(s) com erro"):
                for fonte, msg in erros:
                    st.markdown(f"- **{fonte}**: `{msg[:120]}`")

        if not itens_filtrados:
            st.markdown("""
            <div class="alerta">
                📭 Nenhuma notícia corresponde aos filtros atuais.
                Tente ampliar o período, marcar mais temas ou adicionar palavras-chave.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"### 📰 {len(itens_filtrados)} notícias encontradas")
            st.caption(f"Ordenadas por data · período: {periodo_label.lower()}")

            # Paginação simples
            por_pagina = 20
            total_paginas = max(1, (len(itens_filtrados) + por_pagina - 1) // por_pagina)
            if total_paginas > 1:
                pagina = st.selectbox("Página", list(range(1, total_paginas + 1)), key="pag_n")
            else:
                pagina = 1
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
                        if salva:
                            st.session_state.salvas.pop(card_id, None)
                        else:
                            st.session_state.salvas[card_id] = it
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  ABA — TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with aba_t:
    st.markdown("### 📈 O que está em alta no Brasil")
    st.caption("Use o Google Trends para entender qual tema tem mais buscas e priorizar pautas em alta.")

    termos_trends = []
    for tema in temas_sel:
        # pega só o primeiro termo de cada tema para Trends (limite de 5)
        termos_trends.append(TEMAS_PALAVRAS[tema][0])
    termos_trends.extend(palavras_extra)
    termos_trends = list(dict.fromkeys(termos_trends))[:5]

    if not termos_trends:
        termos_trends = ["Vale do Javari", "povos indígenas", "UNIVAJA"]
        st.markdown("""
        <div class="alerta">
            💡 Nenhum tema selecionado. Usando padrão: <strong>Vale do Javari, povos indígenas, UNIVAJA</strong>.
            Marque temas na barra lateral para personalizar.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"**Termos no comparativo:** {', '.join(termos_trends)}")

    periodo_trends_map = {
        "Últimas 24h": "now 1-d",
        "Últimos 3 dias": "now 7-d",
        "Última semana": "now 7-d",
        "Últimas 2 semanas": "today 1-m",
        "Sem filtro": "today 12-m",
    }
    periodo_tr = periodo_trends_map.get(periodo_label, "today 1-m")

    q_trends = ",".join(termos_trends)
    url_compare = f"https://trends.google.com/trends/explore?q={quote_plus(q_trends)}&geo=BR&date={quote_plus(periodo_tr)}&hl=pt-BR"
    url_explore = f"https://trends.google.com/trends/explore?q={quote_plus(termos_trends[0])}&geo=BR&hl=pt-BR"
    url_diaria  = f"https://trends.google.com/trends/trendingsearches/daily?geo=BR&hl=pt-BR"
    url_realtime= f"https://trends.google.com/trends/trendingsearches/realtime?geo=BR&category=all&hl=pt-BR"

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

    st.markdown("---")
    st.markdown("### 🔎 Buscas em portais de notícia")
    q_news = " OR ".join([f'"{t}"' for t in termos_trends[:3]])
    qdr_map = {
        "Últimas 24h": "d", "Últimos 3 dias": "w", "Última semana": "w",
        "Últimas 2 semanas": "m", "Sem filtro": "y",
    }
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

    st.markdown("---")
    st.markdown("""
    <div class="alerta alerta-azul">
        💡 <strong>Como usar na reunião de segunda:</strong> abra os 4 links acima, anote 3–5 temas que aparecem
        com força e leve como sugestão de pauta com justificativa (“tema X subiu Y% esta semana”).
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ABA — SALVAS
# ══════════════════════════════════════════════════════════════════════════════
with aba_s:
    st.markdown("### ⭐ Notícias salvas para a reunião")
    st.caption("Itens marcados com ☆ na aba Notícias. Use para preparar a pauta da reunião de segunda.")

    if not st.session_state.salvas:
        st.markdown("""
        <div class="alerta">
            📌 Nenhuma notícia salva ainda. Vá em <strong>📰 Notícias</strong> e clique em ☆ ao lado das matérias relevantes.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"**{len(st.session_state.salvas)} notícia(s) salva(s)**")

        if st.button("🗑️ Limpar todas", type="secondary"):
            st.session_state.salvas = {}
            st.rerun()

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
                st.session_state.salvas.pop(link, None)
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  ABA — EXPORTAR
# ══════════════════════════════════════════════════════════════════════════════
with aba_e:
    st.markdown("### 📤 Exportar pauta para a reunião")
    st.caption("Gera um documento com as notícias salvas, pronto para colar no grupo ASCOM.")

    if not st.session_state.salvas:
        st.markdown("""
        <div class="alerta">
            ⚠️ Nenhuma notícia salva. Salve ao menos uma para gerar o relatório.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Texto simples
        hoje = datetime.now().strftime("%d/%m/%Y")
        linhas = [
            f"📋 PAUTAS SUGERIDAS — UNIVAJA ASCOM",
            f"Reunião de segunda · {hoje}",
            f"Total de matérias: {len(st.session_state.salvas)}",
            "",
        ]
        for i, (link, it) in enumerate(st.session_state.salvas.items(), 1):
            linhas.append(f"{i}. {it['titulo']}")
            linhas.append(f"   Fonte: {it['fonte']} · {fmt_data(it['data'])}")
            if it["resumo"]:
                linhas.append(f"   Resumo: {it['resumo']}")
            linhas.append(f"   Link: {it['link']}")
            linhas.append("")
        texto = "\n".join(linhas)

        # Markdown
        md_linhas = [
            f"# 📋 Pautas sugeridas — UNIVAJA ASCOM",
            f"**Reunião de segunda · {hoje}**  ",
            f"_{len(st.session_state.salvas)} matérias_",
            "",
            "---",
        ]
        for i, (link, it) in enumerate(st.session_state.salvas.items(), 1):
            md_linhas.append(f"## {i}. [{it['titulo']}]({it['link']})")
            md_linhas.append(f"**{it['fonte']}** · _{fmt_data(it['data'])}_  ")
            if it["resumo"]:
                md_linhas.append(f"> {it['resumo']}")
            md_linhas.append("")
        md = "\n".join(md_linhas)

        # JSON
        export_json = json.dumps(
            [{"fonte": it["fonte"], "titulo": it["titulo"], "link": it["link"],
              "resumo": it["resumo"], "data": it["data"].isoformat() if it["data"] else None}
             for it in st.session_state.salvas.values()],
            ensure_ascii=False, indent=2,
        )

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            st.download_button(
                "📄 Baixar TXT",
                texto, file_name=f"pautas_univaja_{hoje.replace('/','-')}.txt",
                mime="text/plain", use_container_width=True,
            )
        with col_d2:
            st.download_button(
                "📝 Baixar Markdown",
                md, file_name=f"pautas_univaja_{hoje.replace('/','-')}.md",
                mime="text/markdown", use_container_width=True,
            )
        with col_d3:
            st.download_button(
                "🗂️ Baixar JSON",
                export_json, file_name=f"pautas_univaja_{hoje.replace('/','-')}.json",
                mime="application/json", use_container_width=True,
            )

        st.markdown("#### 👁️ Pré-visualização")
        st.text_area("", texto, height=400, label_visibility="collapsed")

# ══════════════════════════════════════════════════════════════════════════════
#  ABA — SOBRE
# ══════════════════════════════════════════════════════════════════════════════
with aba_a:
    st.markdown("### ℹ️ Sobre esta plataforma")
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("""
        **Monitor UNIVAJA** é uma plataforma de coleta automatizada de notícias e tendências
        feita para a ASCOM da UNIVAJA. Ela:

        - 📥 **Coleta automaticamente** notícias de 12+ fontes (mídia indígena, ambiental e geral)
        - 🎯 **Filtra por tema** usando palavras-chave dos temas prioritários da UNIVAJA
        - ⭐ **Permite salvar** matérias relevantes para a pauta da reunião de segunda
        - 📤 **Exporta a pauta** em TXT, Markdown ou JSON
        - 📈 **Conecta com o Google Trends** para entender o que está em alta

        ### ⏰ Quando usar
        - **Domingo / Segunda cedo:** comunicador da semana abre a aba 📰 Notícias,
          filtra pelos temas relevantes, salva 5–10 matérias e exporta para levar à reunião.
        - **Terça e quarta:** durante a produção, usa as notícias salvas para embasar
          cards e roteiros.
        - **Quinzenal:** ponto focal apresenta o consolidado de pautas relevantes
          para a coordenação.

        ### 🔄 Atualização
        O cache é de 15 minutos. Para forçar atualização imediata, use o botão
        **🔄 Atualizar agora** na barra lateral.
        """)
    with col2:
        st.markdown("""
        ### 🚀 Publicação no Streamlit
        1. Suba `monitor_univaja.py` + `requirements.txt` em um repositório GitHub
        2. Em [share.streamlit.io](https://share.streamlit.io), conecte o repositório
        3. Selecione `monitor_univaja.py` como entry point
        4. Clique em Deploy — em 2 minutos está no ar

        ### 📚 Fontes ativas
        """)
        for nome in FONTES.keys():
            st.markdown(f"- {nome}")

        st.markdown("""
        ### ➕ Adicionar fontes
        Edite o dicionário `FONTES` no topo do arquivo `monitor_univaja.py`.
        Use qualquer feed RSS — basta o link.
        """)

    st.markdown("---")
    st.caption("Monitor UNIVAJA · ASCOM · 2026 — uso interno")
