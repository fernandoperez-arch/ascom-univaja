# Central Editorial UNIVAJA

Sistema interno de gestão de conteúdo da ASCOM (Streamlit).

## Como publicar no Streamlit Cloud
1. Em [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Repositório: `fernandoperez-arch/ascom-univaja`
3. **Main file path:** `central_univaja.py`
4. Deploy.

## Login
Usuários de teste (troque em produção):
- `admin` / `univaja2026`
- `fran` / `fran2026`
- `imprensa` / `imprensa2026`

Para definir usuários reais com segurança, em **Settings → Secrets** do app:
```toml
[auth]
fran = "<hash sha256 da senha>"
tumi = "<hash sha256 da senha>"
```
Gerar um hash:
```bash
python -c "import hashlib; print(hashlib.sha256('MINHA_SENHA'.encode()).hexdigest())"
```
As senhas **nunca** são guardadas em texto puro — só o hash.

## Dados (persistência)
No Streamlit Cloud o disco é efêmero. Hoje os dados ficam na **sessão** e são
preservados via **backup JSON** (botões na barra lateral: baixar / restaurar).

**Upgrade recomendado (Supabase, grátis e persistente):**
1. Crie um projeto em [supabase.com](https://supabase.com)
2. Copie a connection string em **Settings → Secrets**:
   ```toml
   [supabase]
   url = "..."
   key = "..."
   ```
3. Implemente os 4 hooks marcados `[SUPABASE-HOOK]` em `core/data.py`.
   O resto do app não muda.

## Google Agenda — lembretes automáticos de 15 e 7 dias
Há dois modos:

**A) Modo simples (sem configurar nada)** — botão `📅 Google Agenda` por pauta,
que abre o Calendar já preenchido. Lembretes 15/7 dias ficam escritos na descrição.

**B) Modo automático (recomendado)** — via Calendar API, cria/atualiza o evento na
agenda da `imprensa@univaja.org` com lembretes por **e-mail + popup a 15 dias
(21.600 min) e 7 dias (10.080 min)**. Botões `📆 Agendar (15/7d)` e
`📆 Sincronizar agendadas`.

### Configurar o modo automático (uma vez)
1. **console.cloud.google.com** → crie um projeto (ex: `univaja-agenda`).
2. **APIs e Serviços** → ative a **Google Calendar API**.
3. **Credenciais → Criar → Conta de serviço** → gere e baixe a chave **JSON**.
4. Abra o **Google Agenda da imprensa@univaja.org** → *Configurações da agenda* →
   *Compartilhar com pessoas específicas* → adicione o **e-mail da conta de serviço**
   (`...@....iam.gserviceaccount.com`) com permissão **"Fazer alterações nos eventos"**.
5. No app: **⋮ → Settings → Secrets**, cole:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "..."
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "...@....iam.gserviceaccount.com"
   client_id = "..."
   token_uri = "https://oauth2.googleapis.com/token"

   [gcal]
   calendar_id = "imprensa@univaja.org"
   ```
Pronto — a sidebar passa a mostrar "✅ Conectada" e os botões de sincronizar aparecem.

> O e-mail de lembrete chega para o **dono da agenda** (imprensa@univaja.org).
> A Google Agenda é **espelho** da pauta — a base principal é a Central.

## Estrutura
```
central_univaja.py      app principal (login + navegação + páginas)
univaja_brand.py        identidade visual (cores, grafismos, logo)
core/auth.py            login com hash
core/data.py            camada de dados (sessão → Supabase)
core/workflow.py        status, regras, validações
core/calendar_link.py   link Google Agenda
```

## Workflow editorial
`💡 Ideia → 📋 Pauta aprovada → 🎨 Em produção → 🔍 Em revisão →
⏳ Aguardando aprovação → 📅 Agendado → ✅ Publicado` (+ `❌ Cancelado`)

Regras: não vai a **Agendado** sem data+hora; não vai a **Publicado** sem link final.

## Apps anteriores (ainda no repo)
`ascom_univaja.py`, `monitor_univaja.py`, `planner_univaja.py` continuam
funcionando. A Central Editorial consolida o fluxo num só lugar.
