"""
UNIVAJA — Sistema de identidade visual
Cores e grafismos do manual de marca, prontos para uso em Streamlit.

Grafismos inspirados nos padrões dos povos do Vale do Javari:
- Marubo (meander/labirinto) — costas, barriga, pernas
- Matis (losangos com eixo pontilhado)
- Kanamari (ziguezague vermelho/preto, pontos)
- Kulina (triângulos com pontos, chevrons)
- Mayuruna (Macubo: retângulos; Bedibo: círculos)
"""

from urllib.parse import quote

# ─── CORES (manual de marca UNIVAJA) ─────────────────────────────────────────
PRIMARIA      = "#DC3637"  # vermelho UNIVAJA
VERMELHO_ESC  = "#780B0B"
VERMELHO_MED  = "#B6352E"
VERMELHO_CLARO= "#E58D8D"

VERDE         = "#547658"
VERDE_ESC     = "#384E3A"
VERDE_PRETO   = "#1F2A21"
VERDE_CLARO   = "#99E19E"

CINZA         = "#494949"
PRETO         = "#222221"
BRANCO        = "#FFFFFF"
CREME         = "#F7F3EC"     # off-white para fundos
VERDE_FUNDO   = "#F0F5F1"     # verde claro institucional
VERMELHO_FUNDO= "#FCE8E8"     # vermelho claro de apoio


def svg_to_url(svg: str) -> str:
    """Converte um SVG string em data URL para usar em CSS."""
    return "data:image/svg+xml;utf8," + quote(svg)


# ─── GRAFISMOS (SVG patterns) ────────────────────────────────────────────────

# Marubo — meander/labirinto retangular (greek key adaptado)
# Uso: header, faixas decorativas, divisores grandes
def grafismo_marubo(cor=PRIMARIA, fundo="transparent", altura=24):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 {altura}" preserveAspectRatio="xMidYMid slice">
<rect width="48" height="{altura}" fill="{fundo}"/>
<path d="M0,{altura-2} L0,4 L8,4 L8,12 L4,12 L4,8 L12,8 L12,16 L20,16 L20,4 L28,4 L28,16 L36,16 L36,8 L44,8 L44,12 L40,12 L40,4 L48,4"
stroke="{cor}" stroke-width="2" fill="none" stroke-linejoin="miter"/>
</svg>'''
    return svg_to_url(svg)


# Kanamari — ziguezague duplo vermelho/preto
def grafismo_kanamari_zig(cor1=PRIMARIA, cor2=VERDE_PRETO, altura=18):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 {altura}" preserveAspectRatio="none">
<polygon points="0,{altura} 10,2 20,{altura} 30,2 40,{altura}" fill="{cor1}"/>
<polygon points="0,2 10,{altura-2} 20,2 30,{altura-2} 40,2" fill="{cor2}" opacity="0.85"/>
</svg>'''
    return svg_to_url(svg)


# Kanamari crianças — fileira de pontos
def grafismo_kanamari_pontos(cor=PRIMARIA, altura=12):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 {altura}">
<circle cx="6" cy="{altura/2}" r="2.5" fill="{cor}"/>
<circle cx="18" cy="{altura/2}" r="2.5" fill="{cor}"/>
</svg>'''
    return svg_to_url(svg)


# Matis — losangos com eixo pontilhado
def grafismo_matis_losango(cor=PRIMARIA, opacity=0.08, tamanho=60):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tamanho} {tamanho}">
<polygon points="{tamanho/2},6 {tamanho-8},{tamanho/2} {tamanho/2},{tamanho-6} 8,{tamanho/2}" fill="{cor}" opacity="{opacity}"/>
<line x1="{tamanho/2}" y1="0" x2="{tamanho/2}" y2="{tamanho}" stroke="{cor}" stroke-width="1" stroke-dasharray="2,3" opacity="{opacity*2}"/>
</svg>'''
    return svg_to_url(svg)


# Kulina — chevrons / setas com pontos
def grafismo_kulina_chevron(cor=PRIMARIA, altura=18):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 {altura}">
<polygon points="0,2 12,{altura/2} 0,{altura-2} 4,{altura/2}" fill="{cor}"/>
<polygon points="15,2 27,{altura/2} 15,{altura-2} 19,{altura/2}" fill="{cor}"/>
<circle cx="8" cy="{altura/2}" r="1.2" fill="{VERDE_PRETO}"/>
<circle cx="23" cy="{altura/2}" r="1.2" fill="{VERDE_PRETO}"/>
</svg>'''
    return svg_to_url(svg)


# Mayuruna Bedibo — círculos
def grafismo_mayuruna_circulos(cor=PRIMARIA, altura=16):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 {altura}">
<circle cx="6" cy="{altura/2}" r="4" fill="{cor}"/>
<circle cx="20" cy="{altura/2}" r="4" fill="{cor}"/>
<circle cx="34" cy="{altura/2}" r="4" fill="{cor}"/>
</svg>'''
    return svg_to_url(svg)


# Marubo Boca — triângulos
def grafismo_marubo_triangulos(cor=PRIMARIA, altura=14):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 {altura}">
<polygon points="0,{altura} 7.5,2 15,{altura} 22.5,2 30,{altura}" fill="{cor}" opacity="0.6"/>
<polygon points="0,{altura} 7.5,2 15,{altura}" fill="none" stroke="{cor}" stroke-width="1"/>
</svg>'''
    return svg_to_url(svg)


# Mayuruna Chedebo — losangos com retângulos pretos dentro
def grafismo_mayuruna_chedebo(cor=PRIMARIA, altura=24):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 {altura}">
<polygon points="16,2 30,{altura/2} 16,{altura-2} 2,{altura/2}" fill="{cor}"/>
<rect x="12" y="{altura/2-2}" width="8" height="4" fill="{VERDE_PRETO}"/>
</svg>'''
    return svg_to_url(svg)


# ─── LOGO UNIVAJA — SELO OFICIAL ──────────────────────────────────────────────
def logo_univaja_selo(tamanho: int = 120, cor: str = None, miolo: str = None) -> str:
    """
    Emblema UNIVAJA — selo circular 100% gráfico (sem texto, para não vazar
    no sanitizador do Streamlit). O nome é renderizado como HTML ao lado.

    - Anéis externos + grafismos (Marubo, Kanamari, Matis)
    - Maloca triangular preenchida (cor primária)
    - Jacamim + palmeiras em negativo (cor do miolo)
    """
    c = cor or PRIMARIA
    m = miolo or "white"  # cor do fundo do miolo (negativo da maloca)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" style="height:{tamanho}px;width:{tamanho}px;flex-shrink:0;display:block">
  <circle cx="200" cy="200" r="195" fill="none" stroke="{c}" stroke-width="4"/>
  <circle cx="200" cy="200" r="158" fill="none" stroke="{c}" stroke-width="2"/>
  <circle cx="200" cy="200" r="152" fill="none" stroke="{c}" stroke-width="1"/>

  <g stroke="{c}" stroke-width="2.5" fill="none" stroke-linecap="square">
    <path d="M 110 366 L 110 357 L 124 357 L 124 370 L 138 370 L 138 357 L 152 357 L 152 366
             M 166 366 L 166 357 L 180 357 L 180 370 L 194 370 L 194 357 L 208 357 L 208 366
             M 222 366 L 222 357 L 236 357 L 236 370 L 250 370 L 250 357 L 264 357 L 264 366
             M 278 366 L 278 357 L 292 357 L 292 370 L 300 370"/>
  </g>
  <g stroke="{c}" stroke-width="2.5" fill="none">
    <path d="M 104 32 L 112 23 L 120 32 L 128 23 L 136 32 L 144 23 L 152 32 L 160 23 L 168 32
             L 176 23 L 184 32 L 192 23 L 200 32 L 208 23 L 216 32 L 224 23 L 232 32
             L 240 23 L 248 32 L 256 23 L 264 32 L 272 23 L 280 32 L 288 23 L 296 32"/>
  </g>
  <g stroke="{c}" stroke-width="2" fill="none">
    <path d="M 366 120 L 382 120 M 366 130 L 382 130 M 366 140 L 382 140
             M 366 150 L 382 150 M 366 160 L 382 160 M 366 170 L 382 170
             M 366 180 L 382 180 M 366 190 L 382 190 M 366 200 L 382 200
             M 366 210 L 382 210 M 366 220 L 382 220 M 366 230 L 382 230
             M 366 240 L 382 240 M 366 250 L 382 250 M 366 260 L 382 260
             M 366 270 L 382 270 M 366 280 L 382 280"/>
  </g>
  <g fill="{c}">
    <polygon points="18,120 30,132 18,144"/>
    <polygon points="18,154 30,166 18,178"/>
    <polygon points="18,188 30,200 18,212"/>
    <polygon points="18,222 30,234 18,246"/>
    <polygon points="18,256 30,268 18,280"/>
  </g>
  <circle cx="48" cy="200" r="4" fill="{c}"/>
  <circle cx="352" cy="200" r="4" fill="{c}"/>

  <!-- Maloca (triângulo + base semicircular) preenchida -->
  <path d="M 200 88 L 292 218 L 108 218 Z" fill="{c}"/>
  <path d="M 108 218 L 292 218 A 92 50 0 0 1 108 218 Z" fill="{c}"/>
  <ellipse cx="200" cy="218" rx="92" ry="50" fill="{c}"/>

  <!-- Palmeiras em negativo (miolo) -->
  <g fill="{m}" stroke="{m}" stroke-width="2">
    <line x1="150" y1="150" x2="150" y2="205"/>
    <path d="M 150 152 Q 132 142 122 146" fill="none"/>
    <path d="M 150 156 Q 130 154 120 160" fill="none"/>
    <path d="M 150 152 Q 168 142 178 146" fill="none"/>
    <path d="M 150 156 Q 170 154 180 160" fill="none"/>
    <line x1="250" y1="150" x2="250" y2="205"/>
    <path d="M 250 152 Q 268 142 278 146" fill="none"/>
    <path d="M 250 156 Q 270 154 280 160" fill="none"/>
    <path d="M 250 152 Q 232 142 222 146" fill="none"/>
    <path d="M 250 156 Q 230 154 220 160" fill="none"/>
  </g>

  <!-- Jacamim em negativo -->
  <g fill="{m}">
    <ellipse cx="205" cy="200" rx="26" ry="15"/>
    <path d="M 218 192 Q 224 168 230 160 L 236 162 Q 228 180 224 200 Z"/>
    <circle cx="234" cy="158" r="8"/>
    <polygon points="241,155 256,153 241,162"/>
    <rect x="194" y="212" width="2.5" height="14" rx="1"/>
    <rect x="210" y="212" width="2.5" height="14" rx="1"/>
    <path d="M 180 200 Q 168 194 160 198 Q 172 206 180 200 Z"/>
  </g>
</svg>"""


# ─── LOGO UNIVAJA ─────────────────────────────────────────────────────────────
def logo_svg(variante: str = "completa", cor_simbolo: str = None, cor_texto: str = None,
             altura: int = 60) -> str:
    """
    Logo UNIVAJA inspirada nos elementos do manual de marca:
    - Maloca (triângulo) — símbolo de união
    - Grafismo Marubo (greca) na base
    - Círculo/cabeça evocando o Jacamim (ave-símbolo)

    Variantes:
    - 'completa': símbolo + nome + tagline (horizontal)
    - 'simbolo': só o símbolo (quadrado)
    - 'compacta': símbolo + nome (sem tagline)
    """
    cs = cor_simbolo or PRIMARIA
    ct = cor_texto or PRIMARIA
    ct_sec = VERDE

    if variante == "simbolo":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" style="height:{altura}px;width:{altura}px">
            <circle cx="32" cy="32" r="30" fill="{cs}"/>
            <circle cx="32" cy="32" r="30" fill="none" stroke="{VERMELHO_ESC}" stroke-width="1.5"/>
            <path d="M32 12 L52 38 L12 38 Z" fill="white"/>
            <rect x="10" y="38" width="44" height="2.5" fill="{VERMELHO_ESC}"/>
            <rect x="10" y="40.5" width="44" height="13" fill="{VERDE_PRETO}"/>
            <path d="M14 50 L14 44 L18 44 L18 48 L22 48 L22 44 L26 44 L26 50
                     M30 50 L30 44 L34 44 L34 48 L38 48 L38 44 L42 44 L42 50
                     M46 50 L46 44 L50 44 L50 48"
                  stroke="white" stroke-width="1.3" fill="none" stroke-linecap="square"/>
            <circle cx="32" cy="22" r="2.2" fill="{cs}"/>
        </svg>"""
        return svg

    # Símbolo embutido + texto
    simbolo = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" style="height:{altura}px;width:{altura}px;flex-shrink:0">
        <circle cx="32" cy="32" r="30" fill="{cs}"/>
        <circle cx="32" cy="32" r="30" fill="none" stroke="{VERMELHO_ESC}" stroke-width="1.5"/>
        <path d="M32 12 L52 38 L12 38 Z" fill="white"/>
        <rect x="10" y="38" width="44" height="2.5" fill="{VERMELHO_ESC}"/>
        <rect x="10" y="40.5" width="44" height="13" fill="{VERDE_PRETO}"/>
        <path d="M14 50 L14 44 L18 44 L18 48 L22 48 L22 44 L26 44 L26 50
                 M30 50 L30 44 L34 44 L34 48 L38 48 L38 44 L42 44 L42 50
                 M46 50 L46 44 L50 44 L50 48"
              stroke="white" stroke-width="1.3" fill="none" stroke-linecap="square"/>
        <circle cx="32" cy="22" r="2.2" fill="{cs}"/>
    </svg>"""

    if variante == "compacta":
        return f"""<div class="logo-univaja">
            {simbolo}
            <div class="logo-textos">
                <div class="logo-nome" style="color:{ct}">UNIVAJA</div>
            </div>
        </div>"""

    # completa
    return f"""<div class="logo-univaja">
        {simbolo}
        <div class="logo-textos">
            <div class="logo-nome" style="color:{ct}">UNIVAJA</div>
            <div class="logo-tagline" style="color:{ct_sec}">União dos Povos do Vale do Javari</div>
        </div>
    </div>"""


# ─── CSS GLOBAL — usa os grafismos como elementos decorativos ────────────────
def css_global():
    """CSS completo com paleta e grafismos UNIVAJA aplicados."""

    # Pré-calcula URLs dos grafismos mais usados
    marubo_br        = grafismo_marubo(BRANCO, "transparent", 24)
    marubo_ver       = grafismo_marubo(PRIMARIA, "transparent", 24)
    marubo_verde     = grafismo_marubo(VERDE_CLARO, "transparent", 20)
    kanamari_zig     = grafismo_kanamari_zig(PRIMARIA, VERDE_PRETO, 14)
    kanamari_zig_br  = grafismo_kanamari_zig(BRANCO, VERDE_CLARO, 12)
    pontos_ver       = grafismo_kanamari_pontos(PRIMARIA, 12)
    pontos_br        = grafismo_kanamari_pontos(BRANCO, 10)
    losango_bg       = grafismo_matis_losango(VERDE, 0.05, 80)
    losango_bg_red   = grafismo_matis_losango(PRIMARIA, 0.04, 80)
    chevron_ver      = grafismo_kulina_chevron(PRIMARIA, 16)
    triangulos       = grafismo_marubo_triangulos(VERDE, 12)
    chedebo          = grafismo_mayuruna_chedebo(PRIMARIA, 20)

    return f"""
<style>
/* Fontes do Manual de Marca UNIVAJA:
   Principal: Croog Pro (proprietária — não disponível em web)
   Fallbacks oficiais do manual: Archivo + Battambang (Google Fonts) */
@import url('https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&family=Battambang:wght@400;700&display=swap');

/* ═══ Base ═════════════════════════════════════════════════════════════════ */
html, body, [class*="css"] {{
    font-family: 'Archivo', 'Segoe UI', Arial, sans-serif;
    color: {PRETO};
}}
#MainMenu, footer, header {{ visibility: hidden; }}

/* Fundo geral com losango Matis sutil */
.stApp {{
    background-color: {CREME};
    background-image: url("{losango_bg}");
    background-size: 160px 160px;
}}

/* Títulos com Battambang (fallback secundário do manual) */
h1, h2, h3 {{
    font-family: 'Battambang', 'Archivo', serif;
    color: {VERDE_PRETO};
    font-weight: 700;
    letter-spacing: -0.01em;
}}
h4, h5, h6 {{
    font-family: 'Archivo', sans-serif;
    color: {VERDE_PRETO};
    font-weight: 700;
}}

/* ═══ Logo UNIVAJA ═══════════════════════════════════════════════════════ */
.logo-univaja {{
    display: flex; align-items: center; gap: 14px;
}}
.logo-textos {{ display: flex; flex-direction: column; line-height: 1; }}
.logo-nome {{
    font-family: 'Battambang', 'Archivo', serif;
    font-weight: 700;
    font-size: 28px;
    letter-spacing: 3px;
    line-height: 1;
}}
.logo-tagline {{
    font-family: 'Archivo', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 4px;
    opacity: .9;
}}

/* ═══ Header UNIVAJA — com grafismos Marubo ═══════════════════════════════ */
.header-univaja {{
    background: linear-gradient(135deg, {PRIMARIA} 0%, {VERMELHO_ESC} 100%);
    color: white;
    padding: 24px 28px 18px;
    border-radius: 14px;
    margin-bottom: 22px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(120,11,11,.18);
}}
.header-univaja::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 24px;
    background-image: url("{marubo_br}");
    background-repeat: repeat-x;
    background-size: 48px 24px;
    opacity: 0.55;
}}
.header-univaja::after {{
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 12px;
    background-image: url("{pontos_br}");
    background-repeat: repeat-x;
    background-size: 24px 12px;
    opacity: 0.6;
}}
.header-univaja-conteudo {{ position: relative; z-index: 1; padding: 8px 0; }}
.header-univaja-titulo {{
    font-family: 'Battambang', 'Archivo', serif;
    font-size: 30px; font-weight: 700; letter-spacing: 3px;
    line-height: 1;
}}
.header-univaja-app {{
    font-size: 15px; font-weight: 700; margin-top: 10px;
    letter-spacing: 1px; text-transform: uppercase;
    background: rgba(255,255,255,.18); padding: 4px 12px;
    border-radius: 12px; display: inline-block;
}}
.header-univaja-sub {{
    font-size: 13px; opacity: .92; margin-top: 4px; font-weight: 500;
}}
.header-univaja-meta {{
    font-size: 11px; opacity: .85; text-align: right;
    position: relative; z-index: 1; padding: 8px 0;
    text-transform: uppercase; letter-spacing: 1px;
}}

/* ═══ Kanban de fluxos ═════════════════════════════════════════════════════ */
.flow-row {{
    display: flex; gap: 8px; flex-wrap: wrap;
    margin: 14px 0; align-items: stretch;
}}
.flow-step {{
    flex: 1; min-width: 150px;
    background: white;
    border: 1.5px solid var(--cor-etapa, {VERDE});
    border-radius: 12px;
    padding: 12px 14px 14px;
    position: relative;
    display: flex; flex-direction: column;
}}
.flow-step::before {{
    content: "";
    position: absolute; top: 0; left: 0; right: 0;
    height: 6px;
    background: var(--cor-etapa, {VERDE});
    border-radius: 12px 12px 0 0;
}}
.flow-step-num {{
    display: inline-flex; align-items: center; justify-content: center;
    width: 26px; height: 26px;
    background: var(--cor-etapa, {VERDE});
    color: white;
    border-radius: 50%;
    font-weight: 800; font-size: 13px;
    margin-bottom: 8px; margin-top: 4px;
}}
.flow-step-titulo {{
    font-size: 12px; font-weight: 700; color: {VERDE_PRETO};
    text-transform: uppercase; letter-spacing: 0.5px;
    margin-bottom: 6px; min-height: 28px;
}}
.flow-step-resp {{
    font-size: 11px; color: {CINZA}; line-height: 1.4;
    margin-bottom: 8px; flex: 1;
}}
.flow-step-entrega {{
    background: {CREME};
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 10px;
    color: {VERDE_PRETO};
    border-left: 3px solid var(--cor-etapa, {VERDE});
    line-height: 1.35;
}}
.flow-arrow {{
    display: flex; align-items: center; justify-content: center;
    color: var(--cor-etapa, {VERDE});
    font-size: 22px;
    font-weight: 700;
    margin: 0 -2px;
}}

/* ═══ Divisores com grafismo Marubo ═══════════════════════════════════════ */
.divisor-marubo {{
    height: 24px;
    background-image: url("{marubo_ver}");
    background-repeat: repeat-x;
    background-size: 48px 24px;
    margin: 22px 0;
    opacity: 0.85;
}}
.divisor-zig {{
    height: 14px;
    background-image: url("{kanamari_zig}");
    background-repeat: repeat-x;
    background-size: 40px 14px;
    margin: 18px 0;
}}
.divisor-pontos {{
    height: 12px;
    background-image: url("{pontos_ver}");
    background-repeat: repeat-x;
    background-size: 24px 12px;
    margin: 14px 0;
}}

/* ═══ Abas (Tabs) ═════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    border-bottom: none;
    padding-bottom: 14px;
    background-image: url("{kanamari_zig}");
    background-repeat: repeat-x;
    background-position: bottom left;
    background-size: 40px 8px;
}}
.stTabs [data-baseweb="tab"] {{
    background: {BRANCO};
    border-radius: 10px 10px 0 0;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 14px;
    color: {VERDE_PRETO};
    border: 2px solid {VERDE_CLARO};
    border-bottom: none;
}}
.stTabs [aria-selected="true"] {{
    background: {PRIMARIA} !important;
    color: white !important;
    border-color: {PRIMARIA} !important;
}}

/* ═══ Section title bars (grafismo Marubo na lateral) ═════════════════════ */
.section-title {{
    background: linear-gradient(90deg, {VERDE_PRETO} 0%, {VERDE_ESC} 100%);
    color: white;
    padding: 12px 20px 12px 60px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 15px;
    margin: 18px 0 14px;
    position: relative;
    overflow: hidden;
    letter-spacing: 0.5px;
}}
.section-title::before {{
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 48px;
    background-image: url("{marubo_br}");
    background-repeat: repeat-y;
    background-size: 24px 48px;
    opacity: 0.6;
}}
.section-title-vermelho {{
    background: linear-gradient(90deg, {VERMELHO_ESC} 0%, {PRIMARIA} 100%);
}}
.section-title-verde {{
    background: linear-gradient(90deg, {VERDE_ESC} 0%, {VERDE} 100%);
}}

/* ═══ Cards genéricos ═════════════════════════════════════════════════════ */
.card {{
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    position: relative;
    transition: transform .1s, box-shadow .15s;
}}
.card:hover {{ box-shadow: 0 6px 20px rgba(31,42,33,.08); }}
.card-vermelho {{ border-left: 5px solid {PRIMARIA}; }}
.card-verde    {{ border-left: 5px solid {VERDE}; }}
.card-roxo     {{ border-left: 5px solid {VERDE_ESC}; }}
.card-teal     {{ border-left: 5px solid {VERDE}; }}
.card-laranja  {{ border-left: 5px solid {VERMELHO_MED}; }}
.card-cinza    {{ border-left: 5px solid {CINZA}; }}
.card-coral    {{ border-left: 5px solid {VERMELHO_ESC}; }}
.card-azul     {{ border-left: 5px solid {VERDE_PRETO}; }}

/* Card com grafismo de borda (Marubo) */
.card-grafismo {{
    background: white;
    border: 1px solid {VERDE_CLARO};
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
}}
.card-grafismo::before {{
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 12px;
    background-image: url("{kanamari_zig}");
    background-repeat: repeat-y;
    background-size: 12px 40px;
}}
.card-grafismo-conteudo {{ padding-left: 12px; }}

/* ═══ Badges ══════════════════════════════════════════════════════════════ */
.badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
.badge-seg    {{ background: {VERDE_FUNDO}; color: {VERDE_PRETO}; border: 1px solid {VERDE_CLARO}; }}
.badge-prod   {{ background: {VERDE_FUNDO}; color: {VERDE_ESC};  border: 1px solid {VERDE}; }}
.badge-pol    {{ background: {VERMELHO_FUNDO}; color: {VERMELHO_ESC}; border: 1px solid {VERMELHO_CLARO}; }}
.badge-perm   {{ background: {VERDE_FUNDO}; color: {VERDE_ESC};  border: 1px solid {VERDE_CLARO}; }}
.badge-local  {{ background: {VERMELHO_FUNDO}; color: {VERMELHO_ESC}; border: 1px solid {VERMELHO_CLARO}; }}
.badge-int    {{ background: {VERDE_FUNDO}; color: {VERDE_PRETO}; border: 1px solid {VERDE}; }}
.badge-den    {{ background: {VERMELHO_FUNDO}; color: {VERMELHO_ESC}; border: 1px solid {PRIMARIA}; }}
.badge-pos    {{ background: {VERDE_FUNDO}; color: {VERDE}; border: 1px solid {VERDE_CLARO}; }}

/* ═══ Tabelas de fluxo ════════════════════════════════════════════════════ */
.tabela-fluxo {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 13px;
    margin-bottom: 16px;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {VERDE_CLARO};
}}
.tabela-fluxo th {{
    padding: 12px 14px;
    text-align: left;
    color: white;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: {VERDE_PRETO};
}}
.tabela-fluxo td {{
    padding: 12px 14px;
    border-bottom: 1px solid #e5e7eb;
    vertical-align: top;
    font-size: 13px;
    line-height: 1.5;
}}
.tabela-fluxo tr:last-child td {{ border-bottom: none; }}
.tabela-fluxo tr:nth-child(even) td {{ background: {CREME}; }}

.etapa {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px; height: 32px;
    border-radius: 50%;
    font-weight: 800;
    font-size: 14px;
    color: white;
    border: 2px solid white;
    box-shadow: 0 2px 6px rgba(0,0,0,.15);
}}

/* ═══ Alertas ═════════════════════════════════════════════════════════════ */
.alerta {{
    background: {CREME};
    border: 1px solid {VERMELHO_MED};
    border-left: 5px solid {VERMELHO_MED};
    border-radius: 8px;
    padding: 14px 16px 14px 20px;
    font-size: 13px;
    color: {VERMELHO_ESC};
    margin: 14px 0;
    position: relative;
    overflow: hidden;
}}
.alerta::before {{
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 5px;
    background-image: url("{pontos_ver}");
    background-repeat: repeat-y;
    background-size: 5px 12px;
}}
.alerta-vermelho {{
    background: {VERMELHO_FUNDO};
    border-color: {PRIMARIA};
    border-left-color: {VERMELHO_ESC};
    color: {VERMELHO_ESC};
}}
.alerta-verde {{
    background: {VERDE_FUNDO};
    border-color: {VERDE};
    border-left-color: {VERDE};
    color: {VERDE_PRETO};
}}
.alerta-azul {{
    background: {VERDE_FUNDO};
    border-color: {VERDE_ESC};
    border-left-color: {VERDE_ESC};
    color: {VERDE_PRETO};
}}

/* ═══ Termo pill ══════════════════════════════════════════════════════════ */
.termo-pill {{
    display: inline-block;
    background: white;
    border: 1px solid {VERDE_CLARO};
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    margin: 3px;
    color: {VERDE_PRETO};
    font-weight: 500;
}}

/* ═══ Glossário ═══════════════════════════════════════════════════════════ */
.gloss-card {{
    background: white;
    border: 1px solid #e0e0e0;
    border-left: 4px solid {PRIMARIA};
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 10px;
}}
.gloss-titulo {{
    font-weight: 700; color: {PRIMARIA};
    font-size: 14px; margin-bottom: 4px;
    text-transform: uppercase; letter-spacing: 0.5px;
}}
.gloss-desc {{ font-size: 13px; color: {CINZA}; line-height: 1.55; }}
.gloss-canal {{
    margin-top: 8px; font-size: 11px;
    color: white; background: {VERDE_PRETO};
    padding: 3px 10px; border-radius: 12px;
    display: inline-block; font-weight: 600;
    letter-spacing: 0.3px;
}}

/* ═══ Pessoa card ═════════════════════════════════════════════════════════ */
.pessoa-card {{
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 8px;
    position: relative;
    overflow: hidden;
}}
.pessoa-card::before {{
    content: "";
    position: absolute;
    top: 0; right: 0;
    width: 50px; height: 50px;
    background-image: url("{losango_bg_red}");
    background-size: 80px 80px;
    opacity: 0.6;
}}
.pessoa-nome  {{ font-weight: 700; font-size: 14px; color: {VERDE_PRETO}; margin-bottom: 6px; }}
.pessoa-faz   {{ font-size: 13px; color: {CINZA}; line-height: 1.55; }}
.pessoa-nao   {{ font-size: 12px; color: {VERMELHO_ESC}; margin-top: 6px; line-height: 1.45; }}

/* ═══ Links busca ═════════════════════════════════════════════════════════ */
.link-busca {{
    display: block;
    background: white;
    border: 1px solid {VERDE_CLARO};
    border-radius: 10px;
    padding: 14px 16px 14px 20px;
    text-decoration: none;
    color: {VERDE_PRETO};
    margin-bottom: 10px;
    transition: all .15s;
    position: relative;
    overflow: hidden;
}}
.link-busca::before {{
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 6px;
    background: {PRIMARIA};
    transition: width .15s;
}}
.link-busca:hover {{
    border-color: {PRIMARIA};
    transform: translateX(2px);
    box-shadow: 0 4px 14px rgba(220,54,55,.12);
}}
.link-busca:hover::before {{ width: 10px; }}
.link-busca-titulo {{ font-weight: 700; font-size: 14px; color: {PRIMARIA}; }}
.link-busca-desc {{ font-size: 12px; color: {CINZA}; margin-top: 4px; }}

/* ═══ Decisão política ═══════════════════════════════════════════════════ */
.decisao-col {{
    border-radius: 10px;
    padding: 16px 18px;
    font-size: 13px;
    line-height: 1.55;
    position: relative;
    overflow: hidden;
}}
.decisao-pub    {{ background: {VERDE_FUNDO}; border: 1.5px solid {VERDE}; color: {VERDE_PRETO}; }}
.decisao-wait   {{ background: {CREME}; border: 1.5px solid {VERMELHO_MED}; color: {VERMELHO_ESC}; }}
.decisao-silent {{ background: {VERMELHO_FUNDO}; border: 1.5px solid {PRIMARIA}; color: {VERMELHO_ESC}; }}

/* ═══ Calendário ══════════════════════════════════════════════════════════ */
.cal-dia {{
    background: white;
    border: 1px solid #e0e0e0;
    border-left: 4px solid {PRIMARIA};
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 8px;
}}
.cal-data  {{ font-weight: 700; font-size: 13px; color: {PRIMARIA}; text-transform: uppercase; letter-spacing: 0.5px; }}
.cal-pauta {{ font-size: 13px; color: {CINZA}; line-height: 1.5; margin-top: 4px; }}
.cal-resp  {{ font-size: 11px; color: #6b7280; margin-top: 4px; }}

/* ═══ Pautas sensíveis ════════════════════════════════════════════════════ */
.pauta-sensivel {{
    background: linear-gradient(90deg, {VERMELHO_FUNDO} 0%, white 35%);
    border: 2px solid {PRIMARIA};
    border-left: 8px solid {VERMELHO_ESC};
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 14px rgba(220,54,55,.15);
}}
.pauta-sensivel::before {{
    content: "";
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    background: radial-gradient(circle at top right, {PRIMARIA}22 0%, transparent 70%);
    pointer-events: none;
}}
.alerta-sensivel-tag {{
    display: inline-flex; align-items: center; gap: 6px;
    background: {PRIMARIA};
    color: white;
    padding: 5px 12px;
    border-radius: 14px;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    box-shadow: 0 2px 6px rgba(120,11,11,.3);
}}
.alerta-sensivel-tag::before {{
    content: "⚠️";
    font-size: 14px;
}}
.alerta-sensivel-msg {{
    background: white;
    border-left: 4px solid {PRIMARIA};
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 11px;
    color: {VERMELHO_ESC};
    margin-top: 8px;
    line-height: 1.4;
    font-weight: 500;
}}

/* Link Google estilizado */
.link-google {{
    display: flex; align-items: center; gap: 14px;
    background: white;
    border: 1px solid #dadce0;
    border-radius: 24px;
    padding: 14px 20px;
    text-decoration: none;
    color: #202124;
    margin-bottom: 10px;
    transition: all .15s;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
}}
.link-google:hover {{
    box-shadow: 0 4px 14px rgba(0,0,0,.10);
    border-color: #4285F4;
    transform: translateY(-1px);
}}
.link-google-conteudo {{ flex: 1; }}
.link-google-titulo {{
    font-family: 'Archivo', sans-serif;
    font-weight: 600; font-size: 15px;
    color: #202124;
    margin-bottom: 2px;
    display: flex; align-items: center; gap: 8px;
}}
.link-google-desc {{
    font-size: 12px; color: #5f6368;
    line-height: 1.4;
}}
.link-google-seta {{
    color: #4285F4;
    font-size: 18px;
    font-weight: 700;
}}

/* ═══ News card (Monitor) ════════════════════════════════════════════════ */
.news-card {{
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 14px 18px 14px 24px;
    margin-bottom: 12px;
    transition: box-shadow .15s, transform .1s;
    position: relative;
    overflow: hidden;
}}
.news-card::before {{
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 8px;
    background-image: url("{kanamari_zig}");
    background-repeat: repeat-y;
    background-size: 8px 28px;
}}
.news-card:hover {{
    box-shadow: 0 6px 20px rgba(220,54,55,.10);
    transform: translateY(-1px);
}}
.news-titulo {{
    font-size: 15px; font-weight: 700; color: {VERDE_PRETO}; line-height: 1.4;
    text-decoration: none; display: block; margin-bottom: 6px;
}}
.news-titulo:hover {{ color: {PRIMARIA}; }}
.news-resumo {{ font-size: 13px; color: {CINZA}; line-height: 1.55; margin-bottom: 10px; }}
.news-meta {{
    display: flex; gap: 10px; flex-wrap: wrap;
    font-size: 11px; color: #6b7280; align-items: center;
}}
.news-fonte {{
    background: {PRIMARIA}; color: white;
    padding: 3px 10px; border-radius: 12px;
    font-weight: 700; font-size: 11px;
    text-transform: uppercase; letter-spacing: 0.5px;
}}
.news-tag {{
    background: {VERDE_FUNDO}; color: {VERDE_PRETO};
    padding: 3px 10px; border-radius: 12px;
    font-size: 11px; font-weight: 600;
    border: 1px solid {VERDE_CLARO};
}}
.news-tag-prio {{
    background: {VERMELHO_FUNDO}; color: {VERMELHO_ESC};
    border-color: {VERMELHO_CLARO};
}}

/* ═══ Stat cards ══════════════════════════════════════════════════════════ */
.stat-card {{
    background: white;
    border: 1px solid {VERDE_CLARO};
    border-radius: 12px;
    padding: 16px 18px 14px;
    text-align: center;
    position: relative;
    overflow: hidden;
}}
.stat-card::after {{
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 8px;
    background-image: url("{kanamari_zig}");
    background-repeat: repeat-x;
    background-size: 24px 8px;
}}
.stat-num {{ font-size: 32px; font-weight: 800; color: {PRIMARIA}; line-height: 1; }}
.stat-label {{
    font-size: 11px; color: {VERDE_PRETO}; margin-top: 8px;
    text-transform: uppercase; letter-spacing: 1px; font-weight: 600;
}}

/* ═══ Salvas ══════════════════════════════════════════════════════════════ */
.salva-card {{
    background: {VERMELHO_FUNDO};
    border: 1px solid {VERMELHO_CLARO};
    border-radius: 12px;
    padding: 12px 16px 12px 22px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}}
.salva-card::before {{
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: 0;
    width: 6px;
    background-image: url("{chevron_ver}");
    background-repeat: repeat-y;
    background-size: 6px 24px;
    opacity: 0.85;
}}

/* ═══ Botões Streamlit ════════════════════════════════════════════════════ */
.stButton > button {{
    background: {PRIMARIA};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    transition: all .15s;
}}
.stButton > button:hover {{
    background: {VERMELHO_ESC};
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(120,11,11,.25);
}}

/* ═══ Sidebar ═════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background: {VERDE_PRETO};
    background-image: url("{losango_bg}");
    background-size: 200px 200px;
}}
[data-testid="stSidebar"] * {{ color: {CREME}; }}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{ color: white; }}
[data-testid="stSidebar"] .stCheckbox label {{ color: {CREME} !important; font-size: 13px; }}
[data-testid="stSidebar"] hr {{ border-color: {VERDE_ESC}; }}

/* Logo na sidebar — selo UNIVAJA oficial */
.sidebar-logo {{
    display: flex; flex-direction: column; align-items: center;
    padding: 12px 8px;
    border-radius: 14px;
    background: white;
    margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,.15);
}}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
    border-color: {VERDE_CLARO} !important;
    border-radius: 8px !important;
}}

/* ═══ Caption ═════════════════════════════════════════════════════════════ */
.stCaption, [data-testid="stCaptionContainer"] {{
    color: {CINZA} !important;
    font-style: italic;
}}
</style>
"""


def header(titulo: str, sub: str = "", meta: str = "Uso interno · 2026") -> str:
    """Header: emblema em cor primária sobre disco branco + wordmark em HTML."""
    # Emblema na COR PRIMÁRIA, sobre um disco branco para contraste no header vermelho
    selo = logo_univaja_selo(tamanho=92, cor=PRIMARIA, miolo='white')

    return f"""
<div class="header-univaja">
    <div class="header-univaja-conteudo" style="display:flex;align-items:center;gap:20px">
        <div style="background:white;border-radius:50%;padding:10px;flex-shrink:0;
                    box-shadow:0 4px 14px rgba(0,0,0,.18);line-height:0">{selo}</div>
        <div>
            <div style="font-family:'Battambang','Archivo',serif;font-weight:700;font-size:30px;
                        letter-spacing:3px;line-height:1;color:white">UNIVAJA</div>
            <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;font-weight:600;
                        opacity:.9;margin-top:5px;color:white">União dos Povos Indígenas · Vale do Javari</div>
            <div class="header-univaja-app" style="margin-top:10px">{titulo}</div>
            <div class="header-univaja-sub">{sub}</div>
        </div>
    </div>
    <div class="header-univaja-meta">{meta}</div>
</div>
"""


def divisor(tipo: str = "marubo") -> str:
    """Insere um divisor com grafismo: 'marubo', 'zig' ou 'pontos'."""
    return f'<div class="divisor-{tipo}"></div>'


def section_title(texto: str, variante: str = "padrao") -> str:
    """Barra de seção com Marubo lateral. Variantes: padrao, vermelho, verde."""
    cls = "section-title"
    if variante == "vermelho":
        cls += " section-title-vermelho"
    elif variante == "verde":
        cls += " section-title-verde"
    return f'<div class="{cls}">◆ {texto}</div>'


# ─── LOGOS GOOGLE (para links de busca) ───────────────────────────────────────
def logo_google(tamanho: int = 22) -> str:
    """G colorido oficial do Google."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" style="height:{tamanho}px;width:{tamanho}px;display:inline-block;vertical-align:middle;flex-shrink:0">
<path fill="#4285F4" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z"/>
<path fill="#34A853" d="M24 46c5.94 0 10.92-1.97 14.56-5.33l-7.11-5.52c-1.97 1.32-4.49 2.1-7.45 2.1-5.73 0-10.58-3.87-12.31-9.07H4.34v5.7C7.96 41.07 15.4 46 24 46z"/>
<path fill="#FBBC05" d="M11.69 28.18C11.25 26.86 11 25.45 11 24s.25-2.86.69-4.18v-5.7H4.34C2.85 17.09 2 20.45 2 24c0 3.55.85 6.91 2.34 9.88l7.35-5.7z"/>
<path fill="#EA4335" d="M24 10.75c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 4.18 29.93 2 24 2 15.4 2 7.96 6.93 4.34 14.12l7.35 5.7c1.73-5.2 6.58-9.07 12.31-9.07z"/>
</svg>"""


def logo_google_noticias(tamanho: int = 22) -> str:
    """G colorido + ícone de jornal pequeno."""
    g = logo_google(tamanho)
    return f'<span style="display:inline-flex;align-items:center;gap:6px;vertical-align:middle">{g}<span style="font-family:Archivo,sans-serif;font-size:14px;font-weight:500;color:#5f6368">Notícias</span></span>'


def logo_google_trends(tamanho: int = 22) -> str:
    """G colorido + ícone de tendência ascendente."""
    g = logo_google(tamanho)
    return f'<span style="display:inline-flex;align-items:center;gap:6px;vertical-align:middle">{g}<span style="font-family:Archivo,sans-serif;font-size:14px;font-weight:500;color:#5f6368">Trends</span></span>'


def logo_google_search(tamanho: int = 22) -> str:
    g = logo_google(tamanho)
    return f'<span style="display:inline-flex;align-items:center;gap:6px;vertical-align:middle">{g}<span style="font-family:Archivo,sans-serif;font-size:14px;font-weight:500;color:#5f6368">Search</span></span>'


# ─── DETECÇÃO DE PAUTAS SENSÍVEIS ─────────────────────────────────────────────
PALAVRAS_SENSIVEIS = [
    "denúncia", "denuncia", "denunciar",
    "violência", "violencia", "violento",
    "assassinato", "assassinar", "morte", "morto",
    "garimpo", "garimpeiro",
    "invasão", "invasao", "invasor", "invadir",
    "ameaça", "ameaca", "ameaçar",
    "perseguição", "perseguicao",
    "ataque", "atacar",
    "racismo", "racista",
    "marco temporal",
    "crise", "polêmica", "polemica",
    "bruno pereira", "dom phillips", "bruno e dom",
    "stf", "supremo",
    "pec ", "projeto de lei",
    "madeireira", "madeireiro",
    "narcotráfico", "narcotrafico", "tráfico",
    "conflito",
]

def eh_pauta_sensivel(*textos) -> bool:
    """Detecta se uma pauta toca tema sensível pela presença de palavras-chave."""
    txt = " ".join([str(t) for t in textos if t]).lower()
    if "🔴" in txt or "urgente" in txt:
        return True
    return any(p in txt for p in PALAVRAS_SENSIVEIS)


def sidebar_logo() -> str:
    """Emblema UNIVAJA (cor primária) + wordmark em HTML na sidebar."""
    return f"""<div class="sidebar-logo">
        {logo_univaja_selo(tamanho=120, cor=PRIMARIA, miolo='white')}
        <div style="text-align:center;margin-top:10px">
            <div style="font-family:'Battambang','Archivo',serif;font-weight:700;font-size:22px;
                        color:{PRIMARIA};letter-spacing:4px;line-height:1">UNIVAJA</div>
            <div style="font-family:'Archivo',sans-serif;font-size:8.5px;letter-spacing:1.2px;
                        text-transform:uppercase;color:{VERDE_ESC};margin-top:5px;line-height:1.4">
                União dos Povos Indígenas<br>Vale do Javari
            </div>
        </div>
    </div>"""


def flow_kanban(etapas: list) -> str:
    """Renderiza um kanban horizontal de fluxo.

    Cada item de `etapas` é um dict com:
    - num: número/identificador da etapa (str)
    - titulo: nome da etapa
    - responsavel: quem faz
    - entrega: o que entrega
    - cor: cor da coluna (hex)
    """
    blocos = []
    for i, e in enumerate(etapas):
        cor = e.get("cor", VERDE)
        blocos.append(f"""
        <div class="flow-step" style="--cor-etapa:{cor}">
            <div class="flow-step-num" style="background:{cor}">{e.get('num','')}</div>
            <div class="flow-step-titulo">{e.get('titulo','')}</div>
            <div class="flow-step-resp">👤 {e.get('responsavel','')}</div>
            <div class="flow-step-entrega">📦 {e.get('entrega','')}</div>
        </div>
        """)
        if i < len(etapas) - 1:
            cor_next = etapas[i+1].get("cor", VERDE)
            blocos.append(f'<div class="flow-arrow" style="--cor-etapa:{cor_next}">▶</div>')
    return f'<div class="flow-row">{"".join(blocos)}</div>'
