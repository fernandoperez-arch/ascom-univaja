"""
Geração de link 'Adicionar ao Google Agenda' (versão simples, sem credenciais).

Limitação honesta: a URL-template do Google Calendar NÃO aceita lembretes
customizados. Por isso os lembretes de 15 e 7 dias entram como instrução na
descrição do evento. Para lembretes 100% automáticos, é preciso a Calendar API
(Service Account) — ver core/calendar_api.py (futuro upgrade).
"""

from datetime import datetime, timedelta
from urllib.parse import quote


def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")


def link_google_agenda(pauta: dict, duracao_min: int = 60,
                       email_dono: str = "imprensa@univaja.org") -> str:
    """Monta a URL que abre o Google Agenda com o evento pré-preenchido."""
    titulo = f"[UNIVAJA] {pauta.get('titulo','Pauta')}"

    # Data/hora de início
    try:
        d = pauta.get("data")
        h = pauta.get("hora") or "09:00"
        inicio = datetime.fromisoformat(f"{d}T{h}:00")
    except Exception:
        inicio = datetime.now()
    fim = inicio + timedelta(minutes=duracao_min)

    descricao = (
        f"Pauta editorial UNIVAJA\n\n"
        f"Canal: {pauta.get('canal','')}\n"
        f"Formato: {pauta.get('formato','')}\n"
        f"Responsável: {pauta.get('responsavel','')}\n"
        f"Aprovador: {pauta.get('aprovador','')}\n"
        f"Status: {pauta.get('status','')}\n"
        f"Prioridade: {pauta.get('prioridade','')}\n"
        f"Objetivo: {pauta.get('objetivo','')}\n"
        f"Link do material: {pauta.get('link_rascunho','-')}\n\n"
        f"⏰ LEMBRETES RECOMENDADOS: 15 dias antes e 7 dias antes.\n"
        f"(Configure em 'Notificação' ao salvar o evento.)\n\n"
        f"Dono da agenda: {email_dono}"
    )

    params = (
        "https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text={quote(titulo)}"
        f"&dates={_fmt(inicio)}/{_fmt(fim)}"
        f"&details={quote(descricao)}"
        f"&ctz=America/Sao_Paulo"
    )
    return params
