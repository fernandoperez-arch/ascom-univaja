"""
PLANNER UNIVAJA — Plataforma de planejamento editorial
Os comunicadores propõem pautas, montam o cronograma de postagens e geram
relatório em PDF para a reunião semanal da ASCOM.

Identidade visual: Manual de Marca UNIVAJA (grafismos dos povos do Vale do Javari).
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json
import uuid
import io

from fpdf import FPDF

from univaja_brand import (
    css_global, header, divisor, section_title,
    PRIMARIA, VERMELHO_ESC, VERMELHO_MED, VERMELHO_CLARO,
    VERDE, VERDE_ESC, VERDE_PRETO, VERDE_CLARO,
    CINZA, PRETO, BRANCO, CREME,
)

# ─── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Planner UNIVAJA — Pautas & Cronograma",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(css_global(), unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    header(
        "PLANNER UNIVAJA",
        "Pautas, cronograma e relatório · ASCOM",
        "Uso colaborativo · 2026",
    ),
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
#  SCHEMAS DE CAMPOS
# ══════════════════════════════════════════════════════════════════════════════
TIPOS = [
    "Card único", "Carrossel", "Vídeo / Reels", "Stories",
    "Boletim interno", "Release", "Nota oficial", "Artigo",
    "Live", "Podcast / Áudio",
]

REDES = [
    "Instagram", "Facebook", "LinkedIn", "WhatsApp",
    "YouTube", "TikTok", "Site UNIVAJA", "Imprensa",
]

STATUS_LIST = [
    "💡 Proposta", "✏️ Em produção", "⏳ Aguardando aprovação",
    "✅ Aprovado", "📤 Publicado", "🗄️ Arquivado",
]

PRIORIDADES = ["🟢 Baixa", "🔵 Normal", "🟡 Alta", "🔴 Urgente"]

TEMAS_SUGERIDOS = [
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

# ══════════════════════════════════════════════════════════════════════════════
#  ESTADO
# ══════════════════════════════════════════════════════════════════════════════
if "pautas" not in st.session_state:
    st.session_state.pautas = []
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None


def nova_pauta_dict() -> dict:
    return {
        "id": str(uuid.uuid4())[:8],
        "data": date.today().isoformat(),
        "titulo": "",
        "tema": TEMAS_SUGERIDOS[0],
        "tema_custom": "",
        "tipo": TIPOS[0],
        "redes": [REDES[0]],
        "responsavel": "",
        "designer": "",
        "status": STATUS_LIST[0],
        "prioridade": PRIORIDADES[1],
        "horario": "",
        "publico": "",
        "objetivo": "",
        "briefing": "",
        "hashtags": "#UNIVAJA #ValeDoJavari #PovosIndígenas",
        "links": "",
        "criado_em": datetime.now().isoformat(),
    }


def salvar_pauta(p: dict):
    existente = next((i for i, x in enumerate(st.session_state.pautas) if x["id"] == p["id"]), None)
    if existente is not None:
        st.session_state.pautas[existente] = p
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


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — Filtros + Backup
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔍 Filtros")

    filtro_responsavel = st.text_input("Responsável", placeholder="ex: Fran, Tumi, Débora")
    filtro_status = st.multiselect("Status", STATUS_LIST, default=[])
    filtro_redes = st.multiselect("Rede social", REDES, default=[])
    filtro_prioridade = st.multiselect("Prioridade", PRIORIDADES, default=[])

    filtro_data_de = st.date_input("De", value=None, format="DD/MM/YYYY")
    filtro_data_ate = st.date_input("Até", value=None, format="DD/MM/YYYY")

    st.markdown("---")
    st.markdown("### 💾 Backup")
    st.caption("Salve um JSON com todas as pautas. Reimporte depois para continuar de onde parou ou compartilhar com a equipe.")

    if st.session_state.pautas:
        export_json = json.dumps(st.session_state.pautas, ensure_ascii=False, indent=2)
        st.download_button(
            "📥 Baixar pautas (JSON)",
            export_json,
            file_name=f"pautas_univaja_{date.today().isoformat()}.json",
            mime="application/json",
            use_container_width=True,
        )

    arquivo = st.file_uploader("📤 Importar JSON", type=["json"], label_visibility="collapsed")
    if arquivo is not None:
        try:
            dados = json.loads(arquivo.read())
            if isinstance(dados, list):
                modo = st.radio("Como importar?", ["Adicionar às pautas atuais", "Substituir tudo"], horizontal=False)
                if st.button("Confirmar importação", type="primary"):
                    if modo == "Substituir tudo":
                        st.session_state.pautas = dados
                    else:
                        ids_existentes = {p["id"] for p in st.session_state.pautas}
                        for p in dados:
                            if p.get("id") not in ids_existentes:
                                st.session_state.pautas.append(p)
                    st.success(f"{len(dados)} pauta(s) importada(s)!")
                    st.rerun()
            else:
                st.error("Formato inválido — esperado uma lista de pautas.")
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
#  ABAS
# ══════════════════════════════════════════════════════════════════════════════
aba_n, aba_l, aba_c, aba_k, aba_r, aba_p = st.tabs([
    "➕ Nova pauta",
    "📋 Lista de pautas",
    "📅 Cronograma",
    "📊 Kanban (status)",
    "📄 Relatório PDF",
    "ℹ️ Como usar",
])

# ──────────────────────────────────────────────────────────────────────────────
#  ABA — NOVA PAUTA
# ──────────────────────────────────────────────────────────────────────────────
with aba_n:
    edit_mode = st.session_state.edit_id is not None
    pauta = pauta_por_id(st.session_state.edit_id) if edit_mode else nova_pauta_dict()

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

        # Linha 1 — título e data
        col_t, col_d = st.columns([3, 1])
        with col_t:
            titulo = st.text_input(
                "📌 Título da pauta *",
                value=pauta["titulo"],
                placeholder="ex: Cobertura assembleia Marubo / 3 anos Bruno e Dom",
            )
        with col_d:
            data_str = pauta.get("data") or date.today().isoformat()
            data_dt = st.date_input("📅 Data prevista *", value=date.fromisoformat(data_str), format="DD/MM/YYYY")

        # Linha 2 — tema, tipo, prioridade
        col_te, col_ti, col_pr = st.columns(3)
        with col_te:
            tema = st.selectbox(
                "🎯 Tema",
                TEMAS_SUGERIDOS,
                index=TEMAS_SUGERIDOS.index(pauta["tema"]) if pauta["tema"] in TEMAS_SUGERIDOS else 0,
            )
            tema_custom = ""
            if tema == "Outro":
                tema_custom = st.text_input(
                    "Especifique o tema",
                    value=pauta.get("tema_custom",""),
                    placeholder="ex: Festival Yoxin",
                )
        with col_ti:
            tipo = st.selectbox(
                "📝 Tipo de material",
                TIPOS,
                index=TIPOS.index(pauta["tipo"]) if pauta["tipo"] in TIPOS else 0,
            )
        with col_pr:
            prioridade = st.selectbox(
                "🚦 Prioridade",
                PRIORIDADES,
                index=PRIORIDADES.index(pauta["prioridade"]) if pauta["prioridade"] in PRIORIDADES else 1,
            )

        # Linha 3 — redes + horário
        col_re, col_ho = st.columns([3, 1])
        with col_re:
            redes = st.multiselect(
                "📡 Redes sociais / canais *",
                REDES,
                default=pauta.get("redes", [REDES[0]]),
            )
        with col_ho:
            horario = st.text_input(
                "🕐 Horário (opcional)",
                value=pauta.get("horario",""),
                placeholder="ex: 09h00",
            )

        # Linha 4 — responsáveis
        col_r1, col_r2, col_st = st.columns(3)
        with col_r1:
            responsavel = st.text_input(
                "👤 Responsável (comunicador) *",
                value=pauta.get("responsavel",""),
                placeholder="ex: Fran, Tumi, Pixi Matis",
            )
        with col_r2:
            designer = st.text_input(
                "🎨 Designer / editor (se aplicável)",
                value=pauta.get("designer",""),
                placeholder="ex: João Marubo",
            )
        with col_st:
            status = st.selectbox(
                "📊 Status",
                STATUS_LIST,
                index=STATUS_LIST.index(pauta["status"]) if pauta["status"] in STATUS_LIST else 0,
            )

        # Linha 5 — público + objetivo
        col_pu, col_ob = st.columns(2)
        with col_pu:
            publico = st.text_input(
                "👥 Público-alvo",
                value=pauta.get("publico",""),
                placeholder="ex: aldeias / imprensa / parceiros internacionais",
            )
        with col_ob:
            objetivo = st.text_input(
                "🎯 Objetivo da publicação",
                value=pauta.get("objetivo",""),
                placeholder="ex: informar / denunciar / celebrar / mobilizar",
            )

        # Briefing
        briefing = st.text_area(
            "📝 Briefing (o que o card/vídeo deve comunicar)",
            value=pauta.get("briefing",""),
            placeholder="Descreva o que o material deve dizer, referências visuais, falas, dados a destacar...",
            height=120,
        )

        # Hashtags + links
        col_h, col_l = st.columns(2)
        with col_h:
            hashtags = st.text_input(
                "🏷️ Hashtags",
                value=pauta.get("hashtags", "#UNIVAJA #ValeDoJavari #PovosIndígenas"),
            )
        with col_l:
            links = st.text_input(
                "🔗 Links de referência",
                value=pauta.get("links",""),
                placeholder="ex: matéria base, foto de referência, contato fonte",
            )

        st.markdown("")
        col_ok, col_dup = st.columns([1, 1])
        with col_ok:
            submeter = st.form_submit_button(
                "💾 Salvar pauta" if edit_mode else "➕ Adicionar pauta",
                type="primary",
                use_container_width=True,
            )
        with col_dup:
            if edit_mode:
                duplicar = st.form_submit_button("📋 Salvar como cópia", use_container_width=True)
            else:
                duplicar = False

        if submeter or duplicar:
            erros = []
            if not titulo.strip():
                erros.append("Título é obrigatório.")
            if not responsavel.strip():
                erros.append("Responsável é obrigatório.")
            if not redes:
                erros.append("Selecione ao menos uma rede social / canal.")

            if erros:
                for e in erros:
                    st.error(f"⚠️ {e}")
            else:
                nova = pauta.copy() if edit_mode else nova_pauta_dict()
                if duplicar:
                    nova["id"] = str(uuid.uuid4())[:8]
                    nova["criado_em"] = datetime.now().isoformat()

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
                    st.success(f"✅ Pauta atualizada!")
                else:
                    st.success(f"✅ Pauta adicionada ao planejamento!")
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
        # Stats
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
            # cor da borda por prioridade
            cor_pri = {
                "🟢 Baixa": VERDE_CLARO,
                "🔵 Normal": VERDE,
                "🟡 Alta": VERMELHO_MED,
                "🔴 Urgente": PRIMARIA,
            }.get(p.get("prioridade",""), VERDE)

            data_fmt = ""
            try:
                data_fmt = datetime.fromisoformat(p["data"]).strftime("%d/%m/%Y (%a)")
            except Exception:
                data_fmt = p.get("data","")

            redes_str = " · ".join(p.get("redes", []))
            tema_str = tema_efetivo(p)

            with st.container():
                st.markdown(f"""
                <div class="card" style="border-left:5px solid {cor_pri};margin-bottom:8px">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
                        <div style="flex:1;min-width:280px">
                            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px">
                                <span class="badge badge-perm">{p.get('prioridade','')}</span>
                                <span class="badge badge-pol">{p.get('status','')}</span>
                                <span class="badge badge-int">{p.get('tipo','')}</span>
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

                col_e, col_d, col_id = st.columns([1, 1, 4])
                with col_e:
                    if st.button("✏️ Editar", key=f"edit_{p['id']}", use_container_width=True):
                        st.session_state.edit_id = p["id"]
                        st.rerun()
                with col_d:
                    if st.button("🗑️ Remover", key=f"del_{p['id']}", use_container_width=True):
                        remover_pauta(p["id"])
                        st.rerun()
                with col_id:
                    st.caption(f"ID: {p['id']}")

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
        # Agrupa por data
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
                if delta == 0:
                    selo = "HOJE"
                    cor_selo = PRIMARIA
                elif delta == 1:
                    selo = "AMANHÃ"
                    cor_selo = VERMELHO_MED
                elif delta < 0:
                    selo = f"há {-delta} dia(s)"
                    cor_selo = CINZA
                elif delta <= 7:
                    selo = f"em {delta} dia(s)"
                    cor_selo = VERDE
                else:
                    selo = f"em {delta} dias"
                    cor_selo = VERDE_ESC
            except Exception:
                dia_fmt = d
                selo = ""
                cor_selo = CINZA

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

    if not pautas_filt:
        st.markdown("""
        <div class="alerta">
            📭 Nenhuma pauta para mostrar.
        </div>
        """, unsafe_allow_html=True)
    else:
        # primeiras 4 colunas, depois 2 = 6 colunas em duas linhas
        for linha_inicio in [0, 3]:
            cols = st.columns(3)
            for i, status in enumerate(STATUS_LIST[linha_inicio:linha_inicio+3]):
                pautas_status = [p for p in pautas_filt if p.get("status") == status]
                with cols[i]:
                    cor = {
                        "💡 Proposta": VERDE_CLARO,
                        "✏️ Em produção": VERDE,
                        "⏳ Aguardando aprovação": VERMELHO_MED,
                        "✅ Aprovado": VERDE_ESC,
                        "📤 Publicado": PRIMARIA,
                        "🗄️ Arquivado": CINZA,
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
#  ABA — RELATÓRIO PDF
# ──────────────────────────────────────────────────────────────────────────────

def gerar_pdf(pautas: list, titulo_reuniao: str, periodo_descr: str, observacoes: str) -> bytes:
    """Gera relatório PDF com cores e grafismos UNIVAJA."""

    def hex_rgb(h: str):
        h = h.lstrip("#")
        return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ── helpers ──
    def latin(s: str) -> str:
        return (s or "").encode("latin-1", "replace").decode("latin-1")

    def grafismo_marubo_topo(y0=10, h=8):
        """Faixa Marubo simplificada no topo."""
        r, g, b = hex_rgb(PRIMARIA)
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(0.6)
        x = 10
        step = 6
        while x < 200:
            pdf.line(x, y0+h, x, y0+2)
            pdf.line(x, y0+2, x+step/2, y0+2)
            pdf.line(x+step/2, y0+2, x+step/2, y0+h-2)
            pdf.line(x+step/2, y0+h-2, x+step, y0+h-2)
            pdf.line(x+step, y0+h-2, x+step, y0+2)
            x += step

    def divisor_zig(y, cor=PRIMARIA):
        r, g, b = hex_rgb(cor)
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(0.5)
        x = 10
        up = True
        while x < 200:
            pdf.line(x, y+(0 if up else 3), x+4, y+(3 if up else 0))
            up = not up
            x += 4

    def pontos_kanamari(y, cor=PRIMARIA):
        r, g, b = hex_rgb(cor)
        pdf.set_fill_color(r, g, b)
        x = 10
        while x < 200:
            pdf.ellipse(x, y, 1.2, 1.2, "F")
            pdf.ellipse(x+6, y, 1.2, 1.2, "F")
            x += 12

    # ── HEADER ──
    r, g, b = hex_rgb(PRIMARIA)
    pdf.set_fill_color(r, g, b)
    pdf.rect(0, 0, 210, 38, "F")

    # faixa marubo branca no header
    pdf.set_draw_color(255, 255, 255)
    pdf.set_line_width(0.4)
    x = 10; step = 5
    while x < 200:
        pdf.line(x, 4, x, 8)
        pdf.line(x, 8, x+step/2, 8)
        pdf.line(x+step/2, 8, x+step/2, 5)
        pdf.line(x+step/2, 5, x+step, 5)
        x += step

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 22)
    pdf.set_xy(10, 12)
    pdf.cell(0, 8, latin("UNIVAJA"), ln=1)
    pdf.set_font("helvetica", "", 11)
    pdf.set_x(10)
    pdf.cell(0, 5, latin("Planejamento editorial - ASCOM"), ln=1)
    pdf.set_font("helvetica", "I", 9)
    pdf.set_x(10)
    pdf.cell(0, 5, latin(f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"), ln=1)

    # pontos kanamari no fim do header
    r, g, b = hex_rgb(BRANCO)
    pdf.set_fill_color(r, g, b)
    x = 10
    while x < 200:
        pdf.ellipse(x, 33, 0.8, 0.8, "F")
        pdf.ellipse(x+4, 33, 0.8, 0.8, "F")
        x += 8

    pdf.set_y(46)

    # ── TÍTULO DO RELATÓRIO ──
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

    # ── RESUMO ──
    r, g, b = hex_rgb(VERDE_PRETO)
    pdf.set_text_color(r, g, b)
    pdf.set_font("helvetica", "B", 13)
    pdf.cell(0, 7, latin("Resumo geral"), ln=1)
    pdf.set_font("helvetica", "", 10)
    r, g, b = hex_rgb(CINZA)
    pdf.set_text_color(r, g, b)

    total = len(pautas)
    por_status = {}
    por_rede = {}
    por_resp = {}
    por_prio = {}
    for p in pautas:
        por_status[p.get("status","")] = por_status.get(p.get("status",""), 0) + 1
        por_prio[p.get("prioridade","")] = por_prio.get(p.get("prioridade",""), 0) + 1
        por_resp[p.get("responsavel","—")] = por_resp.get(p.get("responsavel","—"), 0) + 1
        for r2 in p.get("redes", []):
            por_rede[r2] = por_rede.get(r2, 0) + 1

    pdf.cell(0, 6, latin(f"  • Total de pautas: {total}"), ln=1)
    if por_prio:
        prio_txt = "  • Prioridade: " + ", ".join([f"{k} ({v})" for k, v in por_prio.items()])
        pdf.multi_cell(0, 6, latin(prio_txt))
    if por_status:
        st_txt = "  • Status: " + ", ".join([f"{k} ({v})" for k, v in por_status.items()])
        pdf.multi_cell(0, 6, latin(st_txt))
    if por_rede:
        re_txt = "  • Redes/canais: " + ", ".join([f"{k} ({v})" for k, v in por_rede.items()])
        pdf.multi_cell(0, 6, latin(re_txt))
    if por_resp:
        rp_txt = "  • Por responsavel: " + ", ".join([f"{k} ({v})" for k, v in por_resp.items()])
        pdf.multi_cell(0, 6, latin(rp_txt))

    pdf.ln(3)
    pontos_kanamari(pdf.get_y(), PRIMARIA)
    pdf.ln(5)

    # ── OBSERVAÇÕES ──
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

    # ── PAUTAS POR DATA ──
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
        if pdf.get_y() > 250:
            pdf.add_page()

        try:
            dt = datetime.fromisoformat(d)
            dias_pt = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
            dia_fmt = f"{dt.strftime('%d/%m/%Y')} - {dias_pt[dt.weekday()]}"
        except Exception:
            dia_fmt = d

        # Cabeçalho da data
        r, g, b = hex_rgb(VERDE_PRETO)
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 7, latin(f"  {dia_fmt}"), ln=1, fill=True)
        pdf.ln(1)

        for p in lista:
            if pdf.get_y() > 260:
                pdf.add_page()

            cor_pri = {
                "🟢 Baixa": VERDE_CLARO, "🔵 Normal": VERDE,
                "🟡 Alta": VERMELHO_MED, "🔴 Urgente": PRIMARIA,
            }.get(p.get("prioridade",""), VERDE)

            # Barra vertical lateral
            r, g, b = hex_rgb(cor_pri)
            y_ini = pdf.get_y()
            pdf.set_fill_color(r, g, b)

            # Título da pauta
            r, g, b = hex_rgb(VERDE_PRETO)
            pdf.set_text_color(r, g, b)
            pdf.set_font("helvetica", "B", 11)
            pdf.set_x(14)
            titulo_full = p.get("titulo","(sem titulo)")
            if p.get("horario"):
                titulo_full = f"[{p['horario']}] {titulo_full}"
            pdf.multi_cell(0, 6, latin(titulo_full))

            # Linha de metadados
            r, g, b = hex_rgb(CINZA)
            pdf.set_text_color(r, g, b)
            pdf.set_font("helvetica", "", 9)
            meta = f"Tema: {tema_efetivo(p)}  |  Tipo: {p.get('tipo','')}  |  Status: {p.get('status','')}  |  Prioridade: {p.get('prioridade','')}"
            pdf.set_x(14)
            pdf.multi_cell(0, 4.5, latin(meta))

            redes_txt = ", ".join(p.get("redes",[])) or "—"
            pdf.set_x(14)
            pdf.multi_cell(0, 4.5, latin(f"Redes/canais: {redes_txt}"))

            resp_txt = f"Responsavel: {p.get('responsavel','—')}"
            if p.get("designer"):
                resp_txt += f"  |  Designer/editor: {p.get('designer')}"
            pdf.set_x(14)
            pdf.multi_cell(0, 4.5, latin(resp_txt))

            if p.get("publico"):
                pdf.set_x(14)
                pdf.multi_cell(0, 4.5, latin(f"Publico: {p['publico']}"))
            if p.get("objetivo"):
                pdf.set_x(14)
                pdf.multi_cell(0, 4.5, latin(f"Objetivo: {p['objetivo']}"))

            if p.get("briefing"):
                pdf.set_x(14)
                pdf.set_font("helvetica", "I", 9)
                pdf.multi_cell(0, 4.5, latin(f"Briefing: {p['briefing']}"))

            if p.get("hashtags"):
                pdf.set_x(14)
                pdf.set_font("helvetica", "", 9)
                pdf.multi_cell(0, 4.5, latin(f"Hashtags: {p['hashtags']}"))
            if p.get("links"):
                pdf.set_x(14)
                pdf.multi_cell(0, 4.5, latin(f"Links: {p['links']}"))

            y_fim = pdf.get_y()
            r, g, b = hex_rgb(cor_pri)
            pdf.set_fill_color(r, g, b)
            pdf.rect(10, y_ini, 1.5, max(y_fim - y_ini, 4), "F")

            pdf.ln(3)

        pdf.ln(2)

    # ── RODAPÉ ──
    pdf.set_y(-22)
    divisor_zig(pdf.get_y(), PRIMARIA)
    pdf.ln(3)
    r, g, b = hex_rgb(CINZA)
    pdf.set_text_color(r, g, b)
    pdf.set_font("helvetica", "I", 8)
    pdf.cell(0, 4, latin("Planner UNIVAJA - ASCOM 2026 - documento de uso interno"), align="C", ln=1)
    pdf.cell(0, 4, latin("Identidade visual baseada no Manual de Marca UNIVAJA"), align="C", ln=1)

    # Compatível com fpdf2 (bytearray) e PyFPDF antigo (str)
    result = pdf.output(dest="S")
    if isinstance(result, str):
        return result.encode("latin-1", "replace")
    return bytes(result)


with aba_r:
    st.markdown(section_title("Relatório PDF para a reunião", "vermelho"), unsafe_allow_html=True)
    st.caption("Configure as informações de capa, escolha as pautas (use os filtros na barra lateral) e baixe o PDF.")

    col_t, col_p = st.columns(2)
    with col_t:
        titulo_rel = st.text_input(
            "Título do relatório",
            value=f"Reunião ASCOM — {date.today().strftime('%d/%m/%Y')}",
            placeholder="ex: Reunião semanal 09/06/2026",
        )
    with col_p:
        periodo_rel = st.text_input(
            "Período / contexto",
            value="Pautas propostas para a próxima semana",
            placeholder="ex: Quinzena 09-22/06 · Cobertura Amazon Week",
        )

    observ = st.text_area(
        "Observações para a reunião (opcional)",
        placeholder="Pontos a debater, alertas, dependências, decisões pendentes...",
        height=100,
    )

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
                st.download_button(
                    "📄 Baixar relatório PDF",
                    pdf_bytes,
                    file_name=f"pautas_univaja_{date.today().isoformat()}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )
                st.success("✅ PDF pronto — clique para baixar.")
            except Exception as ex:
                st.error(f"Erro ao gerar PDF: {ex}")
        else:
            st.markdown("""
            <div class="alerta">
                ⚠️ Nenhuma pauta para incluir. Adicione pautas ou ajuste os filtros.
            </div>
            """, unsafe_allow_html=True)

    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown("**O PDF inclui:**")
    st.markdown("""
    - 🌿 **Capa UNIVAJA** com grafismos Marubo e pontos Kanamari
    - 📊 **Resumo geral**: total, prioridades, status, redes e responsáveis
    - 📝 **Observações** da reunião (campo acima)
    - 📅 **Pautas detalhadas agrupadas por data**, com tema, tipo, responsável, briefing, hashtags e links
    - 🎨 **Cores e divisores** seguindo o Manual de Marca UNIVAJA
    """)

# ──────────────────────────────────────────────────────────────────────────────
#  ABA — COMO USAR
# ──────────────────────────────────────────────────────────────────────────────
with aba_p:
    st.markdown(section_title("Como usar o Planner", "padrao"), unsafe_allow_html=True)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown(f"""
        ### 🎯 Para que serve
        O **Planner UNIVAJA** organiza todo o ciclo de planejamento editorial da ASCOM.
        Cada comunicador pode propor pautas, definir responsáveis, escolher redes e
        montar o cronograma. No fim, o ponto focal gera um **PDF** para apresentar
        na reunião semanal.

        ### 📋 Fluxo recomendado

        <div class="card card-vermelho">
            <strong style="color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">1. Antes da reunião — propor pautas</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Cada comunicador entra no Planner durante a semana, vai em <strong>➕ Nova pauta</strong> e propõe
            quantas pautas quiser. Define data, tema, tipo, redes e a si mesmo (ou outra pessoa) como responsável.
            Status inicial: <strong>💡 Proposta</strong>.
            </p>
        </div>

        <div class="card card-verde">
            <strong style="color:{VERDE};text-transform:uppercase;letter-spacing:0.5px">2. Reunião de segunda — alinhamento</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Ponto focal abre a aba <strong>📅 Cronograma</strong> e <strong>📊 Kanban</strong>, debate as pautas com a equipe,
            confirma responsáveis, ajusta datas e muda status para <strong>✏️ Em produção</strong> nas aprovadas.
            Em seguida, gera o <strong>📄 PDF</strong> da quinzena e envia para a coordenação.
            </p>
        </div>

        <div class="card card-azul">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">3. Durante a semana — produção</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Comunicadores acompanham suas pautas e atualizam o status conforme avançam:
            <strong>⏳ Aguardando aprovação</strong> → <strong>✅ Aprovado</strong> → <strong>📤 Publicado</strong>.
            </p>
        </div>

        <div class="card card-cinza">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">4. Sexta — fechamento e backup</strong>
            <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">
            Ponto focal baixa o JSON (barra lateral) para guardar o histórico da semana.
            Pautas publicadas viram referência futura. Atrasos viram pauta da próxima reunião.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 💡 Dicas práticas")
        st.markdown(f"""
        <div class="card-grafismo" style="margin-bottom:10px">
            <div class="card-grafismo-conteudo">
                <strong style="font-size:13px;color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">💾 Backup é fundamental</strong>
                <p style="font-size:12px;margin-top:6px;line-height:1.5;color:{CINZA}">
                Este app guarda as pautas na sua sessão (memória do navegador).
                <strong>Baixe o JSON ao fim de cada uso</strong> na barra lateral para não perder o trabalho.
                </p>
            </div>
        </div>

        <div class="card-grafismo" style="margin-bottom:10px">
            <div class="card-grafismo-conteudo">
                <strong style="font-size:13px;color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">🔄 Compartilhe o JSON</strong>
                <p style="font-size:12px;margin-top:6px;line-height:1.5;color:{CINZA}">
                Para trabalhar em equipe, exporte o JSON e envie no grupo ASCOM.
                Outros podem importar e ver/editar as mesmas pautas.
                </p>
            </div>
        </div>

        <div class="card-grafismo" style="margin-bottom:10px">
            <div class="card-grafismo-conteudo">
                <strong style="font-size:13px;color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">🔍 Use os filtros</strong>
                <p style="font-size:12px;margin-top:6px;line-height:1.5;color:{CINZA}">
                Filtre por responsável, rede ou status na barra lateral. O PDF do relatório
                respeita os filtros ativos.
                </p>
            </div>
        </div>

        <div class="card-grafismo" style="margin-bottom:10px">
            <div class="card-grafismo-conteudo">
                <strong style="font-size:13px;color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">🚦 Prioridade urgente</strong>
                <p style="font-size:12px;margin-top:6px;line-height:1.5;color:{CINZA}">
                Use <strong>🔴 Urgente</strong> apenas para pautas que não podem esperar a próxima reunião
                (datas sensíveis, denúncias, coberturas ao vivo).
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.caption("Planner UNIVAJA · ASCOM · 2026 — uso interno · Identidade visual baseada no Manual de Marca UNIVAJA")
