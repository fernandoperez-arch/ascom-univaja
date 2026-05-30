"""
PLANNER UNIVAJA — Plataforma de planejamento editorial
Os comunicadores propõem pautas, montam o cronograma de postagens, notificam a
imprensa e geram relatório em PDF para a reunião semanal da ASCOM.

Tudo customizável: tipos, redes, status, prioridades, temas e templates de email.
Identidade visual: Manual de Marca UNIVAJA (grafismos dos povos do Vale do Javari).
"""

import streamlit as st
from datetime import datetime, date, timedelta
from urllib.parse import quote
import json
import uuid

from fpdf import FPDF

from univaja_brand import (
    css_global, header, divisor, section_title, flow_kanban, logo_svg, sidebar_logo,
    PRIMARIA, VERMELHO_ESC, VERMELHO_MED, VERMELHO_CLARO,
    VERDE, VERDE_ESC, VERDE_PRETO, VERDE_CLARO,
    CINZA, PRETO, BRANCO, CREME,
)

st.set_page_config(
    page_title="Planner UNIVAJA — Pautas & Cronograma",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(css_global(), unsafe_allow_html=True)
st.markdown(
    header(
        "PLANNER UNIVAJA",
        "Pautas, cronograma e relatório · ASCOM",
        "Uso colaborativo · 2026",
    ),
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  DEFAULTS (tudo editável depois pela aba ⚙️ Configurações)
# ══════════════════════════════════════════════════════════════════════════════
TIPOS_DEFAULT = [
    "Card único", "Carrossel", "Vídeo / Reels", "Stories",
    "Boletim interno", "Release", "Nota oficial", "Artigo",
    "Live", "Podcast / Áudio",
]
REDES_DEFAULT = [
    "Instagram", "Facebook", "LinkedIn", "WhatsApp",
    "YouTube", "TikTok", "Site UNIVAJA", "Imprensa",
]
STATUS_DEFAULT = [
    "💡 Proposta", "✏️ Em produção", "⏳ Aguardando aprovação",
    "✅ Aprovado", "📤 Publicado", "🗄️ Arquivado",
]
PRIORIDADES_DEFAULT = ["🟢 Baixa", "🔵 Normal", "🟡 Alta", "🔴 Urgente"]
TEMAS_DEFAULT = [
    "Povos isolados",
    "Direitos indígenas / marco temporal",
    "Cultura e tradições dos povos",
    "Garimpo e invasão",
    "Bruno Pereira e Dom Phillips",
    "Saúde indígena",
    "Educação indígena",
    "Datas comemorativas",
    "Associações de base UNIVAJA",
    "Lideranças e protagonistas",
    "Mobilizações e assembleias",
    "FUNAI e políticas indigenistas",
    "Internacional / COP / Amazon Week",
    "Meio ambiente / desmatamento",
    "Denúncia (com orientação jurídica)",
    "Cobertura de evento",
    "Boletim informativo das aldeias",
    "Outro",
]

EMAIL_ASSUNTO_DEFAULT = "Pauta UNIVAJA pronta: {titulo}"
EMAIL_CORPO_DEFAULT = """Olá,

Segue pauta aprovada para publicação pela ASCOM UNIVAJA:

📌 Título: {titulo}
📅 Data prevista: {data} {horario}
🎯 Tema: {tema}
📝 Tipo: {tipo}
📡 Redes / canais: {redes}
👥 Público-alvo: {publico}
🎯 Objetivo: {objetivo}

👤 Responsável: {responsavel}
🎨 Designer / editor: {designer}
🚦 Prioridade: {prioridade}
📊 Status: {status}

📝 Briefing:
{briefing}

🏷️ Hashtags: {hashtags}
🔗 Links de referência: {links}

—
Enviado pelo Planner UNIVAJA · ASCOM"""

# ══════════════════════════════════════════════════════════════════════════════
#  ESTADO + CONFIGURAÇÕES (persistidas via JSON download/upload)
# ══════════════════════════════════════════════════════════════════════════════
if "config" not in st.session_state:
    st.session_state.config = {
        "tipos": TIPOS_DEFAULT.copy(),
        "redes": REDES_DEFAULT.copy(),
        "status": STATUS_DEFAULT.copy(),
        "prioridades": PRIORIDADES_DEFAULT.copy(),
        "temas": TEMAS_DEFAULT.copy(),
        "email_imprensa": "imprensa@univaja.org",
        "email_cc": "",
        "email_assunto": EMAIL_ASSUNTO_DEFAULT,
        "email_corpo": EMAIL_CORPO_DEFAULT,
    }

if "pautas" not in st.session_state:
    st.session_state.pautas = []
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

cfg = st.session_state.config


def tipos():        return cfg["tipos"]
def redes_list():   return cfg["redes"]
def status_list():  return cfg["status"]
def prioridades(): return cfg["prioridades"]
def temas():        return cfg["temas"] + (["Outro"] if "Outro" not in cfg["temas"] else [])


def nova_pauta_dict() -> dict:
    return {
        "id": str(uuid.uuid4())[:8],
        "data": date.today().isoformat(),
        "titulo": "",
        "tema": temas()[0] if temas() else "",
        "tema_custom": "",
        "tipo": tipos()[0] if tipos() else "",
        "redes": [redes_list()[0]] if redes_list() else [],
        "responsavel": "",
        "designer": "",
        "status": status_list()[0] if status_list() else "",
        "prioridade": prioridades()[1] if len(prioridades()) > 1 else (prioridades()[0] if prioridades() else ""),
        "horario": "",
        "publico": "",
        "objetivo": "",
        "briefing": "",
        "hashtags": "#UNIVAJA #ValeDoJavari #PovosIndígenas",
        "links": "",
        "email_enviado": False,
        "criado_em": datetime.now().isoformat(),
    }


def salvar_pauta(p: dict):
    idx = next((i for i, x in enumerate(st.session_state.pautas) if x["id"] == p["id"]), None)
    if idx is not None:
        st.session_state.pautas[idx] = p
    else:
        st.session_state.pautas.append(p)


def remover_pauta(pid: str):
    st.session_state.pautas = [p for p in st.session_state.pautas if p["id"] != pid]


def pauta_por_id(pid: str):
    return next((p for p in st.session_state.pautas if p["id"] == pid), None)


def tema_efetivo(p: dict) -> str:
    if p.get("tema") == "Outro" and p.get("tema_custom"):
        return p["tema_custom"]
    return p.get("tema", "")


def mailto_url(p: dict) -> str:
    """Gera link mailto com a pauta formatada via templates do config."""
    valores = {
        "titulo": p.get("titulo", ""),
        "data": p.get("data", ""),
        "horario": p.get("horario", ""),
        "tema": tema_efetivo(p),
        "tipo": p.get("tipo", ""),
        "redes": ", ".join(p.get("redes", [])),
        "publico": p.get("publico", "—"),
        "objetivo": p.get("objetivo", "—"),
        "responsavel": p.get("responsavel", "—"),
        "designer": p.get("designer", "—"),
        "prioridade": p.get("prioridade", ""),
        "status": p.get("status", ""),
        "briefing": p.get("briefing", "—"),
        "hashtags": p.get("hashtags", ""),
        "links": p.get("links", "—"),
    }
    try:
        assunto = cfg["email_assunto"].format(**valores)
        corpo = cfg["email_corpo"].format(**valores)
    except KeyError as ex:
        assunto = f"Pauta: {p.get('titulo','')}"
        corpo = f"Erro de template: variável {ex} não encontrada."

    destino = cfg["email_imprensa"]
    cc = cfg.get("email_cc", "").strip()
    extras = f"&cc={quote(cc)}" if cc else ""
    return f"mailto:{destino}?subject={quote(assunto)}&body={quote(corpo)}{extras}"


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — Filtros + Backup
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(sidebar_logo(), unsafe_allow_html=True)
    st.markdown("### 🔍 Filtros")

    filtro_responsavel = st.text_input("Responsável", placeholder="ex: Fran, Tumi, Débora")
    filtro_status = st.multiselect("Status", status_list(), default=[])
    filtro_redes = st.multiselect("Rede social", redes_list(), default=[])
    filtro_prioridade = st.multiselect("Prioridade", prioridades(), default=[])

    filtro_data_de = st.date_input("De", value=None, format="DD/MM/YYYY")
    filtro_data_ate = st.date_input("Até", value=None, format="DD/MM/YYYY")

    st.markdown("---")
    st.markdown("### 💾 Backup")
    st.caption("Salve um JSON com TODAS as pautas e configurações. Reimporte depois para continuar ou compartilhar com a equipe.")

    backup_obj = {"pautas": st.session_state.pautas, "config": cfg}
    export_json = json.dumps(backup_obj, ensure_ascii=False, indent=2)
    st.download_button(
        "📥 Baixar backup completo (JSON)",
        export_json,
        file_name=f"univaja_planner_{date.today().isoformat()}.json",
        mime="application/json",
        use_container_width=True,
    )

    arquivo = st.file_uploader("📤 Importar JSON", type=["json"], label_visibility="collapsed")
    if arquivo is not None:
        try:
            dados = json.loads(arquivo.read())

            # Aceita 2 formatos: {pautas, config} OU lista plana de pautas (compat legado)
            if isinstance(dados, list):
                pautas_in = dados
                config_in = None
            elif isinstance(dados, dict):
                pautas_in = dados.get("pautas", [])
                config_in = dados.get("config")
            else:
                pautas_in, config_in = [], None

            modo = st.radio("Como importar pautas?",
                            ["Adicionar às pautas atuais", "Substituir tudo"],
                            horizontal=False)
            substituir_config = st.checkbox(
                "Também substituir configurações (tipos, redes, email…)",
                value=True if config_in else False,
                disabled=config_in is None,
            )

            if st.button("Confirmar importação", type="primary"):
                if modo == "Substituir tudo":
                    st.session_state.pautas = pautas_in
                else:
                    ids = {p["id"] for p in st.session_state.pautas}
                    for p in pautas_in:
                        if p.get("id") not in ids:
                            st.session_state.pautas.append(p)
                if substituir_config and config_in:
                    st.session_state.config.update(config_in)
                st.success(f"✅ {len(pautas_in)} pauta(s) importada(s)!")
                st.rerun()
        except Exception as ex:
            st.error(f"Erro ao ler JSON: {ex}")

    st.markdown("---")
    if st.button("🗑️ Limpar todas as pautas", type="secondary"):
        if st.session_state.get("confirmar_limpar"):
            st.session_state.pautas = []
            st.session_state.confirmar_limpar = False
            st.rerun()
        else:
            st.session_state.confirmar_limpar = True
            st.warning("Clique de novo para confirmar.")


# ─── Aplicar filtros ─────────────────────────────────────────────────────────
def aplicar_filtros(pautas):
    out = pautas
    if filtro_responsavel:
        f = filtro_responsavel.lower()
        out = [p for p in out if f in (p.get("responsavel","") + " " + p.get("designer","")).lower()]
    if filtro_status:
        out = [p for p in out if p.get("status") in filtro_status]
    if filtro_redes:
        out = [p for p in out if any(r in p.get("redes", []) for r in filtro_redes)]
    if filtro_prioridade:
        out = [p for p in out if p.get("prioridade") in filtro_prioridade]
    if filtro_data_de:
        out = [p for p in out if p.get("data") and p["data"] >= filtro_data_de.isoformat()]
    if filtro_data_ate:
        out = [p for p in out if p.get("data") and p["data"] <= filtro_data_ate.isoformat()]
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  ABAS — "Como usar" em PRIMEIRO
# ══════════════════════════════════════════════════════════════════════════════
aba_h, aba_n, aba_l, aba_c, aba_k, aba_f, aba_r, aba_cfg = st.tabs([
    "ℹ️ Como usar",
    "➕ Nova pauta",
    "📋 Lista de pautas",
    "📅 Cronograma",
    "📊 Kanban (status)",
    "🔁 Fluxo de produção",
    "📄 Relatório PDF",
    "⚙️ Configurações",
])


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — COMO USAR
# ──────────────────────────────────────────────────────────────────────────────
with aba_h:
    st.markdown(section_title("Como usar o Planner", "padrao"), unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown(f"""
        ### 🎯 Para que serve
        O **Planner UNIVAJA** organiza todo o ciclo de planejamento editorial da ASCOM.
        Cada comunicador propõe pautas, define responsáveis, escolhe redes e monta o
        cronograma. No fim, o ponto focal gera um **PDF** para a reunião e dispara
        emails para a imprensa quando as pautas ficam prontas.

        ### 📋 Fluxo recomendado

        <div class="card card-vermelho">
            <strong style="color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">1. Antes da reunião — propor pautas</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Cada comunicador entra no Planner durante a semana, vai em <strong>➕ Nova pauta</strong> e propõe
            quantas pautas quiser. Define data, tema, tipo, redes e responsável.
            Status inicial: <strong>💡 Proposta</strong>.
            </p>
        </div>

        <div class="card card-verde">
            <strong style="color:{VERDE};text-transform:uppercase;letter-spacing:0.5px">2. Reunião de segunda — alinhamento</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Ponto focal abre as abas <strong>📅 Cronograma</strong> e <strong>📊 Kanban</strong>, debate as pautas,
            confirma responsáveis, ajusta datas e muda status para <strong>✏️ Em produção</strong> nas aprovadas.
            Em seguida, gera o <strong>📄 PDF</strong> da quinzena e envia para a coordenação.
            </p>
        </div>

        <div class="card card-azul">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">3. Durante a semana — produção</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Comunicadores acompanham suas pautas e atualizam o status conforme avançam:
            <strong>⏳ Aguardando aprovação</strong> → <strong>✅ Aprovado</strong> → <strong>📤 Publicado</strong>.
            Quando a pauta é aprovada, clicam em <strong>📧 Notificar imprensa</strong> para abrir um email
            preenchido para <code>{cfg['email_imprensa']}</code>.
            </p>
        </div>

        <div class="card card-cinza">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">4. Sexta — fechamento e backup</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Ponto focal baixa o JSON (sidebar) para guardar o histórico da semana.
            Pautas publicadas viram referência futura. Atrasos viram pauta da próxima reunião.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 💡 Dicas práticas")
        dicas = [
            ("💾 Backup é fundamental",
             "Este app guarda as pautas na memória do navegador. <strong>Baixe o JSON ao fim de cada uso</strong> na barra lateral."),
            ("🔄 Compartilhe o JSON",
             "Para trabalhar em equipe, exporte o JSON e envie no grupo ASCOM. Outros podem importar e ver as mesmas pautas."),
            ("🔍 Use os filtros",
             "Filtre por responsável, rede ou status. O PDF do relatório respeita os filtros ativos."),
            ("🚦 Prioridade urgente",
             "Use <strong>🔴 Urgente</strong> apenas para pautas que não podem esperar a próxima reunião (datas sensíveis, denúncias, coberturas)."),
            ("⚙️ Tudo é customizável",
             "Na aba <strong>⚙️ Configurações</strong> você pode editar tipos, redes, status, prioridades, temas e o template do email."),
            ("📧 Notificar imprensa",
             "Na aba <strong>📋 Lista</strong>, cada pauta tem um botão que abre seu cliente de email com tudo preenchido."),
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
#  ABA — NOVA PAUTA
# ──────────────────────────────────────────────────────────────────────────────
with aba_n:
    edit_mode = st.session_state.edit_id is not None
    pauta = pauta_por_id(st.session_state.edit_id) if edit_mode else nova_pauta_dict()
    if edit_mode and pauta is None:
        st.session_state.edit_id = None
        pauta = nova_pauta_dict()
        edit_mode = False

    titulo_aba = "Editar pauta" if edit_mode else "Propor nova pauta"
    st.markdown(section_title(titulo_aba, "vermelho" if edit_mode else "padrao"), unsafe_allow_html=True)

    if edit_mode:
        col_inf, col_cancel = st.columns([5, 1])
        with col_inf:
            st.markdown(f"""
            <div class="alerta alerta-azul">
                ✏️ Editando pauta <strong>{pauta.get('titulo') or '(sem título)'}</strong> — ID <code>{pauta['id']}</code>
            </div>
            """, unsafe_allow_html=True)
        with col_cancel:
            if st.button("Cancelar edição", use_container_width=True):
                st.session_state.edit_id = None
                st.rerun()

    with st.form("form_pauta", clear_on_submit=not edit_mode):

        col_t, col_d = st.columns([3, 1])
        with col_t:
            titulo = st.text_input("📌 Título da pauta *", value=pauta["titulo"],
                placeholder="ex: Cobertura assembleia Marubo / 3 anos Bruno e Dom")
        with col_d:
            data_str = pauta.get("data") or date.today().isoformat()
            data_dt = st.date_input("📅 Data prevista *", value=date.fromisoformat(data_str), format="DD/MM/YYYY")

        col_te, col_ti, col_pr = st.columns(3)
        with col_te:
            opcoes_temas = temas()
            idx_t = opcoes_temas.index(pauta["tema"]) if pauta["tema"] in opcoes_temas else 0
            tema = st.selectbox("🎯 Tema", opcoes_temas, index=idx_t)
            tema_custom = ""
            if tema == "Outro":
                tema_custom = st.text_input("Especifique o tema",
                    value=pauta.get("tema_custom",""),
                    placeholder="ex: Festival Yoxin")
        with col_ti:
            opcoes_tipos = tipos()
            idx_ti = opcoes_tipos.index(pauta["tipo"]) if pauta["tipo"] in opcoes_tipos else 0
            tipo = st.selectbox("📝 Tipo de material", opcoes_tipos, index=idx_ti)
        with col_pr:
            opcoes_pri = prioridades()
            idx_pr = opcoes_pri.index(pauta["prioridade"]) if pauta["prioridade"] in opcoes_pri else (1 if len(opcoes_pri) > 1 else 0)
            prioridade = st.selectbox("🚦 Prioridade", opcoes_pri, index=idx_pr)

        col_re, col_ho = st.columns([3, 1])
        with col_re:
            redes = st.multiselect("📡 Redes sociais / canais *", redes_list(),
                default=[r for r in pauta.get("redes", []) if r in redes_list()] or ([redes_list()[0]] if redes_list() else []))
        with col_ho:
            horario = st.text_input("🕐 Horário (opcional)", value=pauta.get("horario",""),
                placeholder="ex: 09h00")

        col_r1, col_r2, col_st = st.columns(3)
        with col_r1:
            responsavel = st.text_input("👤 Responsável (comunicador) *",
                value=pauta.get("responsavel",""), placeholder="ex: Fran, Tumi, Pixi Matis")
        with col_r2:
            designer = st.text_input("🎨 Designer / editor (se aplicável)",
                value=pauta.get("designer",""), placeholder="ex: João Marubo")
        with col_st:
            opcoes_st = status_list()
            idx_st = opcoes_st.index(pauta["status"]) if pauta["status"] in opcoes_st else 0
            status = st.selectbox("📊 Status", opcoes_st, index=idx_st)

        col_pu, col_ob = st.columns(2)
        with col_pu:
            publico = st.text_input("👥 Público-alvo", value=pauta.get("publico",""),
                placeholder="ex: aldeias / imprensa / parceiros internacionais")
        with col_ob:
            objetivo = st.text_input("🎯 Objetivo da publicação", value=pauta.get("objetivo",""),
                placeholder="ex: informar / denunciar / celebrar / mobilizar")

        briefing = st.text_area("📝 Briefing (o que o card/vídeo deve comunicar)",
            value=pauta.get("briefing",""),
            placeholder="Descreva o que o material deve dizer, referências visuais, falas, dados a destacar...",
            height=120)

        col_h, col_l = st.columns(2)
        with col_h:
            hashtags = st.text_input("🏷️ Hashtags",
                value=pauta.get("hashtags", "#UNIVAJA #ValeDoJavari #PovosIndígenas"))
        with col_l:
            links = st.text_input("🔗 Links de referência", value=pauta.get("links",""),
                placeholder="ex: matéria base, foto de referência, contato fonte")

        st.markdown("")
        col_ok, col_dup = st.columns([1, 1])
        with col_ok:
            submeter = st.form_submit_button(
                "💾 Salvar pauta" if edit_mode else "➕ Adicionar pauta",
                type="primary", use_container_width=True)
        with col_dup:
            duplicar = st.form_submit_button("📋 Salvar como cópia", use_container_width=True) if edit_mode else False

        if submeter or duplicar:
            erros = []
            if not titulo.strip(): erros.append("Título é obrigatório.")
            if not responsavel.strip(): erros.append("Responsável é obrigatório.")
            if not redes: erros.append("Selecione ao menos uma rede social / canal.")

            if erros:
                for e in erros: st.error(f"⚠️ {e}")
            else:
                nova = pauta.copy() if edit_mode else nova_pauta_dict()
                if duplicar:
                    nova["id"] = str(uuid.uuid4())[:8]
                    nova["criado_em"] = datetime.now().isoformat()
                    nova["email_enviado"] = False

                nova.update({
                    "data": data_dt.isoformat(),
                    "titulo": titulo.strip(),
                    "tema": tema,
                    "tema_custom": tema_custom.strip(),
                    "tipo": tipo,
                    "redes": redes,
                    "responsavel": responsavel.strip(),
                    "designer": designer.strip(),
                    "status": status,
                    "prioridade": prioridade,
                    "horario": horario.strip(),
                    "publico": publico.strip(),
                    "objetivo": objetivo.strip(),
                    "briefing": briefing.strip(),
                    "hashtags": hashtags.strip(),
                    "links": links.strip(),
                })

                salvar_pauta(nova)
                if edit_mode and not duplicar:
                    st.session_state.edit_id = None
                    st.success("✅ Pauta atualizada!")
                else:
                    st.success("✅ Pauta adicionada ao planejamento!")
                st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — LISTA DE PAUTAS
# ──────────────────────────────────────────────────────────────────────────────
with aba_l:
    st.markdown(section_title("Lista de pautas", "padrao"), unsafe_allow_html=True)

    pautas_filt = aplicar_filtros(st.session_state.pautas)
    pautas_filt.sort(key=lambda p: (p.get("data") or "", p.get("horario") or ""))

    if not st.session_state.pautas:
        st.markdown("""
        <div class="alerta">
            📭 Nenhuma pauta criada ainda. Vá à aba <strong>➕ Nova pauta</strong> para começar.
        </div>
        """, unsafe_allow_html=True)
    elif not pautas_filt:
        st.markdown("""
        <div class="alerta">
            🔍 Nenhuma pauta corresponde aos filtros atuais. Ajuste os filtros na barra lateral.
        </div>
        """, unsafe_allow_html=True)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{len(pautas_filt)}</div>
                <div class="stat-label">Pautas filtradas</div></div>""", unsafe_allow_html=True)
        with col2:
            urgentes = sum(1 for p in pautas_filt if "Urgente" in p.get("prioridade",""))
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{urgentes}</div>
                <div class="stat-label">Urgentes</div></div>""", unsafe_allow_html=True)
        with col3:
            em_prod = sum(1 for p in pautas_filt if "produção" in p.get("status","") or "aprovação" in p.get("status",""))
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{em_prod}</div>
                <div class="stat-label">Em produção</div></div>""", unsafe_allow_html=True)
        with col4:
            publicados = sum(1 for p in pautas_filt if "Publicado" in p.get("status",""))
            st.markdown(f"""<div class="stat-card"><div class="stat-num">{publicados}</div>
                <div class="stat-label">Publicados</div></div>""", unsafe_allow_html=True)

        st.markdown(divisor("zig"), unsafe_allow_html=True)

        for p in pautas_filt:
            cor_pri = {
                "🟢 Baixa": VERDE_CLARO, "🔵 Normal": VERDE,
                "🟡 Alta": VERMELHO_MED, "🔴 Urgente": PRIMARIA,
            }.get(p.get("prioridade",""), VERDE)

            try:
                data_fmt = datetime.fromisoformat(p["data"]).strftime("%d/%m/%Y (%a)")
            except Exception:
                data_fmt = p.get("data","")

            redes_str = " · ".join(p.get("redes", []))
            tema_str = tema_efetivo(p)
            badge_email = '<span class="badge badge-pos">✉️ Notificada</span>' if p.get("email_enviado") else ""

            st.markdown(f"""
            <div class="card" style="border-left:5px solid {cor_pri};margin-bottom:8px">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
                    <div style="flex:1;min-width:280px">
                        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px">
                            <span class="badge badge-perm">{p.get('prioridade','')}</span>
                            <span class="badge badge-pol">{p.get('status','')}</span>
                            <span class="badge badge-int">{p.get('tipo','')}</span>
                            {badge_email}
                        </div>
                        <div style="font-weight:700;font-size:16px;color:{VERDE_PRETO};margin-bottom:4px">{p.get('titulo','(sem título)')}</div>
                        <div style="font-size:13px;color:{CINZA};margin-bottom:6px">
                            🎯 <strong>{tema_str}</strong> · 📡 {redes_str}
                        </div>
                        <div style="font-size:12px;color:#6b7280">
                            📅 {data_fmt} {('· 🕐 ' + p.get('horario','')) if p.get('horario') else ''}
                            · 👤 {p.get('responsavel','—')}
                            {('· 🎨 ' + p.get('designer','')) if p.get('designer') else ''}
                        </div>
                        {f'<div style="font-size:12px;color:{CINZA};margin-top:8px;font-style:italic">📝 {p.get("briefing","")[:200]}{"..." if len(p.get("briefing","")) > 200 else ""}</div>' if p.get('briefing') else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_e, col_d, col_m, col_id = st.columns([1, 1, 2, 3])
            with col_e:
                if st.button("✏️ Editar", key=f"edit_{p['id']}", use_container_width=True):
                    st.session_state.edit_id = p["id"]
                    st.rerun()
            with col_d:
                if st.button("🗑️ Remover", key=f"del_{p['id']}", use_container_width=True):
                    remover_pauta(p["id"])
                    st.rerun()
            with col_m:
                url = mailto_url(p)
                st.markdown(f"""
                <a href="{url}" target="_blank" style="display:block;background:{PRIMARIA};color:white;text-align:center;padding:6px 10px;border-radius:6px;text-decoration:none;font-weight:600;font-size:13px"
                   onclick="setTimeout(()=>{{window.parent.postMessage({{type:'email_sent','id':'{p['id']}'}},'*')}},500)">
                   📧 Notificar imprensa
                </a>
                """, unsafe_allow_html=True)
                if st.button("✓ Marcar como notificada", key=f"mark_{p['id']}", use_container_width=True):
                    p["email_enviado"] = True
                    salvar_pauta(p)
                    st.rerun()
            with col_id:
                st.caption(f"ID: {p['id']} · email: {cfg['email_imprensa']}")


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — CRONOGRAMA
# ──────────────────────────────────────────────────────────────────────────────
with aba_c:
    st.markdown(section_title("Cronograma de postagens", "verde"), unsafe_allow_html=True)
    st.caption("Pautas agrupadas por data. Use para visualizar a distribuição semanal e identificar lacunas.")

    pautas_filt = aplicar_filtros(st.session_state.pautas)

    if not pautas_filt:
        st.markdown("""
        <div class="alerta">
            📭 Nenhuma pauta para mostrar. Adicione pautas na aba <strong>➕ Nova pauta</strong>.
        </div>
        """, unsafe_allow_html=True)
    else:
        por_data = {}
        for p in pautas_filt:
            d = p.get("data") or "sem-data"
            por_data.setdefault(d, []).append(p)

        for d in sorted(por_data.keys()):
            try:
                dt = datetime.fromisoformat(d)
                dias_pt = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
                meses_pt = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
                dia_fmt = f"{dt.day:02d} {meses_pt[dt.month-1]} · {dias_pt[dt.weekday()]}"
                hoje = date.today()
                delta = (dt.date() - hoje).days
                if delta == 0: selo, cor_selo = "HOJE", PRIMARIA
                elif delta == 1: selo, cor_selo = "AMANHÃ", VERMELHO_MED
                elif delta < 0: selo, cor_selo = f"há {-delta} dia(s)", CINZA
                elif delta <= 7: selo, cor_selo = f"em {delta} dia(s)", VERDE
                else: selo, cor_selo = f"em {delta} dias", VERDE_ESC
            except Exception:
                dia_fmt, selo, cor_selo = d, "", CINZA

            st.markdown(f"""
            <div style="background:{VERDE_PRETO};color:white;padding:10px 18px;border-radius:8px;margin:14px 0 8px;display:flex;justify-content:space-between;align-items:center">
                <div style="font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:1px">📅 {dia_fmt}</div>
                <span style="background:{cor_selo};padding:3px 12px;border-radius:12px;font-size:11px;font-weight:700;letter-spacing:0.5px">{selo}</span>
            </div>
            """, unsafe_allow_html=True)

            for p in sorted(por_data[d], key=lambda x: x.get("horario") or ""):
                cor_pri = {
                    "🟢 Baixa": VERDE_CLARO, "🔵 Normal": VERDE,
                    "🟡 Alta": VERMELHO_MED, "🔴 Urgente": PRIMARIA,
                }.get(p.get("prioridade",""), VERDE)
                redes_pills = "".join([f'<span class="termo-pill" style="font-size:11px">{r}</span>' for r in p.get("redes",[])])

                st.markdown(f"""
                <div class="card" style="border-left:5px solid {cor_pri};margin-bottom:6px;padding:12px 16px">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
                        <div style="flex:1;min-width:260px">
                            <div style="font-weight:700;font-size:14px;color:{VERDE_PRETO}">
                                {('🕐 ' + p.get('horario','') + ' · ') if p.get('horario') else ''}{p.get('titulo','(sem título)')}
                            </div>
                            <div style="font-size:12px;color:{CINZA};margin-top:4px">
                                🎯 {tema_efetivo(p)} · 📝 {p.get('tipo','')} · 👤 {p.get('responsavel','—')}
                            </div>
                            <div style="margin-top:6px">{redes_pills}</div>
                        </div>
                        <div style="text-align:right;font-size:11px;color:#6b7280">
                            <div>{p.get('status','')}</div>
                            <div style="margin-top:2px">{p.get('prioridade','')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — KANBAN
# ──────────────────────────────────────────────────────────────────────────────
with aba_k:
    st.markdown(section_title("Quadro Kanban — por status", "padrao"), unsafe_allow_html=True)
    st.caption("Visualize as pautas pelo estágio de produção. Edite pelo botão na aba Lista.")

    pautas_filt = aplicar_filtros(st.session_state.pautas)
    sts = status_list()

    if not pautas_filt:
        st.markdown("""
        <div class="alerta">📭 Nenhuma pauta para mostrar.</div>
        """, unsafe_allow_html=True)
    else:
        # divide em linhas de 3
        for i0 in range(0, len(sts), 3):
            cols = st.columns(3)
            for i, status in enumerate(sts[i0:i0+3]):
                pautas_status = [p for p in pautas_filt if p.get("status") == status]
                with cols[i]:
                    cor = {
                        "💡 Proposta": VERDE_CLARO, "✏️ Em produção": VERDE,
                        "⏳ Aguardando aprovação": VERMELHO_MED, "✅ Aprovado": VERDE_ESC,
                        "📤 Publicado": PRIMARIA, "🗄️ Arquivado": CINZA,
                    }.get(status, VERDE)

                    st.markdown(f"""
                    <div style="background:{cor};color:white;padding:8px 14px;border-radius:8px;margin-bottom:8px;font-weight:700;font-size:13px;text-align:center;letter-spacing:0.5px">
                        {status}<br>
                        <span style="font-size:11px;opacity:.9;font-weight:500">{len(pautas_status)} pauta(s)</span>
                    </div>
                    """, unsafe_allow_html=True)

                    if not pautas_status:
                        st.markdown(f"""
                        <div style="background:white;border:1px dashed #d1d5db;border-radius:8px;padding:14px;text-align:center;font-size:12px;color:#9ca3af;margin-bottom:6px">
                            (vazio)
                        </div>
                        """, unsafe_allow_html=True)

                    for p in pautas_status:
                        try:
                            data_fmt = datetime.fromisoformat(p["data"]).strftime("%d/%m")
                        except Exception:
                            data_fmt = p.get("data","")
                        redes_str = " · ".join(p.get("redes", [])[:3])

                        st.markdown(f"""
                        <div style="background:white;border:1px solid #e5e7eb;border-left:3px solid {cor};border-radius:6px;padding:10px 12px;margin-bottom:6px">
                            <div style="font-weight:600;font-size:12px;color:{VERDE_PRETO};line-height:1.3;margin-bottom:4px">{p.get('titulo','(sem título)')[:80]}</div>
                            <div style="font-size:10px;color:{CINZA}">
                                📅 {data_fmt} · 👤 {p.get('responsavel','—')}<br>
                                📡 {redes_str}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — FLUXO DE PRODUÇÃO
# ──────────────────────────────────────────────────────────────────────────────
def etapa_fluxo(pauta: dict) -> str:
    """Mapeia o status da pauta para uma etapa do fluxo de publicação."""
    st_atual = pauta.get("status", "")
    if "Proposta" in st_atual:                     return "1"
    if "produção" in st_atual:                     return "3"
    if "Aguardando" in st_atual:                   return "5"
    if "Aprovado" in st_atual:                     return "6"
    if "Publicado" in st_atual:                    return "7"
    if "Arquivado" in st_atual:                    return "7"
    return "1"


ETAPAS_FLUXO_CARD = [
    {"num": "1", "titulo": "Proposta",   "responsavel": "Comunicador designado",   "entrega": "Tema na reunião",       "cor": VERDE},
    {"num": "2", "titulo": "Briefing",   "responsavel": "Comunicador → Designer",  "entrega": "Briefing no grupo",     "cor": VERDE},
    {"num": "3", "titulo": "Design",     "responsavel": "Designer",                "entrega": "Card finalizado",       "cor": VERDE},
    {"num": "4", "titulo": "Legenda",    "responsavel": "Comunicador responsável", "entrega": "Texto + hashtags",      "cor": VERDE},
    {"num": "5", "titulo": "Aprovação",  "responsavel": "Ponto focal → Coordenação", "entrega": "Aprovação registrada","cor": VERMELHO_MED},
    {"num": "6", "titulo": "Aprovado",   "responsavel": "Coordenação ASCOM",       "entrega": "Pronto para publicar",  "cor": VERDE_ESC},
    {"num": "7", "titulo": "Publicação", "responsavel": "TUMI / DÉBORA",           "entrega": "✅ Publicado nas redes","cor": PRIMARIA},
]


with aba_f:
    st.markdown(section_title("Fluxo de produção das pautas", "verde"), unsafe_allow_html=True)
    st.caption("Visualize cada pauta no estágio em que ela está dentro do fluxo de publicação da ASCOM.")

    st.markdown("##### 📊 Etapas do fluxo")
    st.markdown(flow_kanban(ETAPAS_FLUXO_CARD), unsafe_allow_html=True)

    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown("##### 📌 Suas pautas em cada etapa")

    pautas_filt = aplicar_filtros(st.session_state.pautas)

    if not pautas_filt:
        st.markdown("""
        <div class="alerta">📭 Nenhuma pauta para mostrar.</div>
        """, unsafe_allow_html=True)
    else:
        # Distribui pautas pelas etapas
        por_etapa = {e["num"]: [] for e in ETAPAS_FLUXO_CARD}
        for p in pautas_filt:
            por_etapa[etapa_fluxo(p)].append(p)

        # Exibe etapas em 3 linhas de até 3 colunas
        for i0 in range(0, len(ETAPAS_FLUXO_CARD), 3):
            cols = st.columns(min(3, len(ETAPAS_FLUXO_CARD) - i0))
            for ci, etapa in enumerate(ETAPAS_FLUXO_CARD[i0:i0+3]):
                pautas_etapa = por_etapa[etapa["num"]]
                with cols[ci]:
                    st.markdown(f"""
                    <div style="background:{etapa['cor']};color:white;padding:10px 14px;border-radius:8px;margin-bottom:8px;font-weight:700;text-align:center;letter-spacing:0.5px">
                        <div style="font-size:11px;opacity:.9;text-transform:uppercase">Etapa {etapa['num']}</div>
                        <div style="font-size:14px;margin-top:2px">{etapa['titulo']}</div>
                        <div style="font-size:11px;opacity:.9;font-weight:500;margin-top:4px">{len(pautas_etapa)} pauta(s)</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if not pautas_etapa:
                        st.markdown("""
                        <div style="background:white;border:1px dashed #d1d5db;border-radius:8px;padding:14px;text-align:center;font-size:12px;color:#9ca3af;margin-bottom:6px">
                            (sem pautas nesta etapa)
                        </div>
                        """, unsafe_allow_html=True)

                    for p in pautas_etapa:
                        try:
                            data_fmt = datetime.fromisoformat(p["data"]).strftime("%d/%m")
                        except Exception:
                            data_fmt = p.get("data","")
                        redes_str = " · ".join(p.get("redes", [])[:2])
                        st.markdown(f"""
                        <div style="background:white;border:1px solid #e5e7eb;border-left:3px solid {etapa['cor']};border-radius:6px;padding:10px 12px;margin-bottom:6px">
                            <div style="font-weight:600;font-size:12px;color:{VERDE_PRETO};line-height:1.3;margin-bottom:4px">{p.get('titulo','(sem título)')[:70]}</div>
                            <div style="font-size:10px;color:{CINZA}">
                                📅 {data_fmt} · 👤 {p.get('responsavel','—')}<br>
                                📡 {redes_str}<br>
                                <span style="color:#9ca3af">{p.get('status','')}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — RELATÓRIO PDF
# ──────────────────────────────────────────────────────────────────────────────
def gerar_pdf(pautas: list, titulo_reuniao: str, periodo_descr: str, observacoes: str) -> bytes:
    def hex_rgb(h: str):
        h = h.lstrip("#")
        return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    def latin(s: str) -> str:
        return (s or "").encode("latin-1", "replace").decode("latin-1")

    def divisor_zig(y, cor=PRIMARIA):
        r, g, b = hex_rgb(cor)
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(0.5)
        x = 10; up = True
        while x < 200:
            pdf.line(x, y+(0 if up else 3), x+4, y+(3 if up else 0))
            up = not up; x += 4

    def pontos_kanamari(y, cor=PRIMARIA):
        r, g, b = hex_rgb(cor)
        pdf.set_fill_color(r, g, b)
        x = 10
        while x < 200:
            pdf.ellipse(x, y, 1.2, 1.2, "F")
            pdf.ellipse(x+6, y, 1.2, 1.2, "F")
            x += 12

    # HEADER
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

    # ── LOGO UNIVAJA — desenhada com primitives (compatível com fpdf2 e PyFPDF) ──
    cx, cy = 22, 22

    # Círculo branco principal
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*hex_rgb(VERMELHO_ESC))
    pdf.set_line_width(0.4)
    raio = 12
    pdf.ellipse(cx-raio, cy-raio, raio*2, raio*2, "FD")

    # Maloca como pirâmide vermelha (retângulos empilhados)
    pdf.set_fill_color(*hex_rgb(PRIMARIA))
    pdf.rect(cx-1.0, cy-8, 2.0, 1.8, "F")
    pdf.rect(cx-2.4, cy-6.2, 4.8, 1.8, "F")
    pdf.rect(cx-3.8, cy-4.4, 7.6, 1.8, "F")
    pdf.rect(cx-5.2, cy-2.6, 10.4, 1.8, "F")
    pdf.rect(cx-6.6, cy-0.8, 13.2, 2.0, "F")

    # Solo vermelho escuro (faixa)
    pdf.set_fill_color(*hex_rgb(VERMELHO_ESC))
    pdf.rect(cx-7.5, cy+1.4, 15, 0.8, "F")

    # Base verde escuro com greca Marubo
    pdf.set_fill_color(*hex_rgb(VERDE_PRETO))
    pdf.rect(cx-7.5, cy+2.2, 15, 5.0, "F")

    # Greca Marubo branca dentro da base
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.35)
    bx = cx - 6.5
    for _ in range(3):
        pdf.line(bx, cy+6.5, bx, cy+3.5)
        pdf.line(bx, cy+3.5, bx+1.6, cy+3.5)
        pdf.line(bx+1.6, cy+3.5, bx+1.6, cy+5.5)
        pdf.line(bx+1.6, cy+5.5, bx+3.2, cy+5.5)
        pdf.line(bx+3.2, cy+5.5, bx+3.2, cy+3.5)
        bx += 4.5

    # Ponto vermelho topo (jacamim)
    pdf.set_fill_color(*hex_rgb(PRIMARIA))
    pdf.ellipse(cx-1.0, cy-10.5, 2.0, 2.0, "F")

    # Texto ao lado da logo
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 22)
    pdf.set_xy(40, 11)
    pdf.cell(0, 8, latin("UNIVAJA"), ln=1)
    pdf.set_font("helvetica", "", 9)
    pdf.set_x(40)
    pdf.cell(0, 4, latin("UNIAO DOS POVOS DO VALE DO JAVARI"), ln=1)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_x(40)
    pdf.cell(0, 5, latin("Planejamento editorial - ASCOM"), ln=1)
    pdf.set_font("helvetica", "I", 8)
    pdf.set_x(40)
    pdf.cell(0, 4, latin(f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"), ln=1)

    # Pontos brancos Kanamari na base do header
    pdf.set_fill_color(255, 255, 255)
    x = 10
    while x < 200:
        pdf.ellipse(x, 37, 0.8, 0.8, "F")
        pdf.ellipse(x+4, 37, 0.8, 0.8, "F")
        x += 8

    pdf.set_y(50)

    # TÍTULO
    r, g, b = hex_rgb(VERDE_PRETO)
    pdf.set_text_color(r, g, b)
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 8, latin(titulo_reuniao), ln=1, align="L")
    pdf.set_font("helvetica", "", 10)
    r, g, b = hex_rgb(CINZA)
    pdf.set_text_color(r, g, b)
    pdf.cell(0, 5, latin(periodo_descr), ln=1)
    pdf.ln(2)
    divisor_zig(pdf.get_y(), PRIMARIA)
    pdf.ln(6)

    # RESUMO
    r, g, b = hex_rgb(VERDE_PRETO)
    pdf.set_text_color(r, g, b)
    pdf.set_font("helvetica", "B", 13)
    pdf.cell(0, 7, latin("Resumo geral"), ln=1)
    pdf.set_font("helvetica", "", 10)
    r, g, b = hex_rgb(CINZA)
    pdf.set_text_color(r, g, b)

    total = len(pautas)
    por_status, por_rede, por_resp, por_prio = {}, {}, {}, {}
    for p in pautas:
        por_status[p.get("status","")] = por_status.get(p.get("status",""), 0) + 1
        por_prio[p.get("prioridade","")] = por_prio.get(p.get("prioridade",""), 0) + 1
        por_resp[p.get("responsavel","—")] = por_resp.get(p.get("responsavel","—"), 0) + 1
        for r2 in p.get("redes", []):
            por_rede[r2] = por_rede.get(r2, 0) + 1

    pdf.cell(0, 6, latin(f"  • Total de pautas: {total}"), ln=1)
    for label, mapa in [("Prioridade", por_prio), ("Status", por_status),
                       ("Redes/canais", por_rede), ("Por responsavel", por_resp)]:
        if mapa:
            txt = f"  • {label}: " + ", ".join([f"{k} ({v})" for k, v in mapa.items()])
            pdf.multi_cell(0, 6, latin(txt))

    pdf.ln(3)
    pontos_kanamari(pdf.get_y(), PRIMARIA)
    pdf.ln(5)

    # OBSERVAÇÕES
    if observacoes.strip():
        r, g, b = hex_rgb(VERDE_PRETO)
        pdf.set_text_color(r, g, b)
        pdf.set_font("helvetica", "B", 13)
        pdf.cell(0, 7, latin("Observações da reunião"), ln=1)
        r, g, b = hex_rgb(CINZA)
        pdf.set_text_color(r, g, b)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 5, latin(observacoes))
        pdf.ln(3)

    divisor_zig(pdf.get_y(), VERDE)
    pdf.ln(6)
    r, g, b = hex_rgb(VERDE_PRETO)
    pdf.set_text_color(r, g, b)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 8, latin("Pautas detalhadas"), ln=1)
    pdf.ln(2)

    pautas_sorted = sorted(pautas, key=lambda p: (p.get("data") or "", p.get("horario") or ""))
    por_data_g = {}
    for p in pautas_sorted:
        por_data_g.setdefault(p.get("data") or "sem-data", []).append(p)

    for d, lista in por_data_g.items():
        if pdf.get_y() > 250: pdf.add_page()
        try:
            dt = datetime.fromisoformat(d)
            dias_pt = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
            dia_fmt = f"{dt.strftime('%d/%m/%Y')} - {dias_pt[dt.weekday()]}"
        except Exception:
            dia_fmt = d

        r, g, b = hex_rgb(VERDE_PRETO)
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 7, latin(f"  {dia_fmt}"), ln=1, fill=True)
        pdf.ln(1)

        for p in lista:
            if pdf.get_y() > 260: pdf.add_page()

            cor_pri = {
                "🟢 Baixa": VERDE_CLARO, "🔵 Normal": VERDE,
                "🟡 Alta": VERMELHO_MED, "🔴 Urgente": PRIMARIA,
            }.get(p.get("prioridade",""), VERDE)

            y_ini = pdf.get_y()

            r, g, b = hex_rgb(VERDE_PRETO)
            pdf.set_text_color(r, g, b)
            pdf.set_font("helvetica", "B", 11)
            pdf.set_x(14)
            titulo_full = p.get("titulo","(sem titulo)")
            if p.get("horario"): titulo_full = f"[{p['horario']}] {titulo_full}"
            pdf.multi_cell(0, 6, latin(titulo_full))

            r, g, b = hex_rgb(CINZA)
            pdf.set_text_color(r, g, b)
            pdf.set_font("helvetica", "", 9)
            meta = f"Tema: {tema_efetivo(p)}  |  Tipo: {p.get('tipo','')}  |  Status: {p.get('status','')}  |  Prioridade: {p.get('prioridade','')}"
            pdf.set_x(14); pdf.multi_cell(0, 4.5, latin(meta))

            pdf.set_x(14); pdf.multi_cell(0, 4.5, latin(f"Redes/canais: {', '.join(p.get('redes',[])) or '—'}"))

            resp_txt = f"Responsavel: {p.get('responsavel','—')}"
            if p.get("designer"): resp_txt += f"  |  Designer/editor: {p.get('designer')}"
            pdf.set_x(14); pdf.multi_cell(0, 4.5, latin(resp_txt))

            if p.get("publico"):
                pdf.set_x(14); pdf.multi_cell(0, 4.5, latin(f"Publico: {p['publico']}"))
            if p.get("objetivo"):
                pdf.set_x(14); pdf.multi_cell(0, 4.5, latin(f"Objetivo: {p['objetivo']}"))
            if p.get("briefing"):
                pdf.set_x(14); pdf.set_font("helvetica", "I", 9)
                pdf.multi_cell(0, 4.5, latin(f"Briefing: {p['briefing']}"))
            if p.get("hashtags"):
                pdf.set_x(14); pdf.set_font("helvetica", "", 9)
                pdf.multi_cell(0, 4.5, latin(f"Hashtags: {p['hashtags']}"))
            if p.get("links"):
                pdf.set_x(14); pdf.multi_cell(0, 4.5, latin(f"Links: {p['links']}"))

            y_fim = pdf.get_y()
            r, g, b = hex_rgb(cor_pri)
            pdf.set_fill_color(r, g, b)
            pdf.rect(10, y_ini, 1.5, max(y_fim - y_ini, 4), "F")
            pdf.ln(3)

        pdf.ln(2)

    pdf.set_y(-22)
    divisor_zig(pdf.get_y(), PRIMARIA)
    pdf.ln(3)
    r, g, b = hex_rgb(CINZA)
    pdf.set_text_color(r, g, b)
    pdf.set_font("helvetica", "I", 8)
    pdf.cell(0, 4, latin("Planner UNIVAJA - ASCOM 2026 - documento de uso interno"), align="C", ln=1)
    pdf.cell(0, 4, latin("Identidade visual baseada no Manual de Marca UNIVAJA"), align="C", ln=1)

    result = pdf.output(dest="S")
    if isinstance(result, str):
        return result.encode("latin-1", "replace")
    return bytes(result)


with aba_r:
    st.markdown(section_title("Relatório PDF para a reunião", "vermelho"), unsafe_allow_html=True)
    st.caption("Configure as informações de capa, escolha as pautas (use os filtros na barra lateral) e baixe o PDF.")

    col_t, col_p = st.columns(2)
    with col_t:
        titulo_rel = st.text_input("Título do relatório",
            value=f"Reunião ASCOM — {date.today().strftime('%d/%m/%Y')}")
    with col_p:
        periodo_rel = st.text_input("Período / contexto",
            value="Pautas propostas para a próxima semana")

    observ = st.text_area("Observações para a reunião (opcional)",
        placeholder="Pontos a debater, alertas, dependências, decisões pendentes...", height=100)

    pautas_filt = aplicar_filtros(st.session_state.pautas)

    st.markdown(divisor("pontos"), unsafe_allow_html=True)

    col_q, col_b = st.columns([1, 1])
    with col_q:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-num">{len(pautas_filt)}</div>
            <div class="stat-label">Pautas no PDF</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Ajuste os filtros na barra lateral para incluir/excluir pautas.")
    with col_b:
        if pautas_filt:
            try:
                pdf_bytes = gerar_pdf(pautas_filt, titulo_rel, periodo_rel, observ)
                st.download_button("📄 Baixar relatório PDF", pdf_bytes,
                    file_name=f"pautas_univaja_{date.today().isoformat()}.pdf",
                    mime="application/pdf", type="primary", use_container_width=True)
                st.success("✅ PDF pronto — clique para baixar.")
            except Exception as ex:
                st.error(f"Erro ao gerar PDF: {ex}")
        else:
            st.markdown("""
            <div class="alerta">
                ⚠️ Nenhuma pauta para incluir. Adicione pautas ou ajuste os filtros.
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
#  ABA — CONFIGURAÇÕES
# ──────────────────────────────────────────────────────────────────────────────
with aba_cfg:
    st.markdown(section_title("Configurações da plataforma", "padrao"), unsafe_allow_html=True)
    st.caption("Tudo é customizável. As listas afetam todos os formulários. Salve o backup na sidebar para preservar suas configurações.")

    st.markdown(f"""
    <div class="alerta alerta-azul">
        💡 <strong>Como editar listas:</strong> coloque um item por linha.
        Os emojis no início são opcionais mas ajudam a destacar visualmente.
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 📝 Tipos de material")
        tipos_txt = st.text_area("Um por linha",
            value="\n".join(cfg["tipos"]), height=200, key="cfg_tipos",
            label_visibility="collapsed")

        st.markdown("#### 📡 Redes sociais / canais")
        redes_txt = st.text_area("Um por linha",
            value="\n".join(cfg["redes"]), height=180, key="cfg_redes",
            label_visibility="collapsed")

        st.markdown("#### 🚦 Prioridades")
        pri_txt = st.text_area("Um por linha (do menor para o maior)",
            value="\n".join(cfg["prioridades"]), height=120, key="cfg_pri",
            label_visibility="collapsed")

    with col_b:
        st.markdown("#### 📊 Status do fluxo")
        st.caption("Recomendado: na ordem do fluxo (Proposta → Publicado → Arquivado).")
        status_txt = st.text_area("Um por linha (ordem do fluxo)",
            value="\n".join(cfg["status"]), height=180, key="cfg_status",
            label_visibility="collapsed")

        st.markdown("#### 🎯 Temas sugeridos")
        st.caption("Mostrados como sugestões em 'Tema' no formulário. O usuário ainda pode escolher 'Outro' e digitar livremente.")
        temas_txt = st.text_area("Um por linha",
            value="\n".join([t for t in cfg["temas"] if t != "Outro"]),
            height=260, key="cfg_temas", label_visibility="collapsed")

    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown("#### 📧 Email para a imprensa")
    st.caption("Quando você clicar em 'Notificar imprensa' em uma pauta, abre seu cliente de email com tudo preenchido.")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        email_imp = st.text_input("Destinatário principal", value=cfg["email_imprensa"],
            placeholder="imprensa@univaja.org")
    with col_e2:
        email_cc = st.text_input("Cópia (CC) — opcional", value=cfg.get("email_cc",""),
            placeholder="ascom@univaja.org, fran@univaja.org")

    email_assunto = st.text_input("Modelo do assunto",
        value=cfg["email_assunto"],
        help="Use {titulo}, {data}, {tema}, etc. — os campos da pauta.")

    email_corpo = st.text_area("Modelo do corpo do email",
        value=cfg["email_corpo"], height=300,
        help="Use {titulo}, {data}, {horario}, {tema}, {tipo}, {redes}, {publico}, {objetivo}, {responsavel}, {designer}, {prioridade}, {status}, {briefing}, {hashtags}, {links}")

    with st.expander("📋 Variáveis disponíveis no template"):
        st.markdown("""
        Variáveis que você pode usar no assunto e corpo do email (entre chaves):

        | Variável | Conteúdo |
        |---|---|
        | `{titulo}` | Título da pauta |
        | `{data}` | Data prevista (AAAA-MM-DD) |
        | `{horario}` | Horário (se informado) |
        | `{tema}` | Tema (sugerido ou customizado) |
        | `{tipo}` | Tipo de material |
        | `{redes}` | Lista de redes/canais (separada por vírgula) |
        | `{publico}` | Público-alvo |
        | `{objetivo}` | Objetivo da publicação |
        | `{responsavel}` | Comunicador responsável |
        | `{designer}` | Designer/editor |
        | `{prioridade}` | Prioridade |
        | `{status}` | Status atual |
        | `{briefing}` | Briefing completo |
        | `{hashtags}` | Hashtags |
        | `{links}` | Links de referência |
        """)

    st.markdown(divisor("pontos"), unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns([2, 2, 1])
    with col_s1:
        if st.button("💾 Salvar todas as configurações", type="primary", use_container_width=True):
            cfg["tipos"] = [l.strip() for l in tipos_txt.split("\n") if l.strip()]
            cfg["redes"] = [l.strip() for l in redes_txt.split("\n") if l.strip()]
            cfg["status"] = [l.strip() for l in status_txt.split("\n") if l.strip()]
            cfg["prioridades"] = [l.strip() for l in pri_txt.split("\n") if l.strip()]
            cfg["temas"] = [l.strip() for l in temas_txt.split("\n") if l.strip()]
            cfg["email_imprensa"] = email_imp.strip()
            cfg["email_cc"] = email_cc.strip()
            cfg["email_assunto"] = email_assunto
            cfg["email_corpo"] = email_corpo
            st.success("✅ Configurações salvas! Lembre de baixar o JSON na sidebar para preservar.")
            st.rerun()

    with col_s2:
        cfg_export = json.dumps(cfg, ensure_ascii=False, indent=2)
        st.download_button("📥 Baixar só as configurações", cfg_export,
            file_name=f"univaja_config_{date.today().isoformat()}.json",
            mime="application/json", use_container_width=True)

    with col_s3:
        if st.button("↺ Resetar", use_container_width=True,
                     help="Volta tudo aos valores padrão UNIVAJA"):
            st.session_state.config = {
                "tipos": TIPOS_DEFAULT.copy(),
                "redes": REDES_DEFAULT.copy(),
                "status": STATUS_DEFAULT.copy(),
                "prioridades": PRIORIDADES_DEFAULT.copy(),
                "temas": TEMAS_DEFAULT.copy(),
                "email_imprensa": "imprensa@univaja.org",
                "email_cc": "",
                "email_assunto": EMAIL_ASSUNTO_DEFAULT,
                "email_corpo": EMAIL_CORPO_DEFAULT,
            }
            st.rerun()

    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.caption("Planner UNIVAJA · ASCOM · 2026 — uso interno · Identidade visual baseada no Manual de Marca UNIVAJA")
