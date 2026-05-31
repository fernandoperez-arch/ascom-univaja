"""
Camada de dados da Central Editorial UNIVAJA.

ESTRATÉGIA (escolha: Streamlit Community Cloud)
-----------------------------------------------
O disco do Streamlit Cloud é efêmero, então os dados vivem em st.session_state
e são preservados via backup JSON (download/upload na sidebar).

A camada está ISOLADA aqui de propósito: quando você criar um Supabase
(Postgres grátis), basta implementar as 4 funções marcadas com [SUPABASE-HOOK]
lendo st.secrets["supabase"] — o resto do app não muda.

Cada pauta é um dict com o schema de `nova_pauta()`.
"""

from datetime import datetime, date
import uuid
import json
import streamlit as st


# ─── Schema ──────────────────────────────────────────────────────────────────
def nova_pauta() -> dict:
    return {
        "id": str(uuid.uuid4())[:8],
        "titulo": "",
        "descricao": "",
        "canal": "Instagram",
        "formato": "Card único",
        "responsavel": "",
        "aprovador": "",
        "data": date.today().isoformat(),
        "hora": "09:00",
        "status": "💡 Ideia",
        "prioridade": "🔵 Normal",
        "campanha": "",
        "publico": "",
        "objetivo": "",
        "link_rascunho": "",
        "link_publicado": "",
        "data_real": "",
        "obs_internas": "",
        "obs_pos": "",
        "obs_revisao": "",
        "metricas": {"impressoes": 0, "comentarios": 0, "cliques": 0},
        "criado_em": datetime.now().isoformat(),
        "criado_por": st.session_state.get("auth_user", ""),
    }


# ─── Acesso (session_state) ──────────────────────────────────────────────────
def _bootstrap():
    if "pautas" not in st.session_state:
        st.session_state.pautas = []


def listar() -> list:
    _bootstrap()
    return st.session_state.pautas


def obter(pid: str):
    return next((p for p in listar() if p["id"] == pid), None)


def salvar(pauta: dict):
    _bootstrap()
    idx = next((i for i, p in enumerate(st.session_state.pautas) if p["id"] == pauta["id"]), None)
    pauta["atualizado_em"] = datetime.now().isoformat()
    if idx is None:
        st.session_state.pautas.append(pauta)
    else:
        st.session_state.pautas[idx] = pauta
    _persistir()  # [SUPABASE-HOOK] gravar no banco


def remover(pid: str):
    _bootstrap()
    st.session_state.pautas = [p for p in st.session_state.pautas if p["id"] != pid]
    _persistir()


# ─── Persistência / backup ───────────────────────────────────────────────────
def exportar_json() -> str:
    return json.dumps(listar(), ensure_ascii=False, indent=2)


def importar_json(conteudo, substituir=True) -> int:
    _bootstrap()
    dados = json.loads(conteudo)
    if not isinstance(dados, list):
        raise ValueError("JSON inválido — esperado uma lista de pautas.")
    if substituir:
        st.session_state.pautas = dados
    else:
        ids = {p["id"] for p in st.session_state.pautas}
        for p in dados:
            if p.get("id") not in ids:
                st.session_state.pautas.append(p)
    _persistir()
    return len(dados)


def _persistir():
    """
    [SUPABASE-HOOK] Hoje não faz nada (dados ficam na sessão; backup é manual).
    Para ativar Supabase: detectar st.secrets['supabase'] e dar UPSERT na tabela
    'pautas'. As funções listar/salvar/remover passariam a ler/gravar lá.
    """
    return


# ─── Seed opcional (dados de exemplo no primeiro uso) ────────────────────────
def carregar_exemplos():
    exemplos = [
        {**nova_pauta(),
         "titulo": "Card: 4 anos sem Bruno e Dom",
         "descricao": "Memória ativa — tom respeitoso e firme.",
         "canal": "Instagram", "formato": "Card único",
         "responsavel": "Tumi", "aprovador": "Coordenação",
         "status": "⏳ Aguardando aprovação", "prioridade": "🔴 Urgente",
         "campanha": "Datas sensíveis", "publico": "Geral + imprensa",
         "objetivo": "Memória e denúncia",
         "obs_internas": "Validar com Procuradoria antes."},
        {**nova_pauta(),
         "titulo": "Série Associações de Base — parte 3",
         "descricao": "Apresentar a associação e suas lideranças.",
         "canal": "Instagram", "formato": "Carrossel",
         "responsavel": "Fran", "status": "🎨 Em produção",
         "prioridade": "🔵 Normal", "campanha": "Associações"},
    ]
    st.session_state.pautas = exemplos
    _persistir()
