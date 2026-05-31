"""
Workflow editorial da Central UNIVAJA — status, cores, regras e validações.
"""

from datetime import date, datetime

# Importa a paleta da marca para as cores de status
from univaja_brand import (
    PRIMARIA, VERMELHO_ESC, VERMELHO_MED, VERDE, VERDE_ESC, VERDE_PRETO, VERDE_CLARO, CINZA,
)

# ─── Status (ordem do fluxo) ─────────────────────────────────────────────────
STATUS = [
    "💡 Ideia",
    "📋 Pauta aprovada",
    "🎨 Em produção",
    "🔍 Em revisão",
    "⏳ Aguardando aprovação",
    "📅 Agendado",
    "✅ Publicado",
    "❌ Cancelado",
]

# Cores discretas por status (conforme briefing do cliente)
STATUS_COR = {
    "💡 Ideia":                 "#9ca3af",   # neutro
    "📋 Pauta aprovada":        "#7BA87F",   # verde claro
    "🎨 Em produção":           "#2563eb",   # azul
    "🔍 Em revisão":            "#d4a017",   # amarelo
    "⏳ Aguardando aprovação":  "#e67e22",   # laranja
    "📅 Agendado":              VERDE,        # verde
    "✅ Publicado":             VERDE_PRETO,  # verde escuro
    "❌ Cancelado":             VERMELHO_MED, # vermelho discreto
}

PRIORIDADES = ["🟢 Baixa", "🔵 Normal", "🟡 Alta", "🔴 Urgente"]
PRIORIDADE_COR = {
    "🟢 Baixa": "#7BA87F", "🔵 Normal": VERDE,
    "🟡 Alta": "#e67e22", "🔴 Urgente": PRIMARIA,
}

CANAIS = ["Instagram", "Facebook", "LinkedIn", "WhatsApp",
          "YouTube", "TikTok", "Site UNIVAJA", "Imprensa"]

FORMATOS = ["Card único", "Carrossel", "Vídeo / Reels", "Stories",
            "Boletim interno", "Release", "Nota oficial", "Artigo", "Live", "Podcast / Áudio"]


def cor_status(status: str) -> str:
    return STATUS_COR.get(status, CINZA)


def badge_status(status: str) -> str:
    """HTML de badge para um status."""
    cor = cor_status(status)
    return (f'<span style="background:{cor}1a;color:{cor};border:1px solid {cor};'
            f'padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;'
            f'white-space:nowrap">{status}</span>')


def badge_prioridade(prioridade: str) -> str:
    cor = PRIORIDADE_COR.get(prioridade, CINZA)
    return (f'<span style="background:{cor}1a;color:{cor};border:1px solid {cor};'
            f'padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700;'
            f'white-space:nowrap">{prioridade}</span>')


# ─── Validações / regras operacionais ───────────────────────────────────────
def validar(pauta: dict) -> list:
    """Retorna lista de erros que impedem o status atual. Vazio = ok."""
    erros = []
    s = pauta.get("status", "")

    if "Agendado" in s:
        if not pauta.get("data") or not pauta.get("hora"):
            erros.append("Para **Agendado**, defina data E hora.")

    if "Publicado" in s:
        if not pauta.get("link_publicado", "").strip():
            erros.append("Para **Publicado**, informe o link final do post.")

    return erros


def esta_atrasada(pauta: dict) -> bool:
    """Pauta com data no passado e ainda não publicada/cancelada."""
    s = pauta.get("status", "")
    if "Publicado" in s or "Cancelado" in s:
        return False
    try:
        return date.fromisoformat(pauta["data"]) < date.today()
    except Exception:
        return False


def dias_para(pauta: dict):
    try:
        return (date.fromisoformat(pauta["data"]) - date.today()).days
    except Exception:
        return None


def esta_proxima(pauta: dict, janela=7) -> bool:
    s = pauta.get("status", "")
    if "Publicado" in s or "Cancelado" in s:
        return False
    d = dias_para(pauta)
    return d is not None and 0 <= d <= janela
