"""
ASCOM UNIVAJA — Plataforma de fluxos integrados de comunicação
Identidade visual: Manual de Marca UNIVAJA (cores + grafismos dos povos do Vale do Javari).
"""

import streamlit as st
from datetime import date, datetime, timedelta
from urllib.parse import quote_plus, quote
import json
import uuid

from univaja_brand import (
    css_global, header, divisor, section_title, flow_kanban, sidebar_logo,
    PRIMARIA, VERMELHO_ESC, VERMELHO_MED, VERMELHO_CLARO,
    VERDE, VERDE_ESC, VERDE_PRETO, VERDE_CLARO,
    CINZA, PRETO, BRANCO, CREME,
)

st.set_page_config(
    page_title="ASCOM UNIVAJA",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(css_global(), unsafe_allow_html=True)
st.markdown(
    header(
        "ASCOM",
        "Assessoria de Comunicação",
        "Uso interno · 2026",
    ),
    unsafe_allow_html=True,
)

# Logo na sidebar
with st.sidebar:
    st.markdown(sidebar_logo(), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CALENDÁRIO DE DATAS FIXAS — pré-populado, totalmente editável
# ══════════════════════════════════════════════════════════════════════════════
DATAS_FIXAS_DEFAULT = [
    {"data": "01-28", "titulo": "Dia do Pajé", "categoria": "Indígena nacional",
     "sugestao": "Card celebrando os pajés do Vale do Javari — guardiões do conhecimento ancestral.",
     "formato": "Card / Carrossel"},
    {"data": "02-07", "titulo": "Dia do Cacique", "categoria": "Indígena nacional",
     "sugestao": "Card homenageando os caciques das aldeias da UNIVAJA. Trazer foto/depoimento de um cacique.",
     "formato": "Card / Vídeo curto"},
    {"data": "03-08", "titulo": "Dia Internacional da Mulher", "categoria": "Mulher indígena",
     "sugestao": "Vídeo / carrossel destacando a força das mulheres indígenas do Vale do Javari nas associações de base.",
     "formato": "Reels / Carrossel"},
    {"data": "04-19", "titulo": "Dia dos Povos Indígenas", "categoria": "Indígena nacional · DATA MAIOR",
     "sugestao": "Campanha completa: card institucional + vídeo com lideranças + boletim para as aldeias. Pauta política sobre demarcação.",
     "formato": "Campanha (card + vídeo + boletim)"},
    {"data": "04-22", "titulo": "Dia da Terra", "categoria": "Meio ambiente",
     "sugestao": "Card conectando a defesa do território indígena à proteção da Amazônia.",
     "formato": "Card / Carrossel"},
    {"data": "04-25", "titulo": "ATL — Acampamento Terra Livre (semana)", "categoria": "Mobilização",
     "sugestao": "Cobertura do ATL em Brasília. Depoimentos das lideranças que participam, registros, denúncias.",
     "formato": "Stories diários + Reels + Cards"},
    {"data": "05-13", "titulo": "Homologação da TI Vale do Javari", "categoria": "UNIVAJA · DATA MAIOR",
     "sugestao": "Memória da conquista: a Terra Indígena foi homologada em 13/05/2001. Vídeo histórico + carrossel com marcos da luta.",
     "formato": "Vídeo + Carrossel"},
    {"data": "06-05", "titulo": "Bruno e Dom (memória) + Dia do Meio Ambiente", "categoria": "Memória · DATA MAIOR",
     "sugestao": "Card sóbrio de memória ativa: 'A UNIVAJA não esquece, não cala, não recua.' Aprovação obrigatória com coordenação + procuradoria.",
     "formato": "Card único nas 3 redes simultaneamente"},
    {"data": "07-26", "titulo": "Dia do Tradutor", "categoria": "Cultural",
     "sugestao": "Homenagem aos intérpretes das línguas indígenas do Vale (Marubo, Matis, Kanamari, Kulina, Mayoruna).",
     "formato": "Card / Carrossel"},
    {"data": "08-09", "titulo": "Dia Internacional dos Povos Indígenas (ONU)", "categoria": "Internacional · DATA MAIOR",
     "sugestao": "Mensagem em português + inglês para alcance internacional. Conexão com parceiros (RFN, BMZ).",
     "formato": "Card bilíngue + Vídeo legendado"},
    {"data": "09-05", "titulo": "Dia da Amazônia", "categoria": "Meio ambiente · DATA MAIOR",
     "sugestao": "Card vinculando a UNIVAJA à proteção da Amazônia. Destaque para os povos isolados como guardiões.",
     "formato": "Carrossel + Vídeo curto"},
    {"data": "10-12", "titulo": "Dia da Resistência Indígena", "categoria": "Indígena nacional",
     "sugestao": "Pauta histórica: 500+ anos de resistência. Vídeo com depoimento de uma liderança mais velha.",
     "formato": "Vídeo / Reels"},
    {"data": "11-20", "titulo": "Dia da Consciência Negra", "categoria": "Aliança",
     "sugestao": "Solidariedade entre povos indígenas e quilombolas em defesa de territórios tradicionais.",
     "formato": "Card / Carrossel"},
    {"data": "12-10", "titulo": "Dia dos Direitos Humanos", "categoria": "Direitos",
     "sugestao": "Card sobre violações de direitos indígenas no Vale do Javari — orientação jurídica obrigatória.",
     "formato": "Card / Nota oficial"},
]


# ══════════════════════════════════════════════════════════════════════════════
#  ESTADO
# ══════════════════════════════════════════════════════════════════════════════
if "datas_fixas" not in st.session_state:
    st.session_state.datas_fixas = [dict(d) for d in DATAS_FIXAS_DEFAULT]

if "agenda_pautas" not in st.session_state:
    st.session_state.agenda_pautas = []  # pautas dinâmicas criadas pelos comunicadores

if "programacao_mensal" not in st.session_state:
    st.session_state.programacao_mensal = ""

if "aprovadores_emails" not in st.session_state:
    st.session_state.aprovadores_emails = "imprensa@univaja.org"

# Estado do monitor (preservado)
TEMAS_MONITOR_DEFAULT = {
    "Povos isolados": {"tag": "pauta permanente", "badge": "badge-perm",
        "termos": ["povos isolados Vale do Javari", "isolados voluntários Amazônia", "FUNAI isolados"]},
    "Garimpo e invasão": {"tag": "denúncia / vigilância", "badge": "badge-den",
        "termos": ["garimpo ilegal Vale do Javari", "invasão terra indígena Javari", "mineração ilegal Amazônia"]},
    "Direitos indígenas": {"tag": "pauta política", "badge": "badge-perm",
        "termos": ["direitos indígenas Brasil", "demarcação terra indígena", "marco temporal indígena"]},
    "FUNAI e políticas": {"tag": "institucional", "badge": "badge-seg",
        "termos": ["FUNAI política indigenista", "ministério povos indígenas", "política indigenista Brasil"]},
    "Violência e assassinatos": {"tag": "denúncia", "badge": "badge-den",
        "termos": ["violência contra indígenas Amazônia", "assassinato liderança indígena", "conflito terra indígena"]},
    "Bruno e Dom": {"tag": "memória", "badge": "badge-pos",
        "termos": ["Bruno Pereira Dom Phillips", "Vale do Javari jornalista", "jornalista indigenista assassinado"]},
    "Meio ambiente": {"tag": "ambiental", "badge": "badge-pos",
        "termos": ["desmatamento Amazônia Vale do Javari", "proteção territorial indígena", "biodiversidade Javari"]},
    "Saúde indígena": {"tag": "social", "badge": "badge-pos",
        "termos": ["saúde indígena SESAI Javari", "doenças comunidades indígenas", "assistência médica aldeia"]},
    "Educação indígena": {"tag": "social", "badge": "badge-pos",
        "termos": ["educação escolar indígena Amazônia", "escola indígena Javari", "educação bilíngue indígena"]},
    "Amazon Week 2026": {"tag": "evento atual", "badge": "badge-int",
        "termos": ["Amazon Week 2026 Berlin", "liderança indígena fronteira", "UNIVAJA international event"]},
    "Clima e COP": {"tag": "internacional", "badge": "badge-int",
        "termos": ["mudança climática povos indígenas", "COP indigena Amazônia", "clima floresta tropical"]},
    "Atalaia do Norte": {"tag": "local", "badge": "badge-local",
        "termos": ["Atalaia do Norte notícias", "Amazonas terra indígena", "Vale do Javari município"]},
}
if "temas_monitor" not in st.session_state:
    st.session_state.temas_monitor = {k: dict(v) for k, v in TEMAS_MONITOR_DEFAULT.items()}

if "termos_extras_monitor" not in st.session_state:
    st.session_state.termos_extras_monitor = []


# ══════════════════════════════════════════════════════════════════════════════
#  ABAS — ordem: Como usar → Fluxos → Glossário → MONITOR → AGENDA → Aprovação
# ══════════════════════════════════════════════════════════════════════════════
aba_h, aba1, aba2, aba_monitor, aba_agenda, aba_aprov = st.tabs([
    "ℹ️ Como usar",
    "📋 Fluxos integrados",
    "📖 Glossário & referência",
    "🔍 Monitor de pautas",
    "📅 Agenda dinâmica",
    "✅ Aprovação",
])


# ══════════════════════════════════════════════════════════════════════════════
#  ABA — COMO USAR
# ══════════════════════════════════════════════════════════════════════════════
with aba_h:
    st.markdown(section_title("Como usar esta plataforma", "padrao"), unsafe_allow_html=True)

    col_u1, col_u2 = st.columns([1.2, 1])

    with col_u1:
        st.markdown(f"""
        ### 🎯 O que é
        A **ASCOM UNIVAJA** é a plataforma central de comunicação. Reúne:

        - 📋 **Fluxos integrados** — passo a passo visual de cada tipo de publicação
        - 📖 **Glossário** — tipos de texto, pautas prioritárias e pilares
        - 🔍 **Monitor de pautas** — busca notícias atuais sobre os temas UNIVAJA
        - 📅 **Agenda dinâmica** — calendário de datas fixas + planejamento aberto
        - ✅ **Aprovação** — envia relatório PDF para os representantes assinarem

        ### 🚦 Fluxo da reunião semanal
        """)

        usos = [
            ("1️⃣ Antes da reunião", "Comunicador da semana abre o <strong>🔍 Monitor de pautas</strong>, busca notícias atuais sobre os temas selecionados e separa 3-5 sugestões."),
            ("2️⃣ Reunião (segunda)", "Equipe abre a <strong>📅 Agenda dinâmica</strong>, consulta as <strong>datas fixas próximas</strong>, adiciona as pautas do mês e define responsáveis."),
            ("3️⃣ Durante a semana", "Cada um acompanha os <strong>📋 Fluxos integrados</strong> e cumpre a sua etapa (briefing, design, legenda, aprovação)."),
            ("4️⃣ Fim da reunião", "Ponto focal abre <strong>✅ Aprovação</strong>, gera o relatório PDF e envia por email para os representantes."),
        ]
        for momento, desc in usos:
            st.markdown(f"""
            <div class="card-grafismo" style="margin-bottom:10px">
                <div class="card-grafismo-conteudo">
                    <strong style="font-size:13px;color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">{momento}</strong>
                    <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_u2:
        st.markdown("### 💡 Princípios")
        principios = [
            ("🎨 Identidade", "Segue rigorosamente o Manual de Marca UNIVAJA — cores e grafismos dos povos do Vale."),
            ("📱 Acessível", "Funciona no navegador de qualquer celular ou computador. Não precisa instalar nada."),
            ("⚙️ Customizável", "Datas fixas, temas, termos e emails são editáveis pelos comunicadores."),
            ("🤝 Colaborativa", "Permite exportar JSON e compartilhar no grupo ASCOM."),
            ("📄 Aprovação por PDF", "Toda agenda fechada vira PDF para representantes aprovarem por email."),
        ]
        for titulo_p, desc in principios:
            st.markdown(f"""
            <div class="card card-cinza" style="margin-bottom:8px">
                <strong style="font-size:13px;color:{VERDE_PRETO}">{titulo_p}</strong>
                <p style="font-size:12px;color:{CINZA};margin:4px 0 0;line-height:1.5">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(divisor("marubo"), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA — FLUXOS INTEGRADOS (com infográficos)
# ══════════════════════════════════════════════════════════════════════════════
def render_fluxograma(titulo, etapas, cor_titulo=VERDE):
    """Renderiza um fluxograma vertical visual com cards conectados por setas."""
    blocos = []
    for i, e in enumerate(etapas):
        cor = e.get("cor", cor_titulo)
        blocos.append(f"""
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:6px">
            <div style="background:{cor};color:white;width:48px;height:48px;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800;
                        flex-shrink:0;border:3px solid white;box-shadow:0 3px 10px rgba(0,0,0,.15);
                        font-family:'Battambang','Archivo',serif">{e.get('num','')}</div>
            <div style="flex:1;background:white;border-radius:10px;padding:12px 18px;border-left:5px solid {cor};
                        box-shadow:0 2px 8px rgba(0,0,0,.04)">
                <div style="font-weight:700;color:{VERDE_PRETO};font-size:14px;margin-bottom:4px">
                    {e.get('icon','')} {e.get('titulo','')}
                </div>
                <div style="font-size:12px;color:{CINZA};line-height:1.5">{e.get('descricao','')}</div>
                <div style="background:{CREME};margin-top:8px;padding:6px 10px;border-radius:6px;font-size:11px;color:{VERDE_PRETO};
                            border-left:3px solid {cor}">
                    <strong>👤 {e.get('responsavel','')}</strong> · 📦 {e.get('entrega','')}
                </div>
            </div>
        </div>
        """)
        if i < len(etapas) - 1:
            blocos.append(f"""
            <div style="margin-left:22px;font-size:18px;color:{cor};line-height:1;padding:2px 0">▼</div>
            """)
    return "".join(blocos)


with aba1:
    st.markdown(section_title("Fluxos integrados de comunicação", "padrao"), unsafe_allow_html=True)
    st.caption("Fluxogramas visuais de cada tipo de publicação. Use antes da reunião e durante a produção.")

    # ── Ciclo semanal — infográfico circular ─────────────────────────────
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown(section_title("◆ Fluxo 1 — Ciclo semanal", "padrao"), unsafe_allow_html=True)

    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    ciclo_etapas = [
        ("SEGUNDA",  "🗣️", "Reunião de pauta",  "Seleção de temas e divisão de tarefas",  VERDE_PRETO),
        ("TER-QUA",  "🎨", "Produção",          "Roteiros, cards, vídeos e textos",         VERDE_ESC),
        ("QUI-SEX",  "✅", "Aprovação",         "Envio ao grupo e validação da coord.",    VERMELHO_MED),
        ("SEXTA+",   "📤", "Publicação",        "TUMI/DÉBORA publicam nas redes",          PRIMARIA),
    ]
    for col, (dia, icon, titulo, desc, cor) in zip([col_c1, col_c2, col_c3, col_c4], ciclo_etapas):
        with col:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:18px 14px;text-align:center;border-top:5px solid {cor};
                        box-shadow:0 4px 12px rgba(0,0,0,.06);height:200px;display:flex;flex-direction:column;justify-content:space-between">
                <div>
                    <div style="font-size:11px;color:{cor};font-weight:800;letter-spacing:1.5px">{dia}</div>
                    <div style="font-size:36px;margin:8px 0">{icon}</div>
                    <div style="font-family:'Battambang',serif;font-size:16px;font-weight:700;color:{VERDE_PRETO}">{titulo}</div>
                </div>
                <div style="font-size:11px;color:{CINZA};line-height:1.4">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Fluxo 2A — Card / Imagem (fluxograma visual) ─────────────────────
    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown(section_title("◆ Fluxo 2A — Publicação de Card / Imagem", "verde"), unsafe_allow_html=True)

    etapas_2a = [
        {"num": "1", "icon": "💡", "titulo": "Proposta de pauta",
         "descricao": "Comunicador propõe tema na reunião de segunda. Define objetivo e público.",
         "responsavel": "Comunicador designado", "entrega": "Proposta no grupo ASCOM", "cor": VERDE},
        {"num": "2", "icon": "📝", "titulo": "Briefing para o designer",
         "descricao": "Comunicador escreve briefing claro: tema, texto principal, destaques e referências visuais.",
         "responsavel": "Comunicador → Designer", "entrega": "Briefing por escrito", "cor": VERDE},
        {"num": "3", "icon": "🎨", "titulo": "Criação do card",
         "descricao": "Designer cria o card seguindo o manual de marca: cores, fontes, grafismos e proporções.",
         "responsavel": "Designer", "entrega": "Card .PNG ou .JPG", "cor": VERDE},
        {"num": "4", "icon": "✍️", "titulo": "Redação da legenda",
         "descricao": "Comunicador redige: chamada + informação principal + hashtags (#UNIVAJA #ValeDoJavari).",
         "responsavel": "Comunicador responsável", "entrega": "Texto + hashtags", "cor": VERDE},
        {"num": "5", "icon": "📨", "titulo": "Envio para aprovação",
         "descricao": "Ponto focal envia card + legenda no grupo ASCOM. Material aguarda aval.",
         "responsavel": "Ponto focal", "entrega": "Material no grupo", "cor": VERMELHO_MED},
        {"num": "6", "icon": "✅", "titulo": "Aprovação da coordenação",
         "descricao": "Coordenação avalia. Aprovado → segue. Ajuste → retorna às etapas 3 ou 4.",
         "responsavel": "Coordenação ASCOM", "entrega": "Aprovação registrada", "cor": VERMELHO_MED},
        {"num": "7", "icon": "📤", "titulo": "Publicação nas redes",
         "descricao": "TUMI ou DÉBORA publicam no Instagram, LinkedIn e WhatsApp conforme orientação.",
         "responsavel": "TUMI / DÉBORA", "entrega": "✅ Post publicado", "cor": PRIMARIA},
    ]
    st.markdown(render_fluxograma("Card", etapas_2a, VERDE), unsafe_allow_html=True)

    st.markdown("""
    <div class="alerta">
        ⚠️ <strong>Regra inegociável:</strong> nenhum material pode ser publicado sem aprovação registrada no grupo ASCOM.
        Em caso de dúvida, aguardar. Melhor atrasar um dia do que publicar algo errado.
    </div>
    """, unsafe_allow_html=True)

    # ── Fluxo 2B — Vídeo / Reels ─────────────────────────────────────────
    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown(section_title("◆ Fluxo 2B — Publicação de Vídeo / Reels", "verde"), unsafe_allow_html=True)

    etapas_2b = [
        {"num": "1", "icon": "💡", "titulo": "Proposta de tema",
         "descricao": "Comunicador define formato: depoimento, cobertura ou boletim. Duração estimada.",
         "responsavel": "Comunicador designado", "entrega": "Proposta no grupo", "cor": VERDE_ESC},
        {"num": "2", "icon": "📜", "titulo": "Roteiro completo",
         "descricao": "Roteiro com contexto, falas, ordem das cenas. Máximo 90 segundos para Reels.",
         "responsavel": "Responsável pelo roteiro", "entrega": "Roteiro aprovado antes de gravar", "cor": VERDE_ESC},
        {"num": "3", "icon": "🎥", "titulo": "Gravação e edição",
         "descricao": "Gravar conforme roteiro. Edição com cortes, legendas em português, trilha e logo UNIVAJA.",
         "responsavel": "Equipe de produção", "entrega": "Vídeo .MP4 finalizado", "cor": VERDE_ESC},
        {"num": "4", "icon": "✍️", "titulo": "Legenda do post",
         "descricao": "Chamada + resumo + hashtags. Acessibilidade: legendas no vídeo são obrigatórias.",
         "responsavel": "Comunicador responsável", "entrega": "Texto + hashtags", "cor": VERDE_ESC},
        {"num": "5", "icon": "📨", "titulo": "Envio para aprovação",
         "descricao": "Ponto focal envia no grupo ASCOM. Material aguarda aval da coordenação.",
         "responsavel": "Ponto focal", "entrega": "Material no grupo", "cor": VERMELHO_MED},
        {"num": "6", "icon": "✅", "titulo": "Aprovação",
         "descricao": "Aprovado → publica. Ajuste → retorna às etapas 3 ou 4 com orientação clara.",
         "responsavel": "Coordenação ASCOM", "entrega": "Aprovação registrada", "cor": VERMELHO_MED},
        {"num": "7", "icon": "📤", "titulo": "Publicação",
         "descricao": "Instagram Reels, WhatsApp e LinkedIn. Adaptam legenda para cada rede.",
         "responsavel": "TUMI / DÉBORA", "entrega": "✅ Reels publicado", "cor": PRIMARIA},
    ]
    st.markdown(render_fluxograma("Vídeo", etapas_2b, VERDE_ESC), unsafe_allow_html=True)

    # ── Fluxo 3 — Político / Sensível ────────────────────────────────────
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown(section_title("◆ Fluxo 3 — Aprovação política (temas sensíveis)", "vermelho"), unsafe_allow_html=True)

    st.markdown("""
    <div class="alerta alerta-vermelho">
        🔴 <strong>Use este fluxo sempre que o material envolver:</strong> posicionamento político, denúncia,
        crise institucional, questão jurídica, imagem do Presidente ou qualquer assunto que possa
        afetar parceiros e patrocinadores.
    </div>
    """, unsafe_allow_html=True)

    etapas_3 = [
        {"num": "🚨", "icon": "🛑", "titulo": "Identificação do tema sensível",
         "descricao": "Qualquer comunicador identifica que envolve tema sensível. NÃO PRODUZ NADA AINDA.",
         "responsavel": "Qualquer comunicador", "entrega": "Alerta no grupo ASCOM", "cor": VERMELHO_ESC},
        {"num": "2", "icon": "📞", "titulo": "Consulta ao ponto focal",
         "descricao": "Aciona diretamente o ponto focal indígena. Descreve o fato e o que precisa ser comunicado.",
         "responsavel": "Comunicador → Ponto focal", "entrega": "Consulta registrada", "cor": VERMELHO_ESC},
        {"num": "3", "icon": "⚖️", "titulo": "Análise jurídica",
         "descricao": "Procuradoria avalia implicações legais. Verifica risco para a UNIVAJA e comunicadores.",
         "responsavel": "Procuradoria jurídica", "entrega": "Parecer jurídico", "cor": CINZA},
        {"num": "4", "icon": "🏛️", "titulo": "Posicionamento político",
         "descricao": "Coordenação geral valida a mensagem institucional ou define silêncio estratégico.",
         "responsavel": "Coordenação geral UNIVAJA", "entrega": "Orientação política", "cor": CINZA},
        {"num": "5", "icon": "🤝", "titulo": "Decisão conjunta",
         "descricao": "Coordenação + Procuradoria decidem juntos entre publicar, aguardar ou silêncio.",
         "responsavel": "Coordenação + Procuradoria", "entrega": "Decisão comunicada", "cor": VERMELHO_MED},
        {"num": "6", "icon": "▶️", "titulo": "Execução",
         "descricao": "Equipe executa conforme decisão: publica pelo fluxo 2A/2B, aguarda ou foca em pauta positiva.",
         "responsavel": "Ponto focal + equipe ASCOM", "entrega": "Ação comunicada", "cor": PRIMARIA},
    ]
    st.markdown(render_fluxograma("Político", etapas_3, VERMELHO_ESC), unsafe_allow_html=True)

    # Três caminhos pós-decisão
    st.markdown("##### 🚦 Três caminhos possíveis após a decisão")
    col_pub, col_wait, col_sil = st.columns(3)
    with col_pub:
        st.markdown(f"""
        <div class="decisao-col decisao-pub" style="text-align:center">
            <div style="font-size:36px">✅</div>
            <strong style="font-size:14px">PUBLICAR</strong><br>
            <span style="font-size:12px">Aprovado pela coordenação e procuradoria. Segue pelo fluxo 2A/2B.</span>
        </div>
        """, unsafe_allow_html=True)
    with col_wait:
        st.markdown(f"""
        <div class="decisao-col decisao-wait" style="text-align:center">
            <div style="font-size:36px">⏳</div>
            <strong style="font-size:14px">AGUARDAR</strong><br>
            <span style="font-size:12px">Em avaliação. Não publica até nova orientação. Outros conteúdos seguem.</span>
        </div>
        """, unsafe_allow_html=True)
    with col_sil:
        st.markdown(f"""
        <div class="decisao-col decisao-silent" style="text-align:center">
            <div style="font-size:36px">🔇</div>
            <strong style="font-size:14px">SILÊNCIO ESTRATÉGICO</strong><br>
            <span style="font-size:12px">Não publica. Foco em conteúdo institucional positivo.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alerta alerta-vermelho" style="margin-top:14px">
        🔴 <strong>Regra de ouro:</strong> Em caso de dúvida, NÃO PUBLIQUE. Acione o ponto focal e aguarde orientação.
    </div>
    """, unsafe_allow_html=True)

    # ── Quem faz o quê ─────────────────────────────────────────────────────
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown(section_title("◆ Quem faz o quê — quadro de referência", "padrao"), unsafe_allow_html=True)

    pessoas = [
        ("Comunicador designado", "💡", "Propõe pauta, redige briefing e legenda, produz roteiro.", "Publicar nas redes sem aprovação."),
        ("Designer", "🎨", "Cria cards seguindo manual de marca. Entrega ao ponto focal.", "Alterar identidade visual sem aval. Publicar sozinho."),
        ("Ponto focal indígena", "🤝", "Articula equipe, envia material ao grupo, aciona coord. em temas sensíveis.", "Publicar material não aprovado pela coord. geral."),
        ("FRAN", "📱", "Gerencia estratégia e conteúdo das redes sociais (Instagram + LinkedIn).", "Publicar sem aprovação ASCOM."),
        ("TUMI / DÉBORA", "📤", "Únicas com acesso ao perfil do Instagram. Publicam após aprovação.", "Publicar material não aprovado. Dar acesso ao Instagram sem aval."),
        ("Coordenação ASCOM", "✅", "Aprova ou solicita ajuste de materiais no grupo ASCOM.", "Emitir posicionamentos políticos sem aval da coord. geral."),
        ("Coordenação geral UNIVAJA", "🏛️", "Valida pautas políticas e institucionais. Define posicionamento.", "— (instância máxima de aprovação)"),
        ("Procuradoria jurídica", "⚖️", "Orienta sobre implicações legais de denúncias e temas sensíveis.", "— (consultiva, não executa conteúdo)"),
    ]
    col_pq1, col_pq2 = st.columns(2)
    for i, (nome, icon, faz, nao) in enumerate(pessoas):
        col = col_pq1 if i % 2 == 0 else col_pq2
        with col:
            st.markdown(f"""
            <div class="pessoa-card">
                <div class="pessoa-nome" style="font-size:15px">{icon} {nome}</div>
                <div class="pessoa-faz">✅ {faz}</div>
                <div class="pessoa-nao">🚫 Não faz sem orientação: {nao}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA — GLOSSÁRIO (preservado)
# ══════════════════════════════════════════════════════════════════════════════
with aba2:
    st.markdown(section_title("Glossário básico e pautas de referência", "padrao"), unsafe_allow_html=True)
    st.caption("Respostas para as perguntas mais comuns sobre tipos de texto e temas prioritários.")

    col_g1, col_g2 = st.columns([1, 1])

    with col_g1:
        st.markdown("#### Tipos de formato")
        formatos = [
            ("Release", "Texto para jornalistas e veículos de imprensa. Conta um fato de interesse público de forma objetiva (quem, o quê, quando, onde, por quê, como). Nunca publicado diretamente nas redes.", "E-mail para jornalistas, portais, rádios"),
            ("Nota oficial", "Posicionamento formal da UNIVAJA sobre um fato ou situação. Linguagem direta, curta e institucional. Aprovada pela coordenação e procuradoria antes de ir a público.", "Site, redes sociais, imprensa"),
            ("Artigo", "Texto de análise e opinião, mais longo. Assinado por uma liderança ou comunicador. Aborda um tema com profundidade.", "Site, portais de parceiros, boletins"),
            ("Card (post)", "Imagem (ou carrossel) com texto curto, formatada para redes sociais. Segue o manual de marca.", "Instagram, Facebook, WhatsApp"),
            ("Legenda", "Texto que acompanha o card ou vídeo. Chamada + informação principal + hashtags.", "Campo de descrição do post"),
            ("Vídeo / Reels", "Vídeo curto (15-90s) com roteiro, gravação e edição. Depoimento, cobertura ou boletim.", "Instagram Reels, WhatsApp, YouTube"),
            ("Boletim interno", "Áudio ou texto com informações para as aldeias. Linguagem acessível, nas línguas dos povos quando possível.", "WhatsApp dos comunicadores, rádio"),
        ]
        for titulo_f, desc, canal in formatos:
            st.markdown(f"""
            <div class="gloss-card">
                <div class="gloss-titulo">{titulo_f}</div>
                <div class="gloss-desc">{desc}</div>
                <span class="gloss-canal">📡 {canal}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_g2:
        st.markdown("#### Pautas prioritárias da UNIVAJA")
        st.markdown(f"""
        <div class="card card-azul" style="margin-bottom:8px">
            <strong style="color:{VERDE_PRETO};font-size:13px">📰 PAUTAS INFORMATIVAS</strong>
            <ul style="font-size:13px;margin:8px 0 0;padding-left:18px;line-height:1.8">
                <li>História de luta e conquistas dos Povos do Vale do Javari</li>
                <li>Demarcação da Terra Indígena — União dos Povos</li>
                <li>Conquista da saúde e educação indígena</li>
                <li>Informações sobre as 8 associações de base da UNIVAJA</li>
                <li>Agendas e atividades da coordenação</li>
                <li>Ameaças institucionais (PECs, projetos de lei)</li>
                <li>Informes sobre programas sociais</li>
                <li>Informes sobre os povos isolados</li>
                <li>Direitos indígenas e papel das instituições</li>
                <li>Segurança digital: combate a notícias falsas</li>
            </ul>
        </div>
        <div class="card card-verde" style="margin-bottom:8px">
            <strong style="color:{VERDE};font-size:13px">🌱 PAUTAS POSITIVAS</strong>
            <ul style="font-size:13px;margin:8px 0 0;padding-left:18px;line-height:1.8">
                <li>Cultura dos Povos do Vale do Javari</li>
                <li>Datas comemorativas e celebrativas</li>
                <li>Festas e rituais dos Povos do Vale do Javari</li>
                <li>Atuação da UNIVAJA e das associações de base</li>
                <li>Protagonismo e lideranças indígenas</li>
            </ul>
        </div>
        <div class="card card-vermelho">
            <strong style="color:{PRIMARIA};font-size:13px">🚨 PAUTAS DE DENÚNCIA</strong>
            <ul style="font-size:13px;margin:8px 0 0;padding-left:18px;line-height:1.8">
                <li>Violência e violações de direitos</li>
                <li>Invasões e exploração do território</li>
                <li>Ameaças, perseguição ou assassinatos</li>
                <li>Racismo contra os Povos Indígenas</li>
            </ul>
            <div class="alerta" style="margin-top:8px;font-size:12px">
                ⚠️ Toda denúncia deve ser orientada pela Procuradoria Jurídica
                e validada pela coordenação antes de publicar.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Pilares da comunicação UNIVAJA")
        pilares = [
            ("Autodeterminação", "Os povos do Vale do Javari são protagonistas de suas próprias narrativas. Eles determinam o que, como e quando comunicar."),
            ("Luta e resistência", "A comunicação é ferramenta estratégica de defesa territorial e cultural."),
            ("Valorização cultural", "Fortalecer identidades, línguas e tradições dos povos do Vale do Javari."),
            ("Denúncia", "Expor publicamente violações de direitos — sempre com orientação jurídica."),
        ]
        for nome, desc in pilares:
            st.markdown(f"""
            <div class="card-grafismo" style="margin-bottom:10px">
                <div class="card-grafismo-conteudo">
                    <strong style="font-size:13px;color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">{nome}</strong>
                    <p style="font-size:12px;color:{CINZA};margin:6px 0 0;line-height:1.5">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA — MONITOR DE PAUTAS (antes da agenda, com termos pré-definidos)
# ══════════════════════════════════════════════════════════════════════════════
with aba_monitor:
    st.markdown(section_title("Monitor de pautas — notícias atuais", "padrao"), unsafe_allow_html=True)
    st.caption("Busca notícias recentes nos temas prioritários da UNIVAJA. Use antes da reunião de segunda.")

    st.markdown(f"""
    <div class="alerta alerta-azul">
        💡 Os temas abaixo já vêm pré-configurados com termos otimizados.
        A busca é direcionada às notícias <strong>mais atuais</strong> (última semana por padrão).
    </div>
    """, unsafe_allow_html=True)

    TEMAS = st.session_state.temas_monitor

    st.markdown("#### 1 · Selecione os temas")
    cols_temas = st.columns(4)
    selecionados_temas = []
    for i, (tema, info) in enumerate(TEMAS.items()):
        with cols_temas[i % 4]:
            sel = st.checkbox(tema, key=f"tema_monitor_{tema}")
            if sel:
                selecionados_temas.append(tema)
            st.markdown(f'<span class="badge {info["badge"]}" style="font-size:10px">{info["tag"]}</span>',
                        unsafe_allow_html=True)

    st.markdown(divisor("pontos"), unsafe_allow_html=True)

    st.markdown("#### 2 · Ou adicione um termo específico")
    col_ti, col_tb = st.columns([4, 1])
    with col_ti:
        termo_custom = st.text_input("",
            placeholder="Ex: garimpo ilegal, saúde indígena, Atalaia do Norte...",
            label_visibility="collapsed", key="termo_custom_monitor")
    with col_tb:
        if st.button("+ Adicionar", use_container_width=True, key="add_termo_monitor"):
            if termo_custom and termo_custom not in st.session_state.termos_extras_monitor:
                st.session_state.termos_extras_monitor.append(termo_custom)
                st.rerun()

    if st.session_state.termos_extras_monitor:
        st.markdown("**Termos adicionados:**")
        cols_rem = st.columns(min(len(st.session_state.termos_extras_monitor), 5))
        for i, t in enumerate(st.session_state.termos_extras_monitor):
            with cols_rem[i % len(cols_rem)]:
                if st.button(f"✕ {t}", key=f"rem_monitor_{t}"):
                    st.session_state.termos_extras_monitor.remove(t)
                    st.rerun()

    st.markdown("#### 3 · Período (padrão: última semana — sempre as mais atuais)")
    periodo = st.radio("",
        ["Últimas 24h", "Últimos 3 dias", "Última semana", "Último mês"],
        horizontal=True, label_visibility="collapsed", index=2, key="periodo_monitor")

    periodo_gn_map = {"Últimas 24h": "d", "Últimos 3 dias": "w", "Última semana": "w", "Último mês": "m"}
    periodo_gt_map = {"Últimas 24h": "now 1-d", "Últimos 3 dias": "now 7-d",
                     "Última semana": "now 7-d", "Último mês": "today 1-m"}
    periodo_gn = periodo_gn_map[periodo]
    periodo_gt = periodo_gt_map[periodo]

    todos_termos = []
    for tema in selecionados_temas:
        todos_termos.extend(TEMAS[tema]["termos"])
    todos_termos.extend(st.session_state.termos_extras_monitor)
    todos_termos = list(dict.fromkeys(todos_termos))

    if not todos_termos:
        todos_termos = ["UNIVAJA", "povos indígenas Vale do Javari", "Vale do Javari"]

    # Forçar busca por mais atuais ordenando por data
    q_encoded = quote_plus(" OR ".join([f'"{t}"' for t in todos_termos[:5]]))
    q_trends = ",".join(todos_termos[:5])

    # &tbs=qdr:X,sbd:1 ordena por data; sbd=1 = sorted by date
    url_gnoticias = f"https://news.google.com/search?q={q_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-BR&as_qdr={periodo_gn}"
    url_gsearch = f"https://www.google.com/search?q={q_encoded}&tbm=nws&hl=pt-BR&tbs=qdr:{periodo_gn},sbd:1"
    url_trends = f"https://trends.google.com/trends/explore?q={quote_plus(q_trends)}&geo=BR&date={quote_plus(periodo_gt)}&hl=pt-BR"
    url_trends_ex = f"https://trends.google.com/trends/explore?q={quote_plus(todos_termos[0])}&geo=BR&hl=pt-BR"

    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown("#### 4 · Abra as buscas (ordenadas pelas mais recentes)")

    if selecionados_temas or st.session_state.termos_extras_monitor:
        st.markdown(f"""
        <div class="alerta alerta-verde">
            ✅ <strong>{len(todos_termos)} termos selecionados.</strong>
            As buscas abaixo já vêm com filtro de data e ordenação cronológica.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alerta">
            💡 Selecione ao menos um tema para personalizar os links de busca.
        </div>
        """, unsafe_allow_html=True)

    pills = " ".join([f'<span class="termo-pill">{t}</span>' for t in todos_termos])
    st.markdown(f"<div style='margin-bottom:14px'>{pills}</div>", unsafe_allow_html=True)

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown(f"""
        <a href="{url_gnoticias}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">📰 Google Notícias →</div>
            <div class="link-busca-desc">Manchetes mais recentes com os termos selecionados.</div>
        </a>
        <a href="{url_gsearch}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">🔎 Google Search News (mais recentes) →</div>
            <div class="link-busca-desc">Ordenado por data — as notícias mais novas primeiro.</div>
        </a>
        """, unsafe_allow_html=True)
    with col_l2:
        st.markdown(f"""
        <a href="{url_trends}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">📈 Google Trends — comparativo →</div>
            <div class="link-busca-desc">Qual termo está em alta no Brasil.</div>
        </a>
        <a href="{url_trends_ex}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">🔬 Google Trends — explorar →</div>
            <div class="link-busca-desc">Explora o primeiro termo em profundidade.</div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown(divisor("pontos"), unsafe_allow_html=True)
    st.markdown("#### 5 · O que fazer com o que encontrou")

    col_o1, col_o2 = st.columns(2)
    with col_o1:
        st.markdown(f"""
        <div class="card card-azul">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">📅 Antes da reunião de segunda</strong>
            <p style="font-size:13px;margin-top:10px;line-height:1.6;color:{CINZA}">
            Selecione 3–5 notícias relevantes e leve como sugestão de pauta.
            Anote qual temática está em alta para justificar a escolha.
            Indique o formato sugerido (card, vídeo ou boletim).
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_o2:
        st.markdown(f"""
        <div class="card card-verde">
            <strong style="color:{VERDE};text-transform:uppercase;letter-spacing:0.5px">✏️ Durante a produção (ter–qua)</strong>
            <p style="font-size:13px;margin-top:10px;line-height:1.6;color:{CINZA}">
            Use as notícias para embasar o card ou o roteiro do vídeo.
            Cite a fonte no briefing enviado ao designer.
            Verifique se o tema ainda é atual antes de publicar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Editor de temas
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    with st.expander("⚙️ Personalizar temas e termos (avançado)"):
        st.caption("Formato: `TEMA: termo1, termo2, termo3` — um tema por linha.")
        temas_atuais_txt = "\n".join([
            f"{tema}: {', '.join(info['termos'])}" for tema, info in TEMAS.items()
        ])
        editor = st.text_area("Temas e termos",
            value=temas_atuais_txt, height=280, label_visibility="collapsed",
            key="editor_temas_monitor")
        col_save, col_reset = st.columns([3, 1])
        with col_save:
            if st.button("💾 Salvar alterações", type="primary", use_container_width=True, key="salvar_temas_monitor"):
                novos = {}
                for linha in editor.split("\n"):
                    if ":" in linha:
                        tema, termos = linha.split(":", 1)
                        tema = tema.strip()
                        termos_list = [t.strip() for t in termos.split(",") if t.strip()]
                        if tema and termos_list:
                            tag_antigo = TEMAS.get(tema, {}).get("tag", "personalizado")
                            badge_antigo = TEMAS.get(tema, {}).get("badge", "badge-perm")
                            novos[tema] = {"tag": tag_antigo, "badge": badge_antigo, "termos": termos_list}
                st.session_state.temas_monitor = novos
                st.success("✅ Temas atualizados!")
                st.rerun()
        with col_reset:
            if st.button("↺ Resetar", use_container_width=True, key="reset_temas_monitor"):
                st.session_state.temas_monitor = {k: dict(v) for k, v in TEMAS_MONITOR_DEFAULT.items()}
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  ABA — AGENDA DINÂMICA
# ══════════════════════════════════════════════════════════════════════════════
TIPOS_POST = ["Card único", "Carrossel", "Vídeo / Reels", "Stories",
              "Boletim interno", "Release", "Nota oficial", "Artigo", "Live"]
REDES_POST = ["Instagram", "Facebook", "LinkedIn", "WhatsApp",
              "YouTube", "TikTok", "Site UNIVAJA", "Imprensa"]
ETAPAS_AGENDA = ["💡 Ideia", "✏️ Em produção", "⏳ Aguardando aprovação",
                 "✅ Aprovado", "📤 Publicado"]

with aba_agenda:
    st.markdown(section_title("Agenda dinâmica — montem juntos na reunião", "padrao"), unsafe_allow_html=True)
    st.caption("Construa o cronograma de postagens do mês. Cada pauta tem responsável, tipo e fluxo. No final, envie para o representante aprovar.")

    # ── Sub-abas dentro da agenda ───────────────────────────────────────────
    sub_cal, sub_nova, sub_kan, sub_mes = st.tabs([
        "📆 Datas fixas (calendário)",
        "➕ Adicionar pauta da semana",
        "📊 Kanban de produção",
        "📝 Programação mensal aberta",
    ])

    # ── DATAS FIXAS ─────────────────────────────────────────────────────────
    with sub_cal:
        st.markdown("##### 📆 Calendário de datas fixas — postagens obrigatórias")
        st.caption("Datas representativas dos povos indígenas, UNIVAJA, Vale do Javari e meio ambiente. Use como base do cronograma anual.")

        # Datas próximas (até 60 dias)
        hoje = date.today()
        proximas = []
        for d in st.session_state.datas_fixas:
            try:
                mes_str, dia_str = d["data"].split("-")
                dt_ano = date(hoje.year, int(mes_str), int(dia_str))
                if dt_ano < hoje:
                    dt_ano = date(hoje.year + 1, int(mes_str), int(dia_str))
                dias = (dt_ano - hoje).days
                if dias <= 90:
                    proximas.append((dias, dt_ano, d))
            except Exception:
                pass

        if proximas:
            st.markdown(f"##### 🚨 Datas nos próximos 90 dias")
            for dias, dt, d in sorted(proximas, key=lambda x: x[0]):
                if dias == 0: selo, cor = "HOJE", PRIMARIA
                elif dias <= 7: selo, cor = f"em {dias} dia(s)", VERMELHO_MED
                elif dias <= 30: selo, cor = f"em {dias} dias", VERDE_ESC
                else: selo, cor = f"em {dias} dias", VERDE

                meses_pt = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
                data_fmt = f"{dt.day:02d} {meses_pt[dt.month-1]} {dt.year}"

                with st.container():
                    col_d, col_c = st.columns([5, 1])
                    with col_d:
                        st.markdown(f"""
                        <div class="card" style="border-left:5px solid {cor};margin-bottom:6px">
                            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
                                <div style="flex:1;min-width:260px">
                                    <div style="display:flex;gap:8px;align-items:center;margin-bottom:4px">
                                        <span style="background:{cor};color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;letter-spacing:0.5px">{selo}</span>
                                        <span style="font-weight:700;font-size:14px;color:{VERDE_PRETO}">📅 {data_fmt}</span>
                                    </div>
                                    <div style="font-weight:700;font-size:15px;color:{VERDE_PRETO};margin-bottom:4px">{d['titulo']}</div>
                                    <div style="font-size:11px;color:{CINZA};margin-bottom:6px">
                                        🏷️ {d['categoria']} · 📝 {d['formato']}
                                    </div>
                                    <div style="font-size:12px;color:{CINZA};line-height:1.5;font-style:italic;background:{CREME};padding:8px 10px;border-radius:6px">
                                        💡 <strong>Sugestão:</strong> {d['sugestao']}
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_c:
                        if st.button("➕ Adicionar à agenda", key=f"add_cal_{d['titulo']}_{dt.year}", use_container_width=True):
                            nova = {
                                "id": str(uuid.uuid4())[:8],
                                "data": dt.isoformat(),
                                "titulo": d["titulo"],
                                "responsavel": "",
                                "tipo": d["formato"].split("/")[0].strip() if "/" in d["formato"] else d["formato"],
                                "redes": ["Instagram"],
                                "etapa": ETAPAS_AGENDA[0],
                                "briefing": d["sugestao"],
                                "origem": "calendário fixo",
                            }
                            st.session_state.agenda_pautas.append(nova)
                            st.success(f"✅ '{d['titulo']}' adicionado à agenda!")
                            st.rerun()

        # Editor das datas fixas (avançado)
        st.markdown(divisor("zig"), unsafe_allow_html=True)
        with st.expander("📋 Ver todas as datas do calendário anual"):
            for d in sorted(st.session_state.datas_fixas, key=lambda x: x["data"]):
                meses_pt = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
                try:
                    m, dd = d["data"].split("-")
                    data_label = f"{dd}/{m} ({meses_pt[int(m)-1]})"
                except Exception:
                    data_label = d["data"]
                st.markdown(f"""
                <div style="background:white;border-left:4px solid {VERDE};padding:8px 12px;border-radius:6px;margin-bottom:6px;font-size:12px">
                    <strong style="color:{VERDE_PRETO}">{data_label} — {d['titulo']}</strong><br>
                    <span style="color:{CINZA}">{d['categoria']} · {d['formato']}</span><br>
                    <span style="font-style:italic;color:{CINZA}">{d['sugestao']}</span>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("✏️ Editar / adicionar datas fixas"):
            st.caption("Cada linha: `MM-DD | Título | Categoria | Formato | Sugestão de postagem`")
            datas_txt = "\n".join([
                f"{d['data']} | {d['titulo']} | {d['categoria']} | {d['formato']} | {d['sugestao']}"
                for d in st.session_state.datas_fixas
            ])
            editor_datas = st.text_area("Datas", value=datas_txt, height=300,
                                       label_visibility="collapsed", key="editor_datas_fixas")
            col_sd, col_rd = st.columns([3, 1])
            with col_sd:
                if st.button("💾 Salvar datas fixas", type="primary", use_container_width=True, key="salvar_datas"):
                    novas = []
                    for linha in editor_datas.split("\n"):
                        partes = [p.strip() for p in linha.split("|")]
                        if len(partes) >= 5:
                            novas.append({"data": partes[0], "titulo": partes[1],
                                         "categoria": partes[2], "formato": partes[3],
                                         "sugestao": partes[4]})
                    st.session_state.datas_fixas = novas
                    st.success(f"✅ {len(novas)} datas salvas!")
                    st.rerun()
            with col_rd:
                if st.button("↺ Resetar", use_container_width=True, key="reset_datas"):
                    st.session_state.datas_fixas = [dict(d) for d in DATAS_FIXAS_DEFAULT]
                    st.rerun()

    # ── NOVA PAUTA ────────────────────────────────────────────────────────
    with sub_nova:
        st.markdown("##### ➕ Adicionar pauta à agenda da semana")
        st.caption("Use na reunião para registrar cada pauta proposta. Os campos são abertos — adaptem ao contexto.")

        with st.form("form_nova_agenda", clear_on_submit=True):
            col_t, col_d = st.columns([3, 1])
            with col_t:
                titulo_p = st.text_input("📌 Pauta / o que será publicado *",
                    placeholder="ex: Cobertura da assembleia / Card 19/04 / Boletim sobre invasão")
            with col_d:
                data_p = st.date_input("📅 Data *", value=date.today(), format="DD/MM/YYYY")

            col_ti, col_re = st.columns(2)
            with col_ti:
                tipo_p = st.selectbox("📝 Tipo de postagem", TIPOS_POST)
            with col_re:
                redes_p = st.multiselect("📡 Redes / canais", REDES_POST, default=["Instagram"])

            col_r, col_e = st.columns(2)
            with col_r:
                resp_p = st.text_input("👤 Responsáveis (vários)",
                    placeholder="ex: Fran, Tumi, Designer João")
            with col_e:
                etapa_p = st.selectbox("📊 Etapa atual", ETAPAS_AGENDA, index=0)

            brief_p = st.text_area("📝 Briefing / observações",
                placeholder="Texto de referência, foto sugerida, fonte, fala da liderança...", height=100)

            if st.form_submit_button("➕ Adicionar à agenda", type="primary", use_container_width=True):
                if titulo_p.strip() and redes_p:
                    nova = {
                        "id": str(uuid.uuid4())[:8],
                        "data": data_p.isoformat(),
                        "titulo": titulo_p.strip(),
                        "responsavel": resp_p.strip(),
                        "tipo": tipo_p,
                        "redes": redes_p,
                        "etapa": etapa_p,
                        "briefing": brief_p.strip(),
                        "origem": "criada na reunião",
                    }
                    st.session_state.agenda_pautas.append(nova)
                    st.success("✅ Pauta adicionada!")
                    st.rerun()
                else:
                    st.error("⚠️ Título e ao menos uma rede são obrigatórios.")

    # ── KANBAN ───────────────────────────────────────────────────────────
    with sub_kan:
        st.markdown("##### 📊 Kanban — fluxo de produção das pautas")
        st.caption("Cada pauta tem um seletor para mover entre etapas. Funciona como um quadro de produção.")

        if not st.session_state.agenda_pautas:
            st.markdown("""
            <div class="alerta">
                📭 Nenhuma pauta na agenda ainda. Vá em <strong>➕ Adicionar pauta</strong> ou
                <strong>📆 Datas fixas</strong> para começar.
            </div>
            """, unsafe_allow_html=True)
        else:
            # Botão de remover tudo
            col_l, col_r = st.columns([3, 1])
            with col_r:
                if st.button("🗑️ Limpar agenda toda", type="secondary"):
                    st.session_state.agenda_pautas = []
                    st.rerun()

            # Distribui em colunas
            cols_k = st.columns(len(ETAPAS_AGENDA))
            for ci, etapa in enumerate(ETAPAS_AGENDA):
                cor_e = {
                    "💡 Ideia": VERDE_CLARO,
                    "✏️ Em produção": VERDE,
                    "⏳ Aguardando aprovação": VERMELHO_MED,
                    "✅ Aprovado": VERDE_ESC,
                    "📤 Publicado": PRIMARIA,
                }.get(etapa, VERDE)
                pautas_e = [p for p in st.session_state.agenda_pautas if p.get("etapa") == etapa]
                with cols_k[ci]:
                    st.markdown(f"""
                    <div style="background:{cor_e};color:white;padding:10px 12px;border-radius:8px;margin-bottom:8px;font-weight:700;text-align:center;font-size:12px;letter-spacing:0.5px">
                        {etapa}<br>
                        <span style="font-size:10px;opacity:.9;font-weight:500">{len(pautas_e)} pauta(s)</span>
                    </div>
                    """, unsafe_allow_html=True)

                    if not pautas_e:
                        st.markdown("""
                        <div style="background:white;border:1px dashed #d1d5db;border-radius:8px;padding:12px;text-align:center;font-size:11px;color:#9ca3af;margin-bottom:6px">
                            (vazio)
                        </div>
                        """, unsafe_allow_html=True)

                    for p in pautas_e:
                        try:
                            data_fmt = datetime.fromisoformat(p["data"]).strftime("%d/%m")
                        except Exception:
                            data_fmt = p.get("data","")
                        redes_s = " · ".join(p.get("redes", [])[:2])
                        st.markdown(f"""
                        <div style="background:white;border:1px solid #e5e7eb;border-left:3px solid {cor_e};border-radius:6px;padding:10px 10px;margin-bottom:6px">
                            <div style="font-weight:600;font-size:11px;color:{VERDE_PRETO};line-height:1.3;margin-bottom:4px">{p.get('titulo','')[:60]}</div>
                            <div style="font-size:10px;color:{CINZA}">
                                📅 {data_fmt}<br>
                                👤 {p.get('responsavel','—')}<br>
                                📡 {redes_s}<br>
                                📝 {p.get('tipo','')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Mover de etapa
                        nova_etapa = st.selectbox("→ mover",
                            ETAPAS_AGENDA, index=ETAPAS_AGENDA.index(etapa),
                            key=f"move_{p['id']}", label_visibility="collapsed")
                        if nova_etapa != etapa:
                            p["etapa"] = nova_etapa
                            st.rerun()
                        if st.button("🗑️", key=f"del_agenda_{p['id']}", help="Remover"):
                            st.session_state.agenda_pautas = [
                                x for x in st.session_state.agenda_pautas if x["id"] != p["id"]
                            ]
                            st.rerun()

    # ── PROGRAMAÇÃO MENSAL ABERTA ─────────────────────────────────────────
    with sub_mes:
        st.markdown("##### 📝 Programação mensal — espaço aberto")
        st.caption("Use este espaço para registrar a visão geral do mês: campanhas planejadas, foco temático, articulações, observações da coordenação.")

        st.session_state.programacao_mensal = st.text_area(
            "Programação aberta do mês",
            value=st.session_state.programacao_mensal,
            height=400,
            placeholder="""Exemplo:

JUNHO 2026 — FOCO: Memória e território

Semana 1 (02-08/06)
- 02 segunda: reunião de pauta
- 04 quarta: Amazon Week 2026 (Berlim) — cobertura remota
- 05 quinta: 4 anos sem Bruno e Dom (data sensível, validação obrigatória)
- 06-07: pautas das associações de base

Semana 2 (09-15/06)
- Campanha sobre povos isolados
- Card sobre direitos indígenas

Articulações:
- Confirmar parceria com Pixi Matis para foto do evento
- Validar texto da nota com a Procuradoria até 03/06

Observações da coordenação:
- Cuidado com termos políticos nas pautas
- Priorizar pauta positiva nesta primeira semana""",
            label_visibility="collapsed",
        )

        if st.button("💾 Salvar programação mensal", type="primary"):
            st.success("✅ Programação salva!")


# ══════════════════════════════════════════════════════════════════════════════
#  ABA — APROVAÇÃO (envio do PDF para representantes)
# ══════════════════════════════════════════════════════════════════════════════
def gerar_pdf_agenda(pautas, programacao, datas_proximas, titulo, observacoes):
    """Gera PDF da agenda para os representantes aprovarem."""
    from fpdf import FPDF

    def hex_rgb(h):
        h = h.lstrip("#")
        return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

    def latin(s):
        return (s or "").encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header vermelho
    r, g, b = hex_rgb(PRIMARIA)
    pdf.set_fill_color(r, g, b)
    pdf.rect(0, 0, 210, 42, "F")

    # Marubo branco no topo
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.4)
    x = 10; step = 5
    while x < 200:
        pdf.line(x, 4, x, 8); pdf.line(x, 8, x+step/2, 8)
        pdf.line(x+step/2, 8, x+step/2, 5); pdf.line(x+step/2, 5, x+step, 5)
        x += step

    # Logo UNIVAJA
    cx, cy = 22, 22
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*hex_rgb(VERMELHO_ESC))
    pdf.ellipse(cx-12, cy-12, 24, 24, "FD")
    pdf.set_fill_color(*hex_rgb(PRIMARIA))
    pdf.rect(cx-1.0, cy-8, 2.0, 1.8, "F")
    pdf.rect(cx-2.4, cy-6.2, 4.8, 1.8, "F")
    pdf.rect(cx-3.8, cy-4.4, 7.6, 1.8, "F")
    pdf.rect(cx-5.2, cy-2.6, 10.4, 1.8, "F")
    pdf.rect(cx-6.6, cy-0.8, 13.2, 2.0, "F")
    pdf.set_fill_color(*hex_rgb(VERMELHO_ESC))
    pdf.rect(cx-7.5, cy+1.4, 15, 0.8, "F")
    pdf.set_fill_color(*hex_rgb(VERDE_PRETO))
    pdf.rect(cx-7.5, cy+2.2, 15, 5.0, "F")
    pdf.set_fill_color(*hex_rgb(PRIMARIA))
    pdf.ellipse(cx-1.0, cy-10.5, 2.0, 2.0, "F")

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 22)
    pdf.set_xy(40, 11)
    pdf.cell(0, 8, latin("UNIVAJA"), ln=1)
    pdf.set_font("helvetica", "", 9)
    pdf.set_x(40)
    pdf.cell(0, 4, latin("UNIAO DOS POVOS DO VALE DO JAVARI"), ln=1)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_x(40)
    pdf.cell(0, 5, latin("ASCOM - Agenda para aprovacao"), ln=1)
    pdf.set_font("helvetica", "I", 8)
    pdf.set_x(40)
    pdf.cell(0, 4, latin(f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"), ln=1)

    pdf.set_fill_color(255, 255, 255)
    x = 10
    while x < 200:
        pdf.ellipse(x, 37, 0.8, 0.8, "F")
        pdf.ellipse(x+4, 37, 0.8, 0.8, "F")
        x += 8

    pdf.set_y(50)

    # Título
    pdf.set_text_color(*hex_rgb(VERDE_PRETO))
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 8, latin(titulo), ln=1)
    pdf.ln(2)

    # Resumo
    pdf.set_text_color(*hex_rgb(VERDE_PRETO))
    pdf.set_font("helvetica", "B", 13)
    pdf.cell(0, 7, latin("Resumo da agenda"), ln=1)
    pdf.set_text_color(*hex_rgb(CINZA))
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 5, latin(f"  - Total de pautas planejadas: {len(pautas)}"), ln=1)
    pdf.cell(0, 5, latin(f"  - Datas comemorativas nos proximos 90 dias: {len(datas_proximas)}"), ln=1)
    pdf.ln(3)

    # Datas próximas
    if datas_proximas:
        pdf.set_text_color(*hex_rgb(VERDE_PRETO))
        pdf.set_font("helvetica", "B", 13)
        pdf.cell(0, 7, latin("Datas fixas obrigatorias (proximos 90 dias)"), ln=1)
        for dias, dt, d in sorted(datas_proximas, key=lambda x: x[0])[:10]:
            pdf.set_fill_color(*hex_rgb(CREME))
            pdf.set_text_color(*hex_rgb(VERDE_PRETO))
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 6, latin(f"  {dt.strftime('%d/%m/%Y')} - {d['titulo']}"), ln=1)
            pdf.set_text_color(*hex_rgb(CINZA))
            pdf.set_font("helvetica", "", 9)
            pdf.multi_cell(0, 4.5, latin(f"    Categoria: {d['categoria']} | Formato: {d['formato']}"))
            pdf.multi_cell(0, 4.5, latin(f"    Sugestao: {d['sugestao']}"))
            pdf.ln(1)
        pdf.ln(3)

    # Pautas da agenda
    if pautas:
        pdf.set_text_color(*hex_rgb(VERDE_PRETO))
        pdf.set_font("helvetica", "B", 13)
        pdf.cell(0, 7, latin("Pautas planejadas"), ln=1)

        pautas_sorted = sorted(pautas, key=lambda p: p.get("data") or "")
        por_data_g = {}
        for p in pautas_sorted:
            por_data_g.setdefault(p.get("data") or "sem-data", []).append(p)

        for d, lista in por_data_g.items():
            if pdf.get_y() > 250: pdf.add_page()
            try:
                dt = datetime.fromisoformat(d)
                dias_pt = ["Segunda","Terca","Quarta","Quinta","Sexta","Sabado","Domingo"]
                dia_fmt = f"{dt.strftime('%d/%m/%Y')} - {dias_pt[dt.weekday()]}"
            except Exception:
                dia_fmt = d

            pdf.set_fill_color(*hex_rgb(VERDE_PRETO))
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("helvetica", "B", 11)
            pdf.cell(0, 7, latin(f"  {dia_fmt}"), ln=1, fill=True)
            pdf.ln(1)

            for p in lista:
                if pdf.get_y() > 260: pdf.add_page()
                pdf.set_text_color(*hex_rgb(VERDE_PRETO))
                pdf.set_font("helvetica", "B", 11)
                pdf.set_x(14)
                pdf.multi_cell(0, 6, latin(f"- {p.get('titulo','')}"))

                pdf.set_text_color(*hex_rgb(CINZA))
                pdf.set_font("helvetica", "", 9)
                pdf.set_x(14)
                pdf.multi_cell(0, 4.5, latin(f"  Tipo: {p.get('tipo','')} | Redes: {', '.join(p.get('redes',[]))}"))
                pdf.set_x(14)
                pdf.multi_cell(0, 4.5, latin(f"  Responsavel: {p.get('responsavel','—')} | Etapa: {p.get('etapa','')}"))
                if p.get("briefing"):
                    pdf.set_x(14)
                    pdf.set_font("helvetica", "I", 9)
                    pdf.multi_cell(0, 4.5, latin(f"  Briefing: {p['briefing']}"))
                pdf.ln(2)

    # Programação mensal
    if programacao.strip():
        if pdf.get_y() > 220: pdf.add_page()
        pdf.set_text_color(*hex_rgb(VERDE_PRETO))
        pdf.set_font("helvetica", "B", 13)
        pdf.cell(0, 7, latin("Programacao mensal aberta"), ln=1)
        pdf.set_text_color(*hex_rgb(CINZA))
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 5, latin(programacao))
        pdf.ln(3)

    # Observações
    if observacoes.strip():
        if pdf.get_y() > 240: pdf.add_page()
        pdf.set_text_color(*hex_rgb(VERDE_PRETO))
        pdf.set_font("helvetica", "B", 13)
        pdf.cell(0, 7, latin("Observacoes da reuniao"), ln=1)
        pdf.set_text_color(*hex_rgb(CINZA))
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 5, latin(observacoes))
        pdf.ln(3)

    # Bloco de aprovação
    if pdf.get_y() > 230: pdf.add_page()
    pdf.set_fill_color(*hex_rgb(CREME))
    pdf.set_text_color(*hex_rgb(VERDE_PRETO))
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 7, latin("APROVACAO DOS REPRESENTANTES"), ln=1, fill=True)
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(*hex_rgb(CINZA))
    pdf.multi_cell(0, 5, latin("Por favor, responder este email com APROVADO, AJUSTAR ou NAO PUBLICAR para cada bloco da agenda. Observacoes especificas podem ser anotadas por pauta."))
    pdf.ln(4)
    pdf.set_text_color(*hex_rgb(VERDE_PRETO))
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 8, latin("[ ] APROVADO integralmente"), ln=1)
    pdf.cell(0, 8, latin("[ ] APROVADO com ajustes (descrever abaixo)"), ln=1)
    pdf.cell(0, 8, latin("[ ] REJEITADO / Solicito nova proposta"), ln=1)
    pdf.ln(2)
    pdf.set_font("helvetica", "I", 9)
    pdf.cell(0, 5, latin("Observacoes do representante:"), ln=1)
    pdf.set_draw_color(*hex_rgb(CINZA))
    for _ in range(4):
        pdf.cell(0, 7, "", ln=1, border="B")

    # Rodapé
    pdf.set_y(-20)
    pdf.set_text_color(*hex_rgb(CINZA))
    pdf.set_font("helvetica", "I", 8)
    pdf.cell(0, 4, latin("ASCOM UNIVAJA - 2026 - documento de uso interno"), align="C", ln=1)

    result = pdf.output(dest="S")
    if isinstance(result, str):
        return result.encode("latin-1", "replace")
    return bytes(result)


with aba_aprov:
    st.markdown(section_title("Aprovação — enviar PDF para representantes", "vermelho"), unsafe_allow_html=True)
    st.caption("Gere o PDF da agenda fechada e envie por email para os representantes aprovarem.")

    st.markdown(f"""
    <div class="alerta alerta-azul">
        💡 <strong>Fluxo:</strong> 1) configure o título e observações da reunião · 2) baixe o PDF
        · 3) clique em <strong>📧 Enviar email</strong> e anexe o PDF baixado · 4) os representantes respondem
        com APROVADO ou ajustes.
    </div>
    """, unsafe_allow_html=True)

    col_t, col_p = st.columns(2)
    with col_t:
        titulo_pdf = st.text_input("Título do relatório",
            value=f"Agenda ASCOM — {date.today().strftime('%d/%m/%Y')}")
    with col_p:
        st.markdown("**Datas que serão incluídas:**")
        hoje = date.today()
        proximas_pdf = []
        for d in st.session_state.datas_fixas:
            try:
                m, dia = d["data"].split("-")
                dt = date(hoje.year, int(m), int(dia))
                if dt < hoje:
                    dt = date(hoje.year + 1, int(m), int(dia))
                dias = (dt - hoje).days
                if dias <= 90:
                    proximas_pdf.append((dias, dt, d))
            except Exception:
                pass
        st.caption(f"📌 {len(st.session_state.agenda_pautas)} pauta(s) + {len(proximas_pdf)} data(s) fixa(s) nos próximos 90 dias")

    observ_aprov = st.text_area("Observações para os representantes",
        placeholder="Pontos a debater, alertas, pedidos específicos de validação...", height=120)

    st.markdown(divisor("zig"), unsafe_allow_html=True)

    st.markdown("#### 📧 Emails dos representantes para aprovação")
    st.caption("Separe múltiplos emails por vírgula. O primeiro vai como destinatário, os demais como CC.")

    st.session_state.aprovadores_emails = st.text_input(
        "Emails de aprovação",
        value=st.session_state.aprovadores_emails,
        placeholder="imprensa@univaja.org, coordenacao@univaja.org, juridico@univaja.org",
        label_visibility="collapsed",
    )

    st.markdown(divisor("pontos"), unsafe_allow_html=True)

    # Gera o PDF
    try:
        pdf_bytes = gerar_pdf_agenda(
            st.session_state.agenda_pautas,
            st.session_state.programacao_mensal,
            proximas_pdf,
            titulo_pdf,
            observ_aprov,
        )

        col_dl, col_em = st.columns(2)

        with col_dl:
            st.download_button(
                "📄 Baixar PDF para aprovação",
                pdf_bytes,
                file_name=f"agenda_univaja_aprovacao_{date.today().isoformat()}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
            st.success("✅ PDF pronto para baixar")

        with col_em:
            emails = [e.strip() for e in st.session_state.aprovadores_emails.split(",") if e.strip()]
            destinatario = emails[0] if emails else "imprensa@univaja.org"
            cc = ",".join(emails[1:]) if len(emails) > 1 else ""

            n_pautas = len(st.session_state.agenda_pautas)
            n_datas = len(proximas_pdf)

            assunto = quote(f"[ASCOM UNIVAJA] {titulo_pdf} - aguardando aprovação")
            corpo = quote(f"""Olá,

Segue para aprovação a agenda de comunicação da ASCOM UNIVAJA.

📋 Resumo:
- {n_pautas} pauta(s) planejada(s)
- {n_datas} data(s) fixa(s) nos próximos 90 dias

📎 IMPORTANTE: Anexe a este email o PDF baixado da plataforma (arquivo agenda_univaja_aprovacao_{date.today().isoformat()}.pdf).

🙏 Pedimos que respondam com:
[ ] APROVADO integralmente
[ ] APROVADO com ajustes (descrever)
[ ] REJEITADO / Solicitar nova proposta

Observações adicionais da reunião:
{observ_aprov if observ_aprov.strip() else '(nenhuma)'}

Agradecemos a atenção e aguardamos retorno.

—
ASCOM UNIVAJA
União dos Povos do Vale do Javari""")

            cc_param = f"&cc={cc}" if cc else ""
            mailto = f"mailto:{destinatario}?subject={assunto}&body={corpo}{cc_param}"

            st.markdown(f"""
            <a href="{mailto}" target="_blank" style="display:block;background:{PRIMARIA};color:white;text-align:center;
                padding:14px 18px;border-radius:10px;text-decoration:none;font-weight:700;font-size:14px;
                letter-spacing:0.5px;width:100%;box-sizing:border-box">
                📧 Abrir email de aprovação
            </a>
            <div style="font-size:11px;color:{CINZA};margin-top:6px;text-align:center">
                Abre seu cliente de email com tudo preenchido<br>
                <strong>Anexe o PDF baixado manualmente</strong>
            </div>
            """, unsafe_allow_html=True)

    except Exception as ex:
        st.error(f"Erro ao gerar PDF: {ex}")

    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown("#### 🔄 Backup da agenda")
    backup = {
        "datas_fixas": st.session_state.datas_fixas,
        "agenda_pautas": st.session_state.agenda_pautas,
        "programacao_mensal": st.session_state.programacao_mensal,
        "aprovadores_emails": st.session_state.aprovadores_emails,
    }
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.download_button(
            "📥 Baixar backup completo (JSON)",
            json.dumps(backup, ensure_ascii=False, indent=2),
            file_name=f"agenda_univaja_{date.today().isoformat()}.json",
            mime="application/json",
            use_container_width=True,
        )
    with col_b2:
        arq = st.file_uploader("📤 Importar backup", type=["json"], label_visibility="collapsed")
        if arq is not None:
            try:
                dados = json.loads(arq.read())
                if st.button("Confirmar importação", type="primary"):
                    for k in ["datas_fixas", "agenda_pautas", "programacao_mensal", "aprovadores_emails"]:
                        if k in dados:
                            st.session_state[k] = dados[k]
                    st.success("✅ Backup restaurado!")
                    st.rerun()
            except Exception as ex:
                st.error(f"Erro: {ex}")

    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.caption("ASCOM UNIVAJA · 2026 — uso interno · Identidade visual baseada no Manual de Marca UNIVAJA")
