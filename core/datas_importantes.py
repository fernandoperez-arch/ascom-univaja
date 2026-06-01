"""
Calendário de datas importantes para a UNIVAJA e os povos do Vale do Javari.

Datas pesquisadas e conferidas (maio/2026). As marcadas como `sensivel=True`
exigem validação da Coordenação + Procuradoria antes de publicar.

Cada data traz uma sugestão de POST (texto de exemplo) e o formato recomendado,
para a equipe já sair da reunião com o material encaminhado.

Fontes principais: univaja.org, Equator Initiative (homologação TI 02/05/2001),
National Geographic / Wikipédia (Dia Internacional da Mulher Indígena, 05/09).
"""

from datetime import date

# data = "MM-DD"
DATAS_UNIVAJA = [
    {
        "data": "01-28", "titulo": "Dia do Pajé",
        "categoria": "Cultura indígena", "formato": "Card / Carrossel",
        "prioridade": "🔵 Normal", "sensivel": False,
        "exemplo": "Os pajés guardam o conhecimento ancestral, a cura e a espiritualidade "
                   "dos povos do Vale do Javari. Hoje celebramos quem mantém viva a sabedoria "
                   "que atravessa gerações. 🌿 #UNIVAJA #ValeDoJavari #PovosIndígenas",
    },
    {
        "data": "03-08", "titulo": "Dia Internacional da Mulher",
        "categoria": "Mulheres indígenas", "formato": "Carrossel / Reels",
        "prioridade": "🟡 Alta", "sensivel": False,
        "exemplo": "Às mulheres indígenas do Vale do Javari — que cuidam, lideram, curam e "
                   "resistem. A força das nossas associações de base tem rosto de mulher. "
                   "💪 #MulheresIndígenas #UNIVAJA #ValeDoJavari",
    },
    {
        "data": "03-21", "titulo": "Dia Internacional das Florestas + Combate à Discriminação Racial",
        "categoria": "Ambiental / Direitos", "formato": "Card",
        "prioridade": "🔵 Normal", "sensivel": False,
        "exemplo": "A floresta em pé é a nossa casa, nossa farmácia e nosso futuro. Proteger "
                   "o território é proteger a vida. 🌳 #DiaDasFlorestas #Amazônia #UNIVAJA",
    },
    {
        "data": "03-22", "titulo": "Dia Mundial da Água",
        "categoria": "Ambiental", "formato": "Card",
        "prioridade": "🔵 Normal", "sensivel": False,
        "exemplo": "Os rios do Vale do Javari são caminho, alimento e vida. Defender as águas "
                   "é defender os povos que delas dependem. 💧 #DiaDaÁgua #ValeDoJavari #UNIVAJA",
    },
    {
        "data": "04-19", "titulo": "Dia dos Povos Indígenas (Brasil) — Abril Indígena / ATL",
        "categoria": "Indígena nacional · DATA MAIOR", "formato": "Campanha (card + vídeo + boletim)",
        "prioridade": "🟡 Alta", "sensivel": False,
        "exemplo": "Não é 'dia do índio'. É o Dia dos POVOS Indígenas — no plural, porque somos "
                   "muitos: Marubo, Matís, Kanamari, Kulina, Mayoruna e os povos isolados do Vale "
                   "do Javari. Nossa existência é resistência. ✊ #DiaDosPovosIndígenas #UNIVAJA "
                   "#ValeDoJavari #AbrilIndígena",
    },
    {
        "data": "04-22", "titulo": "Dia da Terra",
        "categoria": "Ambiental", "formato": "Card / Carrossel",
        "prioridade": "🔵 Normal", "sensivel": False,
        "exemplo": "A maior concentração de povos isolados do mundo está aqui, no Vale do Javari. "
                   "Quando protegemos a Terra, protegemos quem o mundo nem sempre vê. 🌎 "
                   "#DiaDaTerra #Amazônia #UNIVAJA",
    },
    {
        "data": "05-02", "titulo": "Homologação da Terra Indígena Vale do Javari (2001)",
        "categoria": "UNIVAJA · DATA MAIOR", "formato": "Vídeo + Carrossel histórico",
        "prioridade": "🟡 Alta", "sensivel": False,
        "exemplo": "Em 2 de maio de 2001, após mais de 20 anos de luta, conquistamos a "
                   "homologação da Terra Indígena Vale do Javari: 8,5 milhões de hectares, a "
                   "segunda maior TI do Brasil. A demarcação foi vitória dos povos — e seguimos "
                   "defendendo cada palmo dela. 🏹 #ValeDoJavari #UNIVAJA #TerraDemarcada",
    },
    {
        "data": "05-22", "titulo": "Dia Internacional da Biodiversidade",
        "categoria": "Ambiental", "formato": "Card",
        "prioridade": "🟢 Baixa", "sensivel": False,
        "exemplo": "O Vale do Javari abriga uma das maiores sociobiodiversidades do planeta. "
                   "Cada povo, cada língua, cada saber é parte dessa riqueza viva. 🦜🌿 "
                   "#Biodiversidade #Amazônia #UNIVAJA",
    },
    {
        "data": "06-05", "titulo": "Bruno e Dom (memória) + Dia Mundial do Meio Ambiente",
        "categoria": "Memória · DATA MAIOR", "formato": "Card único nas 3 redes (simultâneo)",
        "prioridade": "🔴 Urgente", "sensivel": True,
        "exemplo": "Bruno Pereira e Dom Phillips foram assassinados no Vale do Javari em 5 de "
                   "junho de 2022. A UNIVAJA não esquece, não cala, não recua. Sua luta é a "
                   "nossa luta: território protegido, vidas respeitadas. 🕯️ "
                   "#BrunoEDom #ValeDoJavari #UNIVAJA  "
                   "⚠️ VALIDAR com Coordenação + Procuradoria antes de publicar.",
    },
    {
        "data": "06-17", "titulo": "Dia Mundial de Combate à Desertificação e à Seca",
        "categoria": "Ambiental", "formato": "Card",
        "prioridade": "🟢 Baixa", "sensivel": False,
        "exemplo": "A crise climática chega ao Javari na forma de secas extremas e rios baixos. "
                   "Os povos da floresta sentem primeiro o que o mundo demora a enxergar. 🌍 "
                   "#Clima #Amazônia #UNIVAJA",
    },
    {
        "data": "08-09", "titulo": "Dia Internacional dos Povos Indígenas (ONU)",
        "categoria": "Internacional · DATA MAIOR", "formato": "Card bilíngue + Vídeo legendado",
        "prioridade": "🟡 Alta", "sensivel": False,
        "exemplo": "Do Vale do Javari para o mundo: os povos indígenas são guardiões de "
                   "territórios essenciais para o equilíbrio do planeta. Nossa voz é global. 🌐 "
                   "#IndigenousPeoplesDay #PovosIndígenas #UNIVAJA #ValeDoJavari",
    },
    {
        "data": "09-05", "titulo": "Dia da Amazônia",
        "categoria": "Ambiental · DATA MAIOR", "formato": "Carrossel + Vídeo curto",
        "prioridade": "🟡 Alta", "sensivel": False,
        "exemplo": "A Amazônia não é vazio: é território de povos, línguas e modos de vida. Os "
                   "povos isolados do Vale do Javari são prova de que a floresta tem dono — e "
                   "tem guardiões. 🌳 #DiaDaAmazônia #ValeDoJavari #UNIVAJA",
    },
    {
        "data": "09-05", "titulo": "Dia Internacional da Mulher Indígena",
        "categoria": "Mulheres indígenas · DATA MAIOR", "formato": "Reels / Carrossel",
        "prioridade": "🟡 Alta", "sensivel": False,
        "exemplo": "5 de setembro: em memória de Bartolina Sisa e de todas as mulheres "
                   "indígenas que resistem. No Vale do Javari, elas seguram a luta, a cultura e "
                   "o futuro dos povos. 💜 #MulherIndígena #UNIVAJA #ValeDoJavari",
    },
    {
        "data": "10-12", "titulo": "Dia da Resistência Indígena",
        "categoria": "Indígena · histórico", "formato": "Vídeo / Reels",
        "prioridade": "🔵 Normal", "sensivel": False,
        "exemplo": "Mais de 500 anos depois, seguimos aqui. A resistência dos povos do Vale do "
                   "Javari é diária: na língua que se fala, no rio que se navega, na floresta que "
                   "se protege. ✊ #ResistênciaIndígena #UNIVAJA #ValeDoJavari",
    },
    {
        "data": "11-20", "titulo": "Dia da Consciência Negra",
        "categoria": "Aliança / Direitos", "formato": "Card",
        "prioridade": "🔵 Normal", "sensivel": False,
        "exemplo": "Povos indígenas e povos negros: territórios diferentes, luta comum por "
                   "direitos, terra e dignidade. Solidariedade entre quem resiste. 🤝 "
                   "#ConsciênciaNegra #UNIVAJA",
    },
    {
        "data": "12-10", "titulo": "Dia dos Direitos Humanos",
        "categoria": "Direitos · atenção", "formato": "Card / Nota oficial",
        "prioridade": "🟡 Alta", "sensivel": True,
        "exemplo": "Direito ao território, à vida e à autodeterminação. No Vale do Javari, "
                   "defender direitos humanos é também defender quem nunca quis contato com o "
                   "mundo de fora. 📜 #DireitosHumanos #UNIVAJA #ValeDoJavari  "
                   "⚠️ Se citar violações/denúncias, validar com a Procuradoria.",
    },
]


def _prox_ocorrencia(mmdd: str, hoje: date) -> date:
    m, d = int(mmdd[:2]), int(mmdd[3:])
    try:
        dt = date(hoje.year, m, d)
    except ValueError:
        return date(hoje.year, m, 28)
    if dt < hoje:
        try:
            dt = date(hoje.year + 1, m, d)
        except ValueError:
            dt = date(hoje.year + 1, m, 28)
    return dt


def proximas(dias: int = 90, hoje: date = None):
    """Retorna [(dias_restantes, data_real, entrada)] dentro da janela, ordenado."""
    hoje = hoje or date.today()
    out = []
    for e in DATAS_UNIVAJA:
        dt = _prox_ocorrencia(e["data"], hoje)
        delta = (dt - hoje).days
        if 0 <= delta <= dias:
            out.append((delta, dt, e))
    return sorted(out, key=lambda x: x[0])


def como_pautas(ano: int) -> list:
    """Converte as datas em pautas (schema de core.data) para semear na agenda."""
    from core import data as _data
    pautas = []
    for e in DATAS_UNIVAJA:
        m, d = int(e["data"][:2]), int(e["data"][3:])
        try:
            dt = date(ano, m, d)
        except ValueError:
            dt = date(ano, m, 28)
        p = _data.nova_pauta()
        formato = e["formato"].split("/")[0].split("(")[0].strip()
        p.update({
            "titulo": e["titulo"],
            "descricao": e["exemplo"],
            "canal": "Instagram",
            "formato": formato if formato else "Card único",
            "data": dt.isoformat(),
            "status": "💡 Ideia",
            "prioridade": e["prioridade"],
            "campanha": "Datas comemorativas",
            "objetivo": e["categoria"],
            "obs_internas": ("⚠️ TEMA SENSÍVEL — validar com Coordenação + Procuradoria. "
                             if e["sensivel"] else "") + "Data fixa do calendário UNIVAJA.",
        })
        pautas.append(p)
    return pautas
