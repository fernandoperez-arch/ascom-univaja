"""
Integração com a Google Calendar API (lembretes automáticos de 15 e 7 dias).

Cria/atualiza um evento na agenda da imprensa@univaja.org para cada pauta agendada,
com lembretes por E-MAIL e POPUP a 15 dias (21.600 min) e 7 dias (10.080 min) do evento.

A Google Agenda é ESPELHO da pauta — a base principal continua sendo a Central.

────────────────────────────────────────────────────────────────────────────
CONFIGURAÇÃO (uma vez, feita pela UNIVAJA)
────────────────────────────────────────────────────────────────────────────
1. Em console.cloud.google.com → crie um projeto (ex: "univaja-agenda").
2. APIs e Serviços → ative a "Google Calendar API".
3. Credenciais → Criar credencial → Conta de serviço. Baixe o JSON.
4. Abra o Google Agenda da imprensa@univaja.org → Configurações da agenda →
   "Compartilhar com pessoas específicas" → adicione o e-mail da conta de
   serviço (algo como nome@projeto.iam.gserviceaccount.com) com permissão
   "Fazer alterações nos eventos".
5. No app Streamlit → Settings → Secrets, cole o conteúdo do JSON assim:

   [gcp_service_account]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
   client_email = "...@....iam.gserviceaccount.com"
   client_id = "..."
   token_uri = "https://oauth2.googleapis.com/token"

   [gcal]
   calendar_id = "imprensa@univaja.org"

Pronto. O botão "Sincronizar com Google Agenda" passa a funcionar.
"""

from datetime import datetime, timedelta
import streamlit as st

# Lembretes pedidos: 15 e 7 dias antes (em minutos)
MIN_15_DIAS = 15 * 24 * 60   # 21.600
MIN_7_DIAS = 7 * 24 * 60     # 10.080
TIMEZONE = "America/Sao_Paulo"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def esta_configurado() -> bool:
    try:
        return "gcp_service_account" in st.secrets
    except Exception:
        return False


def _calendar_id() -> str:
    try:
        return st.secrets.get("gcal", {}).get("calendar_id", "imprensa@univaja.org")
    except Exception:
        return "imprensa@univaja.org"


@st.cache_resource(show_spinner=False)
def _servico():
    """Cria o cliente da Calendar API a partir da service account em secrets."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    info = dict(st.secrets["gcp_service_account"])
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def _evento_payload(p: dict) -> dict:
    """Monta o corpo do evento com os lembretes de 15 e 7 dias."""
    try:
        inicio = datetime.fromisoformat(f"{p['data']}T{(p.get('hora') or '09:00')}:00")
    except Exception:
        inicio = datetime.now()
    fim = inicio + timedelta(hours=1)

    descricao = (
        f"Pauta editorial UNIVAJA\n\n"
        f"Canal: {p.get('canal','')}\n"
        f"Formato: {p.get('formato','')}\n"
        f"Responsável: {p.get('responsavel','')}\n"
        f"Aprovador: {p.get('aprovador','')}\n"
        f"Status: {p.get('status','')}\n"
        f"Prioridade: {p.get('prioridade','')}\n"
        f"Objetivo: {p.get('objetivo','')}\n"
        f"Campanha: {p.get('campanha','')}\n"
        f"Link do material: {p.get('link_rascunho','-')}\n\n"
        f"(Sincronizado pela Central Editorial UNIVAJA · ID {p.get('id','')})"
    )

    return {
        "summary": f"[UNIVAJA] {p.get('titulo','Pauta')}",
        "description": descricao,
        "start": {"dateTime": inicio.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": fim.isoformat(), "timeZone": TIMEZONE},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": MIN_15_DIAS},
                {"method": "popup", "minutes": MIN_15_DIAS},
                {"method": "email", "minutes": MIN_7_DIAS},
                {"method": "popup", "minutes": MIN_7_DIAS},
            ],
        },
    }


def sincronizar(p: dict) -> dict:
    """
    Cria (ou atualiza, se já tiver gcal_event_id) o evento da pauta.
    Retorna {'ok': bool, 'event_id': str, 'link': str, 'erro': str}.
    """
    if not esta_configurado():
        return {"ok": False, "erro": "Google Agenda não configurada (ver instruções)."}

    try:
        service = _servico()
        cal_id = _calendar_id()
        body = _evento_payload(p)
        ev_id = p.get("gcal_event_id")

        if ev_id:
            ev = service.events().update(calendarId=cal_id, eventId=ev_id, body=body).execute()
        else:
            ev = service.events().insert(calendarId=cal_id, body=body).execute()

        return {"ok": True, "event_id": ev.get("id", ""),
                "link": ev.get("htmlLink", ""), "erro": ""}
    except Exception as ex:
        return {"ok": False, "erro": str(ex)}


def remover(p: dict) -> bool:
    if not esta_configurado() or not p.get("gcal_event_id"):
        return False
    try:
        _servico().events().delete(calendarId=_calendar_id(),
                                    eventId=p["gcal_event_id"]).execute()
        return True
    except Exception:
        return False
