"""
CENTRAL EDITORIAL UNIVAJA
Sistema interno de gestão de conteúdo da ASCOM.

Login → Dashboard → Cadastro → Calendário → Fila de aprovação → Publicados → Relatórios → Monitor.
Hospedagem: Streamlit Community Cloud. Dados: sessão + backup JSON (preparado p/ Supabase).
Identidade visual: Manual de Marca UNIVAJA.
"""

import calendar as _cal
from datetime import date, datetime, timedelta

import streamlit as st

from univaja_brand import (
    css_global, header, sidebar_logo, divisor, section_title,
    logo_google_noticias, logo_google_trends, logo_google_search,
    PRIMARIA, VERMELHO_ESC, VERMELHO_MED, VERDE, VERDE_ESC, VERDE_PRETO,
    VERDE_CLARO, CINZA, CREME,
)
from core import auth, data
from core import workflow as wf
from core.calendar_link import link_google_agenda

# ─── Config ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Central Editorial UNIVAJA",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(css_global(), unsafe_allow_html=True)


def render_header():
    st.markdown(header("CENTRAL EDITORIAL", "Gestão de conteúdo institucional · ASCOM",
                       "Sistema interno · 2026"), unsafe_allow_html=True)


# ─── LOGIN GATE ────────────────────────────────────────────────────────────────
if not auth.tela_login(render_header):
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — logo, navegação, usuário, backup
# ══════════════════════════════════════════════════════════════════════════════
# Navegação pendente (ex: clicar "Editar" no calendário pula para Cadastro)
if "_pending_nav" in st.session_state:
    st.session_state["nav"] = st.session_state.pop("_pending_nav")

with st.sidebar:
    st.markdown(sidebar_logo(), unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        ["📊 Dashboard", "➕ Cadastro de pauta", "🗓️ Calendário editorial",
         "✅ Fila de aprovação", "📤 Publicados", "📈 Relatórios", "🔍 Monitor de notícias"],
        label_visibility="collapsed",
        key="nav",
    )

    st.markdown("---")
    st.caption(f"👤 Logado como **{auth.usuario_atual()}**")
    if st.button("🚪 Sair", use_container_width=True):
        auth.logout()
        st.rerun()

    st.markdown("---")
    st.markdown("##### 💾 Backup dos dados")
    st.caption("No Streamlit Cloud os dados ficam na sessão. Baixe o JSON ao fim do uso.")
    st.download_button("📥 Baixar (JSON)", data.exportar_json(),
                       file_name=f"central_univaja_{date.today().isoformat()}.json",
                       mime="application/json", use_container_width=True)
    up = st.file_uploader("📤 Restaurar JSON", type=["json"], label_visibility="collapsed")
    if up is not None:
        modo = st.radio("Modo", ["Substituir tudo", "Adicionar"], horizontal=True, key="imp_modo")
        if st.button("Confirmar importação", type="primary", use_container_width=True):
            try:
                n = data.importar_json(up.read(), substituir=(modo == "Substituir tudo"))
                st.success(f"✅ {n} pauta(s) importada(s)!")
                st.rerun()
            except Exception as ex:
                st.error(f"Erro: {ex}")

    if not data.listar():
        if st.button("✨ Carregar exemplos", use_container_width=True):
            data.carregar_exemplos()
            st.rerun()

render_header()


# ─── Helpers de UI ─────────────────────────────────────────────────────────────
def card_metrica(valor, label, cor=PRIMARIA):
    return f"""<div style="background:white;border:1px solid #e5e7eb;border-top:4px solid {cor};
        border-radius:12px;padding:16px 18px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.04)">
        <div style="font-size:30px;font-weight:800;color:{cor};line-height:1;font-family:'Battambang',serif">{valor}</div>
        <div style="font-size:11px;color:{CINZA};margin-top:6px;text-transform:uppercase;letter-spacing:.5px">{label}</div>
    </div>"""


def linha_pauta(p, contexto=""):
    """Card-linha de uma pauta com badges."""
    atras = wf.esta_atrasada(p)
    prox = wf.esta_proxima(p)
    borda = wf.cor_status(p.get("status", ""))
    try:
        data_fmt = datetime.fromisoformat(p["data"]).strftime("%d/%m/%Y")
    except Exception:
        data_fmt = p.get("data", "")

    alerta = ""
    if atras:
        alerta = f'<span style="background:{PRIMARIA};color:white;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700">🔴 ATRASADA</span>'
    elif prox:
        alerta = f'<span style="background:#e67e22;color:white;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700">⏰ EM BREVE</span>'

    return f"""<div style="background:white;border:1px solid #e5e7eb;border-left:5px solid {borda};
        border-radius:10px;padding:12px 16px;margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:flex-start">
            <div style="flex:1;min-width:240px">
                <div style="font-weight:700;font-size:14px;color:{VERDE_PRETO};margin-bottom:4px">{p.get('titulo','(sem título)')} {alerta}</div>
                <div style="font-size:12px;color:{CINZA}">📅 {data_fmt} · 🕐 {p.get('hora','')} · 📡 {p.get('canal','')} · 📝 {p.get('formato','')} · 👤 {p.get('responsavel','—')}</div>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
                {wf.badge_prioridade(p.get('prioridade',''))}
                {wf.badge_status(p.get('status',''))}
            </div>
        </div>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "📊 Dashboard":
    st.markdown(section_title("Dashboard editorial", "padrao"), unsafe_allow_html=True)

    pautas = data.listar()
    if not pautas:
        st.markdown("""<div class="alerta">📭 Nenhuma pauta ainda. Vá em <strong>➕ Cadastro de pauta</strong>
            ou clique em <strong>✨ Carregar exemplos</strong> na barra lateral.</div>""", unsafe_allow_html=True)
    else:
        total = len(pautas)
        publicadas = sum(1 for p in pautas if "Publicado" in p["status"])
        atrasadas = sum(1 for p in pautas if wf.esta_atrasada(p))
        aprovacao = sum(1 for p in pautas if "Aguardando" in p["status"] or "revisão" in p["status"])
        proximas = sum(1 for p in pautas if wf.esta_proxima(p))

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(card_metrica(total, "Total", VERDE_PRETO), unsafe_allow_html=True)
        c2.markdown(card_metrica(proximas, "Próx. 7 dias", VERDE), unsafe_allow_html=True)
        c3.markdown(card_metrica(aprovacao, "Em aprovação", "#e67e22"), unsafe_allow_html=True)
        c4.markdown(card_metrica(atrasadas, "Atrasadas", PRIMARIA), unsafe_allow_html=True)
        c5.markdown(card_metrica(publicadas, "Publicadas", VERDE_ESC), unsafe_allow_html=True)

        st.markdown(divisor("zig"), unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("##### ⏰ Próximas publicações")
            prox_list = sorted([p for p in pautas if wf.esta_proxima(p, 14)],
                               key=lambda x: x.get("data", ""))
            if prox_list:
                for p in prox_list[:6]:
                    st.markdown(linha_pauta(p), unsafe_allow_html=True)
            else:
                st.caption("Nada programado para os próximos 14 dias.")
        with col_b:
            st.markdown("##### 🔴 Pautas atrasadas")
            atr_list = sorted([p for p in pautas if wf.esta_atrasada(p)],
                             key=lambda x: x.get("data", ""))
            if atr_list:
                for p in atr_list[:6]:
                    st.markdown(linha_pauta(p), unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alerta alerta-verde">✅ Nenhuma pauta atrasada. Equipe em dia!</div>',
                            unsafe_allow_html=True)

        st.markdown(divisor("pontos"), unsafe_allow_html=True)

        # Distribuição por status e canal (barras HTML)
        col_s, col_c = st.columns(2)
        with col_s:
            st.markdown("##### 📊 Por status")
            for s in wf.STATUS:
                n = sum(1 for p in pautas if p["status"] == s)
                if n == 0:
                    continue
                pct = int(n / total * 100)
                cor = wf.cor_status(s)
                st.markdown(f"""<div style="margin-bottom:6px">
                    <div style="display:flex;justify-content:space-between;font-size:12px;color:{VERDE_PRETO}">
                        <span>{s}</span><span><strong>{n}</strong></span></div>
                    <div style="background:#eee;border-radius:6px;height:8px;overflow:hidden">
                        <div style="background:{cor};width:{pct}%;height:100%"></div></div>
                </div>""", unsafe_allow_html=True)
        with col_c:
            st.markdown("##### 📡 Por canal")
            canais_count = {}
            for p in pautas:
                canais_count[p.get("canal", "—")] = canais_count.get(p.get("canal", "—"), 0) + 1
            for canal, n in sorted(canais_count.items(), key=lambda x: -x[1]):
                pct = int(n / total * 100)
                st.markdown(f"""<div style="margin-bottom:6px">
                    <div style="display:flex;justify-content:space-between;font-size:12px;color:{VERDE_PRETO}">
                        <span>{canal}</span><span><strong>{n}</strong></span></div>
                    <div style="background:#eee;border-radius:6px;height:8px;overflow:hidden">
                        <div style="background:{VERDE};width:{pct}%;height:100%"></div></div>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: CADASTRO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "➕ Cadastro de pauta":
    editando = st.session_state.get("editar_id")
    p = data.obter(editando) if editando else data.nova_pauta()
    if editando and not p:
        st.session_state.editar_id = None
        p = data.nova_pauta()

    st.markdown(section_title("Editar pauta" if editando else "Nova pauta",
                              "vermelho" if editando else "padrao"), unsafe_allow_html=True)
    if editando:
        st.markdown(f'<div class="alerta alerta-azul">✏️ Editando: <strong>{p.get("titulo")}</strong></div>',
                    unsafe_allow_html=True)
        if st.button("Cancelar edição"):
            st.session_state.editar_id = None
            st.rerun()

    with st.form("form_cad", clear_on_submit=not editando):
        c1, c2 = st.columns([3, 1])
        titulo = c1.text_input("Título da pauta *", value=p["titulo"],
                               help="Como a pauta será identificada na central.")
        prioridade = c2.selectbox("Prioridade", wf.PRIORIDADES,
                                  index=wf.PRIORIDADES.index(p["prioridade"]) if p["prioridade"] in wf.PRIORIDADES else 1)

        descricao = st.text_area("Descrição / resumo", value=p["descricao"],
                                 help="O que a publicação deve comunicar.", height=80)

        c3, c4, c5 = st.columns(3)
        canal = c3.selectbox("Canal *", wf.CANAIS,
                             index=wf.CANAIS.index(p["canal"]) if p["canal"] in wf.CANAIS else 0)
        formato = c4.selectbox("Formato *", wf.FORMATOS,
                              index=wf.FORMATOS.index(p["formato"]) if p["formato"] in wf.FORMATOS else 0)
        status = c5.selectbox("Status", wf.STATUS,
                             index=wf.STATUS.index(p["status"]) if p["status"] in wf.STATUS else 0,
                             help="Etapa do fluxo editorial.")

        c6, c7, c8 = st.columns(3)
        try:
            data_val = date.fromisoformat(p["data"])
        except Exception:
            data_val = date.today()
        data_pub = c6.date_input("Data de publicação *", value=data_val, format="DD/MM/YYYY")
        hora_pub = c7.text_input("Hora", value=p.get("hora", "09:00"), help="Formato 24h, ex: 14:30")
        responsavel = c8.text_input("Responsável *", value=p["responsavel"])

        c9, c10 = st.columns(2)
        aprovador = c9.text_input("Aprovador", value=p["aprovador"],
                                  help="Quem valida antes de publicar.")
        campanha = c10.text_input("Campanha relacionada", value=p["campanha"])

        c11, c12 = st.columns(2)
        publico = c11.text_input("Público-alvo", value=p["publico"])
        objetivo = c12.text_input("Objetivo", value=p["objetivo"])

        link_rascunho = st.text_input("🔗 Link do material / rascunho", value=p["link_rascunho"])

        # Campos secundários escondidos
        with st.expander("➕ Campos adicionais (links finais, observações, métricas)"):
            link_publicado = st.text_input("🔗 Link do post publicado", value=p["link_publicado"],
                                           help="Obrigatório para marcar como Publicado.")
            data_real = st.text_input("Data real de publicação", value=p.get("data_real", ""),
                                      placeholder="ex: 05/06/2026")
            obs_internas = st.text_area("Observações internas", value=p["obs_internas"], height=70)
            obs_pos = st.text_area("Observações pós-publicação", value=p["obs_pos"], height=70)
            mc1, mc2, mc3 = st.columns(3)
            imp = mc1.number_input("Impressões", min_value=0, value=int(p["metricas"].get("impressoes", 0)))
            com = mc2.number_input("Comentários", min_value=0, value=int(p["metricas"].get("comentarios", 0)))
            cli = mc3.number_input("Cliques", min_value=0, value=int(p["metricas"].get("cliques", 0)))

        salvar = st.form_submit_button("💾 Salvar pauta", type="primary", use_container_width=True)

        if salvar:
            p.update({
                "titulo": titulo.strip(), "descricao": descricao.strip(),
                "canal": canal, "formato": formato, "status": status,
                "prioridade": prioridade, "data": data_pub.isoformat(),
                "hora": hora_pub.strip(), "responsavel": responsavel.strip(),
                "aprovador": aprovador.strip(), "campanha": campanha.strip(),
                "publico": publico.strip(), "objetivo": objetivo.strip(),
                "link_rascunho": link_rascunho.strip(),
                "link_publicado": link_publicado.strip(), "data_real": data_real.strip(),
                "obs_internas": obs_internas.strip(), "obs_pos": obs_pos.strip(),
                "metricas": {"impressoes": imp, "comentarios": com, "cliques": cli},
            })
            erros_campo = []
            if not titulo.strip():
                erros_campo.append("Título é obrigatório.")
            if not responsavel.strip():
                erros_campo.append("Responsável é obrigatório.")
            erros_regra = wf.validar(p)

            if erros_campo or erros_regra:
                for e in erros_campo + erros_regra:
                    st.error(f"⚠️ {e}")
            else:
                data.salvar(p)
                st.session_state.editar_id = None
                st.success("✅ Pauta salva!")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: CALENDÁRIO EDITORIAL
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🗓️ Calendário editorial":
    st.markdown(section_title("Calendário editorial", "padrao"), unsafe_allow_html=True)

    # Filtros via form (sem reruns a cada clique)
    with st.expander("🔍 Filtros", expanded=True):
        with st.form("form_filtros"):
            fc1, fc2, fc3 = st.columns(3)
            f_canais = fc1.multiselect("Canal", wf.CANAIS)
            f_status = fc2.multiselect("Status", wf.STATUS)
            f_resp = fc3.text_input("Responsável contém")
            fc4, fc5, fc6 = st.columns(3)
            f_camp = fc4.text_input("Campanha contém")
            f_de = fc5.date_input("De", value=None, format="DD/MM/YYYY")
            f_ate = fc6.date_input("Até", value=None, format="DD/MM/YYYY")
            aplicar = st.form_submit_button("Aplicar filtros", type="primary", use_container_width=True)
            if aplicar:
                st.session_state.filtros = {
                    "canais": f_canais, "status": f_status, "resp": f_resp,
                    "camp": f_camp,
                    "de": f_de.isoformat() if f_de else None,
                    "ate": f_ate.isoformat() if f_ate else None,
                }

    flt = st.session_state.get("filtros", {})

    def passa(p):
        if flt.get("canais") and p["canal"] not in flt["canais"]:
            return False
        if flt.get("status") and p["status"] not in flt["status"]:
            return False
        if flt.get("resp") and flt["resp"].lower() not in p.get("responsavel", "").lower():
            return False
        if flt.get("camp") and flt["camp"].lower() not in p.get("campanha", "").lower():
            return False
        if flt.get("de") and p.get("data", "") < flt["de"]:
            return False
        if flt.get("ate") and p.get("data", "") > flt["ate"]:
            return False
        return True

    pautas = [p for p in data.listar() if passa(p)]

    vis = st.radio("Visualização", ["📅 Mês", "🗒️ Lista"], horizontal=True, label_visibility="collapsed")

    if vis == "📅 Mês":
        if "cal_ano" not in st.session_state: st.session_state.cal_ano = date.today().year
        if "cal_mes" not in st.session_state: st.session_state.cal_mes = date.today().month
        meses_pt = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
        n1, n2, n3 = st.columns([1, 3, 1])
        if n1.button("◀ Mês", use_container_width=True):
            st.session_state.cal_mes = 12 if st.session_state.cal_mes == 1 else st.session_state.cal_mes - 1
            if st.session_state.cal_mes == 12: st.session_state.cal_ano -= 1
            st.rerun()
        n2.markdown(f"<div style='text-align:center;font-family:Battambang,serif;font-weight:700;font-size:20px;color:{VERDE_PRETO};padding:6px'>{meses_pt[st.session_state.cal_mes-1].upper()} {st.session_state.cal_ano}</div>", unsafe_allow_html=True)
        if n3.button("Mês ▶", use_container_width=True):
            st.session_state.cal_mes = 1 if st.session_state.cal_mes == 12 else st.session_state.cal_mes + 1
            if st.session_state.cal_mes == 1: st.session_state.cal_ano += 1
            st.rerun()

        por_dia = {}
        for p in pautas:
            try:
                dt = date.fromisoformat(p["data"])
                if dt.month == st.session_state.cal_mes and dt.year == st.session_state.cal_ano:
                    por_dia.setdefault(dt.day, []).append(p)
            except Exception:
                pass

        _cal.setfirstweekday(_cal.SUNDAY)
        semanas = _cal.monthcalendar(st.session_state.cal_ano, st.session_state.cal_mes)
        dias_lbl = ["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"]
        hdr = "".join([f"<div style='background:{VERDE_PRETO};color:white;padding:6px;text-align:center;font-size:11px;font-weight:700;border-radius:6px 6px 0 0'>{d}</div>" for d in dias_lbl])
        cels = []
        for sem in semanas:
            for dia in sem:
                if dia == 0:
                    cels.append("<div style='min-height:78px'></div>"); continue
                evs = por_dia.get(dia, [])
                ev_html = ""
                for e in evs[:3]:
                    cor = wf.cor_status(e["status"])
                    ev_html += f"<div style='background:{cor};color:white;font-size:9px;padding:2px 4px;border-radius:3px;margin-top:2px;line-height:1.2;overflow:hidden;white-space:nowrap;text-overflow:ellipsis'>{e['titulo'][:18]}</div>"
                if len(evs) > 3:
                    ev_html += f"<div style='font-size:9px;color:{CINZA}'>+{len(evs)-3}</div>"
                bg = "#fff" if not evs else CREME
                cels.append(f"<div style='background:{bg};border:1px solid #e5e7eb;border-radius:6px;padding:4px 5px;min-height:78px'><div style='font-weight:700;font-size:13px;color:{VERDE_PRETO}'>{dia}</div>{ev_html}</div>")
        st.markdown(f"<div style='display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-top:10px'>{hdr}{''.join(cels)}</div>", unsafe_allow_html=True)

    else:  # Lista
        pautas_ord = sorted(pautas, key=lambda x: (x.get("data",""), x.get("hora","")))
        st.caption(f"{len(pautas_ord)} pauta(s)")
        for p in pautas_ord:
            st.markdown(linha_pauta(p), unsafe_allow_html=True)
            cols = st.columns([1.2, 0.8, 2.5, 3.5])
            if cols[0].button("✏️ Editar", key=f"ed_{p['id']}"):
                st.session_state.editar_id = p["id"]
                st.session_state["_pending_nav"] = "➕ Cadastro de pauta"
                st.rerun()
            if cols[1].button("🗑️", key=f"rm_{p['id']}", help="Remover"):
                data.remover(p["id"]); st.rerun()
            url_ag = link_google_agenda(p)
            cols[2].markdown(
                f'<a href="{url_ag}" target="_blank" style="display:inline-block;background:white;'
                f'border:1px solid {VERDE_CLARO};color:{VERDE_PRETO};padding:5px 10px;border-radius:8px;'
                f'text-decoration:none;font-size:12px;font-weight:600">📅 Google Agenda</a>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: FILA DE APROVAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "✅ Fila de aprovação":
    st.markdown(section_title("Fila de aprovação", "vermelho"), unsafe_allow_html=True)
    st.caption("Conteúdos em revisão e aguardando aprovação. Altere status e registre observações.")

    fila = [p for p in data.listar()
            if "revisão" in p["status"] or "Aguardando" in p["status"]]

    if not fila:
        st.markdown('<div class="alerta alerta-verde">✅ Nada na fila. Tudo aprovado ou em produção.</div>',
                    unsafe_allow_html=True)
    else:
        for p in sorted(fila, key=lambda x: x.get("data", "")):
            st.markdown(linha_pauta(p), unsafe_allow_html=True)
            with st.expander(f"Revisar: {p['titulo']}"):
                if p.get("descricao"):
                    st.markdown(f"**Descrição:** {p['descricao']}")
                if p.get("link_rascunho"):
                    st.markdown(f"🔗 [Material/rascunho]({p['link_rascunho']})")
                obs = st.text_area("Observações de revisão", value=p.get("obs_revisao", ""),
                                   key=f"obs_{p['id']}")
                c1, c2, c3 = st.columns(3)
                novo = c1.selectbox("Mudar status", wf.STATUS,
                                    index=wf.STATUS.index(p["status"]), key=f"st_{p['id']}")
                if c2.button("💾 Salvar", key=f"sv_{p['id']}", use_container_width=True):
                    p["obs_revisao"] = obs
                    p["status"] = novo
                    erros = wf.validar(p)
                    if erros:
                        for e in erros: st.error(f"⚠️ {e}")
                    else:
                        data.salvar(p); st.success("✅ Atualizado!"); st.rerun()
                if c3.button("✅ Aprovar e agendar", key=f"ap_{p['id']}", use_container_width=True):
                    p["status"] = "📅 Agendado"
                    p["obs_revisao"] = obs
                    erros = wf.validar(p)
                    if erros:
                        for e in erros: st.error(f"⚠️ {e}")
                    else:
                        data.salvar(p); st.success("✅ Aprovado e agendado!"); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: PUBLICADOS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📤 Publicados":
    st.markdown(section_title("Conteúdos publicados", "verde"), unsafe_allow_html=True)

    pub = [p for p in data.listar() if "Publicado" in p["status"]]
    if not pub:
        st.markdown('<div class="alerta">📭 Nenhum conteúdo publicado ainda.</div>', unsafe_allow_html=True)
    else:
        for p in sorted(pub, key=lambda x: x.get("data_real") or x.get("data"), reverse=True):
            st.markdown(linha_pauta(p), unsafe_allow_html=True)
            with st.expander(f"Pós-publicação: {p['titulo']}"):
                if p.get("link_publicado"):
                    st.markdown(f"🔗 [Post publicado]({p['link_publicado']})")
                m = p.get("metricas", {})
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("👁️ Impressões", m.get("impressoes", 0))
                mc2.metric("💬 Comentários", m.get("comentarios", 0))
                mc3.metric("🖱️ Cliques", m.get("cliques", 0))
                if p.get("obs_pos"):
                    st.markdown(f"**Observações:** {p['obs_pos']}")
                if st.button("✏️ Editar métricas", key=f"edm_{p['id']}"):
                    st.session_state.editar_id = p["id"]
                    st.session_state["_pending_nav"] = "➕ Cadastro de pauta"
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: RELATÓRIOS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "📈 Relatórios":
    st.markdown(section_title("Relatórios", "padrao"), unsafe_allow_html=True)

    pautas = data.listar()
    with st.form("form_rel"):
        c1, c2 = st.columns(2)
        r_de = c1.date_input("De", value=None, format="DD/MM/YYYY")
        r_ate = c2.date_input("Até", value=None, format="DD/MM/YYYY")
        st.form_submit_button("Aplicar período", type="primary")

    def no_periodo(p):
        if r_de and p.get("data", "") < r_de.isoformat(): return False
        if r_ate and p.get("data", "") > r_ate.isoformat(): return False
        return True
    pautas = [p for p in pautas if no_periodo(p)]

    if not pautas:
        st.markdown('<div class="alerta">📭 Sem dados no período.</div>', unsafe_allow_html=True)
    else:
        total = len(pautas)
        pub = sum(1 for p in pautas if "Publicado" in p["status"])
        atr = sum(1 for p in pautas if wf.esta_atrasada(p))
        canc = sum(1 for p in pautas if "Cancelado" in p["status"])
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(card_metrica(total, "Planejadas", VERDE_PRETO), unsafe_allow_html=True)
        c2.markdown(card_metrica(pub, "Publicadas", VERDE_ESC), unsafe_allow_html=True)
        c3.markdown(card_metrica(atr, "Atrasadas", PRIMARIA), unsafe_allow_html=True)
        c4.markdown(card_metrica(canc, "Canceladas", VERMELHO_MED), unsafe_allow_html=True)

        st.markdown(divisor("zig"), unsafe_allow_html=True)
        col_s, col_c = st.columns(2)
        with col_s:
            st.markdown("##### Distribuição por status")
            for s in wf.STATUS:
                n = sum(1 for p in pautas if p["status"] == s)
                if n:
                    pct = int(n/total*100); cor = wf.cor_status(s)
                    st.markdown(f"<div style='margin-bottom:6px'><div style='display:flex;justify-content:space-between;font-size:12px'><span>{s}</span><strong>{n}</strong></div><div style='background:#eee;border-radius:6px;height:8px'><div style='background:{cor};width:{pct}%;height:100%;border-radius:6px'></div></div></div>", unsafe_allow_html=True)
        with col_c:
            st.markdown("##### Distribuição por canal")
            cc = {}
            for p in pautas: cc[p["canal"]] = cc.get(p["canal"], 0) + 1
            for canal, n in sorted(cc.items(), key=lambda x: -x[1]):
                pct = int(n/total*100)
                st.markdown(f"<div style='margin-bottom:6px'><div style='display:flex;justify-content:space-between;font-size:12px'><span>{canal}</span><strong>{n}</strong></div><div style='background:#eee;border-radius:6px;height:8px'><div style='background:{VERDE};width:{pct}%;height:100%;border-radius:6px'></div></div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PÁGINA: MONITOR DE NOTÍCIAS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🔍 Monitor de notícias":
    st.markdown(section_title("Monitor de notícias e tendências", "padrao"), unsafe_allow_html=True)
    st.caption("Busca notícias atuais sobre os temas da UNIVAJA. Use antes da reunião de pauta.")

    from urllib.parse import quote_plus
    TEMAS = {
        "Vale do Javari": ["Vale do Javari", "UNIVAJA", "Atalaia do Norte"],
        "Povos isolados": ["povos isolados Amazônia", "indígenas isolados FUNAI"],
        "Garimpo / invasão": ["garimpo ilegal Amazônia", "invasão terra indígena"],
        "Direitos indígenas": ["marco temporal indígena", "demarcação terra indígena"],
        "Bruno e Dom": ["Bruno Pereira Dom Phillips"],
        "Meio ambiente": ["desmatamento Amazônia", "Dia da Amazônia"],
    }
    sel = []
    cols = st.columns(3)
    for i, (t, termos) in enumerate(TEMAS.items()):
        if cols[i % 3].checkbox(t, key=f"mon_{t}"):
            sel.extend(termos)
    extra = st.text_input("Termo extra (opcional)")
    if extra: sel.append(extra)
    if not sel:
        sel = ["Vale do Javari", "UNIVAJA"]

    q = quote_plus(" OR ".join([f'"{t}"' for t in sel[:5]]))
    url_news = f"https://news.google.com/search?q={q}&hl=pt-BR&gl=BR&ceid=BR:pt-BR&as_qdr=w"
    url_search = f"https://www.google.com/search?q={q}&tbm=nws&hl=pt-BR&tbs=qdr:w,sbd:1"
    url_trends = f"https://trends.google.com/trends/explore?q={quote_plus(','.join(sel[:5]))}&geo=BR&date=now%207-d&hl=pt-BR"

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<a href="{url_news}" target="_blank" class="link-google"><div class="link-google-conteudo"><div class="link-google-titulo">{logo_google_noticias(20)}</div><div class="link-google-desc">Notícias da semana</div></div><div class="link-google-seta">→</div></a>', unsafe_allow_html=True)
    c2.markdown(f'<a href="{url_search}" target="_blank" class="link-google"><div class="link-google-conteudo"><div class="link-google-titulo">{logo_google_search(20)}</div><div class="link-google-desc">Mais recentes (por data)</div></div><div class="link-google-seta">→</div></a>', unsafe_allow_html=True)
    c3.markdown(f'<a href="{url_trends}" target="_blank" class="link-google"><div class="link-google-conteudo"><div class="link-google-titulo">{logo_google_trends(20)}</div><div class="link-google-desc">Tendências no Brasil</div></div><div class="link-google-seta">→</div></a>', unsafe_allow_html=True)
