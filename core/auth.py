"""
Login interno simples para a Central Editorial UNIVAJA.

Segurança mínima adequada a uma equipe pequena:
- senhas NUNCA são guardadas em texto puro — apenas o hash SHA-256
- usuários ficam em st.secrets["auth"] (Streamlit Cloud) ou no dict padrão
- a sessão guarda apenas o estado de autenticação (usuário logado)

Para gerar o hash de uma senha nova, rode no terminal:
    python -c "import hashlib; print(hashlib.sha256('MINHA_SENHA'.encode()).hexdigest())"
"""

import hashlib
import streamlit as st


# Usuários padrão (rodam sem configurar nada). TROQUE as senhas em produção
# via st.secrets. Senhas padrão: admin/univaja2026 · fran/fran2026 · imprensa/imprensa2026
USUARIOS_PADRAO = {
    "admin":    "c0e8f75259dc2285d3d23dd4de519900a3419f7d5cae1c5e0ebefb0ab89b294b",
    "fran":     "3bcf148c1788a5327ca23eedb845f31f39035338f5063553cb5cfc6bbc611f73",
    "imprensa": "89e07a5d4e1c8ab24289eac545eeae4dec39d740125f61880938875a7b319e40",
}


def _hash(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def _carregar_usuarios() -> dict:
    """Lê usuários de st.secrets['auth'] se existir; senão usa o padrão."""
    try:
        if "auth" in st.secrets:
            # Em secrets.toml:  [auth]  fran = "<sha256>"  ...
            return dict(st.secrets["auth"])
    except Exception:
        pass
    return USUARIOS_PADRAO


def esta_logado() -> bool:
    return bool(st.session_state.get("auth_user"))


def usuario_atual() -> str:
    return st.session_state.get("auth_user", "")


def logout():
    st.session_state.pop("auth_user", None)


def login(usuario: str, senha: str) -> bool:
    """Valida credenciais. Retorna True se ok e marca a sessão."""
    usuarios = _carregar_usuarios()
    u = (usuario or "").strip().lower()
    if u in usuarios and usuarios[u] == _hash(senha):
        st.session_state["auth_user"] = u
        return True
    return False


def tela_login(render_header) -> bool:
    """
    Renderiza a tela de login. Retorna True se o usuário está autenticado.
    `render_header` é uma função que desenha o cabeçalho institucional.
    """
    if esta_logado():
        return True

    render_header()

    col_esq, col_meio, col_dir = st.columns([1, 1.3, 1])
    with col_meio:
        st.markdown("### 🔑 Acesso à Central Editorial")
        st.caption("Área de uso interno da ASCOM UNIVAJA.")

        with st.form("form_login"):
            usuario = st.text_input("Usuário", placeholder="ex: fran")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", type="primary", use_container_width=True)

            if entrar:
                if login(usuario, senha):
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")

        with st.expander("ℹ️ Primeiro acesso / senhas padrão"):
            st.markdown("""
            **Usuários de teste** (troque depois em `st.secrets`):
            - `admin` / `univaja2026`
            - `fran` / `fran2026`
            - `imprensa` / `imprensa2026`

            Para definir usuários reais com segurança, crie em **Settings → Secrets**
            do Streamlit Cloud:
            ```toml
            [auth]
            fran = "<hash sha256 da senha>"
            tumi = "<hash sha256 da senha>"
            ```
            """)
    return False
