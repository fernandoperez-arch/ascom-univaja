"""
ASCOM UNIVAJA — Plataforma de fluxos integrados de comunicação
Identidade visual: Manual de Marca UNIVAJA (cores + grafismos dos povos do Vale do Javari).
"""

import streamlit as st
from univaja_brand import (
    css_global, header, divisor, section_title,
    PRIMARIA, VERMELHO_ESC, VERMELHO_MED, VERDE, VERDE_ESC, VERDE_PRETO, CINZA,
)

# ─── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ASCOM UNIVAJA",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(css_global(), unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    header(
        "UNIVAJA",
        "Assessoria de Comunicação — ASCOM",
        "Uso interno · 2026",
    ),
    unsafe_allow_html=True,
)

# ─── Abas ─────────────────────────────────────────────────────────────────────
aba5, aba1, aba2, aba3, aba4 = st.tabs([
    "ℹ️ Como usar",
    "📋 Fluxos integrados",
    "📖 Glossário & referência",
    "📅 Agenda semanal",
    "🔍 Monitor de pautas",
])


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 1 — FLUXOS INTEGRADOS
# ══════════════════════════════════════════════════════════════════════════════
with aba1:

    st.markdown(section_title("Fluxos integrados de comunicação", "padrao"), unsafe_allow_html=True)
    st.caption("Todos os fluxos da ASCOM em um só lugar. Use antes da reunião de segunda e durante a produção.")

    # ── Fluxo 1: Ciclo semanal ──────────────────────────────────────────────
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown(section_title("Fluxo 1 — Ciclo semanal de trabalho", "padrao"), unsafe_allow_html=True)

    st.markdown(f"""
    <table class="tabela-fluxo">
        <thead>
            <tr>
                <th style="width:60px">Etapa</th>
                <th style="width:140px">Quando</th>
                <th>O que acontece</th>
                <th style="width:220px">Quem participa</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="etapa" style="background:{VERDE_PRETO}">1</span></td>
                <td><strong>Segunda-feira</strong></td>
                <td>Reunião ASCOM: seleção de pautas da semana e divisão de tarefas por tipo de material (card, vídeo, boletim). Cada comunicador sai com uma responsabilidade clara.</td>
                <td>14 comunicadores + pontos focais</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE_PRETO}">2</span></td>
                <td><strong>Terça – Quarta</strong></td>
                <td>Produção do material: roteiros, cards, textos e vídeos conforme a divisão da reunião. Designer cria os cards seguindo o manual de marca.</td>
                <td>Comunicadores designados + designer</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE_PRETO}">3</span></td>
                <td><strong>Quinta – Sexta</strong></td>
                <td>Envio ao grupo ASCOM para aprovação. Após aval da coordenação, TUMI ou DÉBORA publicam nas redes sociais.</td>
                <td>Ponto focal + coordenação + TUMI/DÉBORA</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{CINZA}">↺</span></td>
                <td><strong>Segunda seguinte</strong></td>
                <td>Nova semana começa. O ciclo se reinicia com nova reunião de pauta.</td>
                <td>Toda a equipe ASCOM</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # ── Fluxo 2A: Card ──────────────────────────────────────────────────────
    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown(section_title("Fluxo 2A — Publicação: Card / Imagem", "verde"), unsafe_allow_html=True)

    st.markdown(f"""
    <table class="tabela-fluxo">
        <thead>
            <tr>
                <th style="width:60px">Etapa</th>
                <th style="width:200px">Responsável</th>
                <th>Ação</th>
                <th style="width:170px">Entrega</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="etapa" style="background:{VERDE}">1</span></td>
                <td><strong>Comunicador designado</strong></td>
                <td>Propõe o tema na reunião de segunda. Explica o que o card deve comunicar, qual o objetivo e para qual público.</td>
                <td>Proposta oral ou escrita no grupo</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE}">2</span></td>
                <td><strong>Comunicador → Designer</strong></td>
                <td>Envia briefing escrito ao designer com: tema, texto principal, informações de destaque e referências visuais (se houver). O briefing deve ser claro o suficiente para o designer trabalhar sem precisar perguntar.</td>
                <td>Briefing no grupo ASCOM</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE}">3</span></td>
                <td><strong>Designer</strong></td>
                <td>Cria o card seguindo o manual de marca: cores, fontes, logos, grafismos e proporções corretas. Não inventa elementos novos sem consultar o comunicador responsável.</td>
                <td>Card finalizado (.PNG ou .JPG)</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE}">4</span></td>
                <td><strong>Comunicador responsável</strong></td>
                <td>Redige a legenda do post: chamada de abertura + informação principal + hashtags obrigatórios (#UNIVAJA #ValeDoJavari #PovosIndígenas).</td>
                <td>Legenda redigida</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERMELHO_MED}">5</span></td>
                <td><strong>Ponto focal</strong></td>
                <td>Envia card + legenda no grupo ASCOM para aprovação. Material fica em espera — não publica antes do aval.</td>
                <td>Material no grupo ASCOM</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERMELHO_MED}">6</span></td>
                <td><strong>Coordenação ASCOM</strong></td>
                <td>
                    ✅ <strong>Aprovado</strong> → segue para etapa 7<br>
                    🔁 <strong>Ajuste necessário</strong> → retorna às etapas 3 ou 4 com orientação clara do que mudar
                </td>
                <td>Aprovação registrada no grupo</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{PRIMARIA}">7</span></td>
                <td><strong>TUMI ou DÉBORA</strong></td>
                <td>Publicam o card nas redes: Instagram, LinkedIn e WhatsApp conforme a orientação da pauta. Únicas com acesso ao perfil do Instagram.</td>
                <td>✅ Post publicado</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alerta">
        ⚠️ <strong>Regra inegociável:</strong> nenhum material pode ser publicado sem aprovação registrada no grupo ASCOM.
        Em caso de dúvida, aguardar. Melhor atrasar um dia do que publicar algo errado.
    </div>
    """, unsafe_allow_html=True)

    # ── Fluxo 2B: Vídeo ─────────────────────────────────────────────────────
    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown(section_title("Fluxo 2B — Publicação: Vídeo / Reels", "verde"), unsafe_allow_html=True)

    st.markdown(f"""
    <table class="tabela-fluxo">
        <thead>
            <tr>
                <th style="width:60px">Etapa</th>
                <th style="width:230px">Responsável</th>
                <th>Ação</th>
                <th style="width:170px">Entrega</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="etapa" style="background:{VERDE_ESC}">1</span></td>
                <td><strong>Comunicador designado</strong></td>
                <td>Propõe o tema na reunião de segunda. Define o formato: depoimento de liderança, cobertura de evento ou boletim informativo.</td>
                <td>Proposta no grupo ASCOM</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE_ESC}">2</span></td>
                <td><strong>Responsável pelo roteiro</strong></td>
                <td>Escreve o roteiro completo com: contexto, falas ou narração, ordem das cenas, duração estimada. <strong>Máximo 90 segundos para Reels do Instagram.</strong> Roteiro deve ser aprovado antes de gravar.</td>
                <td>Roteiro no grupo ASCOM</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE_ESC}">3</span></td>
                <td><strong>Responsável pela gravação/edição</strong></td>
                <td>Grava conforme o roteiro aprovado. Edita o vídeo incluindo: cortes, legendas em português (acessibilidade), trilha sonora e logo da UNIVAJA.</td>
                <td>Vídeo finalizado (.MP4)</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE_ESC}">4</span></td>
                <td><strong>Comunicador responsável</strong></td>
                <td>Redige a legenda: chamada de abertura + resumo do conteúdo + hashtags (#UNIVAJA #ValeDoJavari #PovosIndígenas #ComunicaçãoIndígena).</td>
                <td>Legenda redigida</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERMELHO_MED}">5</span></td>
                <td><strong>Ponto focal</strong></td>
                <td>Envia vídeo + legenda no grupo ASCOM. Material aguarda aprovação. Não publica antes do aval.</td>
                <td>Material no grupo ASCOM</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERMELHO_MED}">6</span></td>
                <td><strong>Coordenação ASCOM</strong></td>
                <td>
                    ✅ <strong>Aprovado</strong> → segue para etapa 7<br>
                    🔁 <strong>Ajuste necessário</strong> → retorna às etapas 3 ou 4 com orientação do que mudar
                </td>
                <td>Aprovação registrada</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{PRIMARIA}">7</span></td>
                <td><strong>TUMI ou DÉBORA</strong></td>
                <td>Publicam o vídeo nas redes: Instagram Reels, WhatsApp e LinkedIn. Adaptam a legenda para cada rede se necessário (LinkedIn mais formal, sem excesso de hashtags).</td>
                <td>✅ Vídeo publicado</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # ── Fluxo 3: Político ───────────────────────────────────────────────────
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown(section_title("Fluxo 3 — Aprovação política (temas sensíveis)", "vermelho"), unsafe_allow_html=True)

    st.markdown("""
    <div class="alerta alerta-vermelho">
        🔴 <strong>Use este fluxo sempre que o material envolver:</strong> posicionamento político, denúncia,
        crise institucional, questão jurídica, imagem do Presidente ou qualquer assunto que possa
        afetar parceiros e patrocinadores.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <table class="tabela-fluxo">
        <thead>
            <tr>
                <th style="width:60px">Etapa</th>
                <th style="width:220px">Responsável</th>
                <th>Ação</th>
                <th style="width:170px">Resultado</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="etapa" style="background:{VERMELHO_ESC}">1</span></td>
                <td><strong>Qualquer comunicador</strong></td>
                <td>Identifica que o material envolve tema sensível (político, denúncia, jurídico ou crise). <strong>NÃO produz nada ainda.</strong> Aciona o grupo ASCOM imediatamente.</td>
                <td>Alerta no grupo ASCOM</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERMELHO_ESC}">2</span></td>
                <td><strong>Comunicador → Ponto Focal Indígena</strong></td>
                <td>Aciona diretamente o ponto focal indígena da ASCOM. Descreve o tema, o fato ocorrido e o que precisaria ser comunicado. Aguarda orientação antes de qualquer ação.</td>
                <td>Consulta registrada</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{CINZA}">3a</span></td>
                <td><strong>Procuradoria Jurídica</strong></td>
                <td>Avalia as implicações legais do material. Orienta sobre o que pode ou não ser publicado. Verifica se há risco jurídico para a UNIVAJA ou para os comunicadores.</td>
                <td>Parecer jurídico</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{CINZA}">3b</span></td>
                <td><strong>Coordenação Geral UNIVAJA</strong></td>
                <td>Valida o posicionamento político. Define qual é a mensagem institucional da organização. Decide se a UNIVAJA vai se pronunciar ou manter silêncio estratégico.</td>
                <td>Orientação política</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERMELHO_MED}">4</span></td>
                <td><strong>Coordenação + Procuradoria (juntos)</strong></td>
                <td>Decisão conjunta entre as três opções abaixo. A decisão é comunicada à equipe ASCOM com clareza.</td>
                <td>Decisão registrada</td>
            </tr>
            <tr>
                <td><span class="etapa" style="background:{VERDE}">5</span></td>
                <td><strong>Ponto focal + equipe ASCOM</strong></td>
                <td>Executa a decisão: publica conforme fluxo normal (2A ou 2B), aguarda em silêncio, ou foca em conteúdo institucional positivo para proteger a imagem da UNIVAJA.</td>
                <td>Ação comunicada à equipe</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Três saídas
    col_pub, col_wait, col_sil = st.columns(3)
    with col_pub:
        st.markdown("""
        <div class="decisao-col decisao-pub">
            <strong>✅ Publicar</strong><br>
            Material foi aprovado pela coordenação e procuradoria. Segue normalmente pelo fluxo 2A (card) ou 2B (vídeo).
        </div>
        """, unsafe_allow_html=True)
    with col_wait:
        st.markdown("""
        <div class="decisao-col decisao-wait">
            <strong>⏳ Aguardar</strong><br>
            Situação ainda em avaliação. Equipe não publica nada sobre o tema até nova orientação. Mantém produção de outros conteúdos normalmente.
        </div>
        """, unsafe_allow_html=True)
    with col_sil:
        st.markdown("""
        <div class="decisao-col decisao-silent">
            <strong>🔇 Silêncio estratégico</strong><br>
            Não publicar sobre o assunto. Foco em conteúdo institucional positivo (eventos, associações, cultura) para proteger a imagem da UNIVAJA junto a parceiros.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alerta alerta-vermelho" style="margin-top:14px">
        🔴 <strong>Regra de ouro:</strong> Em caso de dúvida, NÃO PUBLIQUE. Acione o ponto focal e aguarde orientação.
        O silêncio temporário é sempre melhor do que uma publicação precipitada que coloque a UNIVAJA em risco.
    </div>
    """, unsafe_allow_html=True)

    # ── Fluxo Quinzenal ─────────────────────────────────────────────────────
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown(section_title("Fluxo 4 — Ciclo quinzenal com a coordenação", "padrao"), unsafe_allow_html=True)

    st.markdown("""
    <table class="tabela-fluxo">
        <thead>
            <tr>
                <th>Reunião</th>
                <th>Frequência</th>
                <th>O que acontece</th>
                <th>Participantes</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Reunião semanal ASCOM</strong></td>
                <td>Toda segunda-feira</td>
                <td>Seleção de pautas, divisão de tarefas, atualização de materiais em andamento e checagem do calendário da semana.</td>
                <td>14 comunicadores + pontos focais</td>
            </tr>
            <tr>
                <td><strong>Reunião com coordenação</strong></td>
                <td>A cada 15 dias</td>
                <td>Balanço das publicações. Alinhamento de pautas políticas e agendas. Orientação sobre temas sensíveis. Aprovação do calendário da próxima quinzena.</td>
                <td>Pontos focais + coordenação UNIVAJA</td>
            </tr>
            <tr>
                <td><strong>Reunião com associações</strong></td>
                <td>1 vez por mês</td>
                <td>Alinhamento com comunicadores das aldeias. Coleta de pautas das bases. Distribuição de boletins e informes internos.</td>
                <td>Comunicadores de base + pontos focais</td>
            </tr>
            <tr>
                <td><strong>Calendário quinzenal</strong></td>
                <td>Definido em cada reunião quinzenal</td>
                <td>Mínimo 6 postagens por quinzena: 2 da série associações + 2 pautas institucionais + 1 cobertura de evento + 1 data comemorativa ou cultural.</td>
                <td>ASCOM + aprovação coordenação</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # ── Calendário editorial fixo ────────────────────────────────────────────
    st.markdown("**Proposta de calendário editorial mínimo por semana:**")
    col_ca, col_cb, col_cc = st.columns(3)
    with col_ca:
        st.markdown(f"""
        <div class="card card-teal">
            <strong style="color:{VERDE}">Terça-feira</strong><br>
            <span style="font-size:13px">Série associações de base</span><br>
            <span style="font-size:12px;color:#6b7280">Instagram + WhatsApp</span>
        </div>
        """, unsafe_allow_html=True)
    with col_cb:
        st.markdown(f"""
        <div class="card card-roxo">
            <strong style="color:{VERDE_ESC}">Quinta-feira</strong><br>
            <span style="font-size:13px">Pauta institucional, agenda ou cobertura de evento</span><br>
            <span style="font-size:12px;color:#6b7280">Instagram + LinkedIn</span>
        </div>
        """, unsafe_allow_html=True)
    with col_cc:
        st.markdown(f"""
        <div class="card card-verde">
            <strong style="color:{VERDE}">Sábado (quinzenal)</strong><br>
            <span style="font-size:13px">Cultura, data comemorativa ou pauta positiva</span><br>
            <span style="font-size:12px;color:#6b7280">Instagram + WhatsApp</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Quem faz o quê ──────────────────────────────────────────────────────
    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown(section_title("Quem faz o quê — quadro de referência", "padrao"), unsafe_allow_html=True)

    pessoas = [
        ("Comunicador designado", "Propõe pauta, redige briefing e legenda, produz roteiro.", "Publicar nas redes sem aprovação."),
        ("Designer", "Cria cards seguindo manual de marca. Entrega ao ponto focal.", "Alterar identidade visual sem aval. Publicar sozinho."),
        ("Ponto focal indígena", "Articula equipe, envia material ao grupo ASCOM, aciona coordenação em temas sensíveis.", "Publicar material não aprovado pela coordenação geral."),
        ("FRAN", "Gerencia estratégia e conteúdo das redes sociais (Instagram + LinkedIn).", "Publicar sem aprovação ASCOM."),
        ("TUMI / DÉBORA", "Únicas com acesso ao perfil do Instagram. Publicam após aprovação.", "Publicar material não aprovado. Dar acesso ao Instagram sem aval."),
        ("Coordenação ASCOM", "Aprova ou solicita ajuste de materiais no grupo ASCOM.", "Emitir posicionamentos políticos sem aval da coordenação geral."),
        ("Coordenação geral UNIVAJA", "Valida pautas políticas e institucionais. Define posicionamento da organização.", "— (instância máxima de aprovação)"),
        ("Procuradoria jurídica", "Orienta sobre implicações legais de publicações sensíveis e denúncias.", "— (consultiva, não executa conteúdo)"),
    ]

    col_pq1, col_pq2 = st.columns(2)
    for i, (nome, faz, nao) in enumerate(pessoas):
        col = col_pq1 if i % 2 == 0 else col_pq2
        with col:
            st.markdown(f"""
            <div class="pessoa-card">
                <div class="pessoa-nome">👤 {nome}</div>
                <div class="pessoa-faz">✅ {faz}</div>
                <div class="pessoa-nao">🚫 Não faz sem orientação: {nao}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 2 — GLOSSÁRIO & REFERÊNCIA
# ══════════════════════════════════════════════════════════════════════════════
with aba2:

    st.markdown(section_title("Glossário básico e pautas de referência", "padrao"), unsafe_allow_html=True)
    st.caption("Respostas para as perguntas mais comuns da equipe sobre tipos de texto e temas prioritários.")

    col_g1, col_g2 = st.columns([1, 1])

    with col_g1:
        st.markdown("#### Tipos de formato")

        formatos = [
            ("Release", "Texto para jornalistas e veículos de imprensa. Conta um fato de interesse público de forma objetiva (quem, o quê, quando, onde, por quê, como). Nunca publicado diretamente nas redes.", "E-mail para jornalistas, portais, rádios"),
            ("Nota oficial", "Posicionamento formal da UNIVAJA sobre um fato ou situação. Linguagem direta, curta e institucional. Deve ser aprovada pela coordenação e procuradoria jurídica antes de ir a público.", "Site, redes sociais, imprensa"),
            ("Artigo", "Texto de análise e opinião, mais longo. Assinado por uma liderança ou comunicador. Pode abordar um tema com profundidade e perspectiva histórica.", "Site, portais de parceiros, boletins"),
            ("Card (post)", "Imagem (ou carrossel) com texto curto, formatada para redes sociais. Deve seguir o manual de marca obrigatoriamente.", "Instagram, Facebook, WhatsApp"),
            ("Legenda", "Texto que acompanha o card ou vídeo nas redes sociais. Deve ter chamada de abertura, informação principal e hashtags relevantes.", "Campo de descrição do post"),
            ("Vídeo / Reels", "Vídeo curto (15–90s) com roteiro, gravação e edição. Pode ser depoimento de liderança, cobertura de evento ou boletim informativo.", "Instagram (Reels), WhatsApp, YouTube"),
            ("Boletim interno", "Áudio ou texto com informações para as aldeias. Linguagem simples e acessível, nas línguas dos povos quando possível.", "WhatsApp dos comunicadores, rádio"),
        ]

        for titulo_f, desc, canal in formatos:
            st.markdown(f"""
            <div class="gloss-card">
                <div class="gloss-titulo">{titulo_f}</div>
                <div class="gloss-desc">{desc}</div>
                <span class="gloss-canal">📡 {canal}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_g2:
        st.markdown("#### Pautas prioritárias da UNIVAJA")

        st.markdown(f"""
        <div class="card card-azul" style="margin-bottom:8px">
            <strong style="color:{VERDE_PRETO};font-size:13px">📰 PAUTAS INFORMATIVAS</strong>
            <ul style="font-size:13px;margin:8px 0 0;padding-left:18px;line-height:1.8">
                <li>História de luta e conquistas dos Povos do Vale do Javari</li>
                <li>Demarcação da Terra Indígena — União dos Povos</li>
                <li>Conquista da saúde e educação indígena</li>
                <li>Informações sobre as 8 associações de base da UNIVAJA</li>
                <li>Agendas e atividades da coordenação (mobilizações, assembleias)</li>
                <li>Ameaças institucionais (PECs, projetos de lei)</li>
                <li>Informes sobre programas sociais (Bolsa Família, saúde)</li>
                <li>Informes sobre os povos isolados</li>
                <li>Direitos indígenas e papel das instituições</li>
                <li>Segurança digital: combate a notícias falsas</li>
            </ul>
        </div>
        <div class="card card-verde" style="margin-bottom:8px">
            <strong style="color:{VERDE};font-size:13px">🌱 PAUTAS POSITIVAS</strong>
            <ul style="font-size:13px;margin:8px 0 0;padding-left:18px;line-height:1.8">
                <li>Cultura dos Povos do Vale do Javari</li>
                <li>Datas comemorativas e celebrativas</li>
                <li>Festas e rituais dos Povos do Vale do Javari</li>
                <li>Atuação da UNIVAJA e das associações de base</li>
                <li>Protagonismo e lideranças indígenas</li>
            </ul>
        </div>
        <div class="card card-vermelho">
            <strong style="color:{PRIMARIA};font-size:13px">🚨 PAUTAS DE DENÚNCIA</strong>
            <ul style="font-size:13px;margin:8px 0 0;padding-left:18px;line-height:1.8">
                <li>Violência e violações de direitos</li>
                <li>Invasões e exploração do território</li>
                <li>Ameaças, perseguição ou assassinatos</li>
                <li>Racismo contra os Povos Indígenas</li>
            </ul>
            <div class="alerta" style="margin-top:8px;font-size:12px">
                ⚠️ Toda denúncia deve ser orientada pela Procuradoria Jurídica
                e validada pela coordenação antes de publicar.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Pilares da comunicação UNIVAJA")
        pilares = [
            ("Autodeterminação", "Os povos do Vale do Javari são protagonistas de suas próprias narrativas. Eles determinam o que, como e quando comunicar."),
            ("Luta e resistência", "A comunicação é ferramenta estratégica de defesa territorial e cultural."),
            ("Valorização cultural", "Fortalecer identidades, línguas e tradições dos povos do Vale do Javari."),
            ("Denúncia", "Expor publicamente violações de direitos — sempre com orientação jurídica."),
        ]
        for nome, desc in pilares:
            st.markdown(f"""
            <div class="card-grafismo" style="margin-bottom:10px">
                <div class="card-grafismo-conteudo">
                    <strong style="font-size:13px;color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">{nome}</strong>
                    <p style="font-size:12px;color:{CINZA};margin:6px 0 0;line-height:1.5">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 3 — AGENDA SEMANAL
# ══════════════════════════════════════════════════════════════════════════════
with aba3:

    st.markdown(section_title("Agenda da semana 02–08/06/2026", "padrao"), unsafe_allow_html=True)
    st.caption("Pautas prioritárias e checklists para cada publicação urgente desta semana.")

    agenda = [
        {
            "data": "02/06 · Segunda", "tipo": "Reunião interna", "cor": VERDE_PRETO,
            "pauta": "Reunião semanal ASCOM: briefar a equipe sobre as publicações de 04 e 05/06. Verificar status das associações de base pendentes. Definir responsáveis para cada entrega da semana.",
            "resp": "Ponto focal + todos os comunicadores",
            "check": ["Pauta da reunião preparada","Responsáveis para 04/06 definidos","Responsáveis para 05/06 definidos","Status da série associações atualizado"]
        },
        {
            "data": "03/06 · Terça", "tipo": "Produção", "cor": VERDE,
            "pauta": "Preparar card de divulgação do evento de Berlim (04/06). Checar contato com Pixi Matis ou organização do Amazon Week para receber registros fotográficos ao vivo.",
            "resp": "Designer + comunicador designado + FRAN",
            "check": ["Card de divulgação do evento criado","Legenda redigida com menção aos parceiros (RFN, BMZ)","Contato estabelecido com Pixi Matis ou org. do evento","Material aprovado no grupo ASCOM"]
        },
        {
            "data": "04/06 · Quarta", "tipo": "Cobertura — URGENTE", "cor": PRIMARIA,
            "pauta": "Indigenous Leadership at the Frontline — Amazon Week 2026, Berlim. Acompanhar o evento remotamente (10h–12h30 horário de Berlim = 7h–9h30 horário de Brasília). Coletar registros. Publicar cobertura até o final do dia.",
            "resp": "FRAN (redes) + comunicador de registro",
            "check": ["Card de divulgação publicado (manhã)","Evento acompanhado remotamente","Registros fotográficos coletados","Card de cobertura criado e aprovado","Publicação no Instagram, LinkedIn e WhatsApp"]
        },
        {
            "data": "05/06 · Quinta", "tipo": "Data sensível — URGENTE", "cor": VERMELHO_ESC,
            "pauta": "Aniversário do assassinato de Bruno Pereira e Dom Phillips (3 anos). Publicar nota/card em TODAS as redes no mesmo dia. Mesma publicação para Instagram, LinkedIn e WhatsApp. Validar com coordenação e procuradoria ANTES de publicar.",
            "resp": "Ponto focal + designer + coordenação + TUMI/DÉBORA",
            "check": ["Rascunho do card pronto até 04/06 à noite","Legenda redigida (tom: memória + resistência + denúncia)","Validação com coordenação geral","Validação com procuradoria jurídica","Aprovação no grupo ASCOM","Publicação simultânea nas 3 redes até as 9h do dia 05/06"]
        },
        {
            "data": "06–07/06 · Fim de semana", "tipo": "Série associações", "cor": VERDE,
            "pauta": "Manter a publicação das associações de base pendentes da semana. Das 8 associações previstas, verificar quantas já foram publicadas e quais faltam.",
            "resp": "Comunicador da série + designer",
            "check": ["Verificar quantas associações foram publicadas","Produzir as 2 associações da semana se pendentes","Aprovar no grupo ASCOM","Publicar no Instagram + WhatsApp"]
        },
        {
            "data": "08/06 · Domingo", "tipo": "Reunião com coordenação", "cor": VERDE_ESC,
            "pauta": "Reunião estratégica com a coordenação geral. Apresentar estrutura atual, fluxo de trabalho e proposta de agenda quinzenal. Definir acessos ao Instagram. Alinhar sobre a situação política.",
            "resp": "Todos + coordenação UNIVAJA",
            "check": ["Apresentação do fluxo operacional preparada","Proposta de calendário quinzenal elaborada","Lista de acessos ao Instagram para discutir","Pauta da reunião enviada com antecedência","Manual de marca compartilhado com a equipe","Organização da caixa de e-mail definida"]
        },
    ]

    for item in agenda:
        with st.expander(f"**{item['data']}** — {item['pauta'][:60]}...", expanded=False):
            st.markdown(f"""
            <div style="border-left:5px solid {item['cor']};padding:14px 18px;background:#fafafa;border-radius:0 10px 10px 0;margin-bottom:14px">
                <span style="background:{item['cor']};color:white;padding:3px 12px;border-radius:12px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px">{item['tipo']}</span>
                <p style="margin:12px 0 8px;font-size:14px;line-height:1.6;color:{CINZA}">{item['pauta']}</p>
                <p style="font-size:12px;color:#6b7280;margin:0"><strong>Responsável:</strong> {item['resp']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Checklist:**")
            for check in item["check"]:
                st.checkbox(check, key=f"{item['data']}_{check}")

    # Sugestão de conteúdo 05/06
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown(section_title("Sugestão de conteúdo — 05/06 (Bruno e Dom)", "vermelho"), unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"""
        <div class="card card-vermelho">
            <strong style="color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">Sugestão de texto para o card</strong>
            <p style="font-size:14px;font-style:italic;margin:12px 0;line-height:1.7;color:{CINZA}">
            "3 anos sem Bruno e Dom.<br>
            A UNIVAJA não esquece, não cala, não recua.<br>
            Sua luta é a nossa luta.<br>
            Território protegido, vidas respeitadas."
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div class="card card-cinza">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">Sugestão de legenda</strong>
            <p style="font-size:13px;margin:12px 0;line-height:1.7;color:{CINZA}">
            Em 5 de junho de 2022, Bruno Pereira e Dom Phillips foram assassinados no Vale do Javari.
            Três anos depois, a UNIVAJA reafirma: a proteção do território é uma questão de vida.
            Sua memória nos fortalece e nos guia.<br><br>
            #BrunoEDom #ValeDoJavari #UNIVAJA #PovosIndígenas #Amazônia
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alerta" style="margin-top:10px">
        ⚠️ <strong>Orientações para o 05/06:</strong> Tom respeitoso, firme e de memória ativa — não de lamento passivo.
        Evitar qualquer associação a questões políticas internas da UNIVAJA nesta data.
        Validar obrigatoriamente com coordenação e procuradoria antes de publicar.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 4 — MONITOR DE PAUTAS
# ══════════════════════════════════════════════════════════════════════════════
with aba4:

    st.markdown(section_title("Monitor de pautas — notícias e tendências", "padrao"), unsafe_allow_html=True)
    st.caption("Use antes da reunião de segunda (para sugerir pautas) e durante a produção (para embasar conteúdos).")

    st.markdown("""
    <div class="alerta alerta-azul">
        💡 <strong>Plataformas complementares:</strong><br>
        • <strong>Monitor UNIVAJA</strong> (<code>monitor_univaja.py</code>) — coleta automática de notícias via RSS de 12+ fontes.<br>
        • <strong>Planner UNIVAJA</strong> (<code>planner_univaja.py</code>) — planejamento de pautas, cronograma editorial e relatório PDF para a reunião.
    </div>
    """, unsafe_allow_html=True)

    col_mb, col_mp = st.columns([1, 1])
    with col_mb:
        st.markdown("**Quando usar:**")
        st.markdown("""
        <div style="display:flex;gap:8px;margin-bottom:12px">
            <span class="badge badge-seg">📅 Antes da reunião de segunda</span>
            <span class="badge badge-prod">✏️ Durante a produção</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 1 · Selecione os temas")

    TEMAS_MONITOR_DEFAULT = {
        "Povos isolados": {"tag": "pauta permanente", "badge": "badge-perm",
            "termos": ["povos isolados Vale do Javari", "isolados voluntários Amazônia", "FUNAI isolados"]},
        "Garimpo e invasão": {"tag": "denúncia / vigilância", "badge": "badge-den",
            "termos": ["garimpo ilegal Vale do Javari", "invasão terra indígena Javari", "mineração ilegal Amazônia"]},
        "Direitos indígenas": {"tag": "pauta política", "badge": "badge-perm",
            "termos": ["direitos indígenas Brasil 2025", "demarcação terra indígena", "marco temporal indígena"]},
        "FUNAI e políticas": {"tag": "institucional", "badge": "badge-seg",
            "termos": ["FUNAI política indigenista", "ministério povos indígenas", "política indigenista Brasil"]},
        "Violência e assassinatos": {"tag": "denúncia", "badge": "badge-den",
            "termos": ["violência contra indígenas Amazônia", "assassinato liderança indígena", "conflito terra indígena"]},
        "Bruno e Dom": {"tag": "memória", "badge": "badge-pos",
            "termos": ["Bruno Pereira Dom Phillips", "aniversário Vale do Javari", "jornalista indigenista assassinado"]},
        "Meio ambiente": {"tag": "ambiental", "badge": "badge-pos",
            "termos": ["desmatamento Amazônia Vale do Javari", "proteção territorial indígena", "biodiversidade Javari"]},
        "Saúde indígena": {"tag": "social", "badge": "badge-pos",
            "termos": ["saúde indígena SESAI Javari", "doenças comunidades indígenas", "assistência médica aldeia"]},
        "Educação indígena": {"tag": "social", "badge": "badge-pos",
            "termos": ["educação escolar indígena Amazônia", "escola indígena Javari", "educação bilíngue indígena"]},
        "Amazon Week 2026": {"tag": "evento atual", "badge": "badge-int",
            "termos": ["Amazon Week 2026 Berlin", "liderança indígena fronteira", "UNIVAJA international event"]},
        "Clima e COP": {"tag": "internacional", "badge": "badge-int",
            "termos": ["mudança climática povos indígenas", "COP indigena Amazônia", "clima floresta tropical"]},
        "Atalaia do Norte": {"tag": "local", "badge": "badge-local",
            "termos": ["Atalaia do Norte notícias", "Amazonas terra indígena", "Vale do Javari município"]},
    }

    if "temas_monitor" not in st.session_state:
        st.session_state.temas_monitor = {k: dict(v) for k, v in TEMAS_MONITOR_DEFAULT.items()}
    TEMAS = st.session_state.temas_monitor

    cols_temas = st.columns(4)
    selecionados_temas = []
    for i, (tema, info) in enumerate(TEMAS.items()):
        with cols_temas[i % 4]:
            sel = st.checkbox(tema, key=f"tema_{tema}")
            if sel:
                selecionados_temas.append(tema)
            st.markdown(f'<span class="badge {info["badge"]}" style="font-size:10px">{info["tag"]}</span>', unsafe_allow_html=True)

    st.markdown(divisor("pontos"), unsafe_allow_html=True)

    st.markdown("#### 2 · Ou adicione um termo específico")
    col_ti, col_tb = st.columns([4, 1])
    with col_ti:
        termo_custom = st.text_input("", placeholder="Ex: garimpo ilegal, saúde indígena, Atalaia do Norte...", label_visibility="collapsed")
    with col_tb:
        adicionar = st.button("+ Adicionar", use_container_width=True)

    if "termos_extras" not in st.session_state:
        st.session_state.termos_extras = []
    if adicionar and termo_custom and termo_custom not in st.session_state.termos_extras:
        st.session_state.termos_extras.append(termo_custom)

    if st.session_state.termos_extras:
        st.markdown("**Termos adicionados:**")
        cols_rem = st.columns(len(st.session_state.termos_extras) + 1)
        for i, t in enumerate(st.session_state.termos_extras):
            with cols_rem[i]:
                if st.button(f"✕ {t}", key=f"rem_{t}"):
                    st.session_state.termos_extras.remove(t)
                    st.rerun()

    st.markdown("#### 3 · Período")
    periodo = st.radio("", ["Última semana", "Último mês", "Último ano"],
                       horizontal=True, label_visibility="collapsed")
    periodo_gn = {"Última semana": "w", "Último mês": "m", "Último ano": "y"}[periodo]
    periodo_gt = {"Última semana": "past_7_days", "Último mês": "past_month", "Último ano": "past_12_months"}[periodo]

    todos_termos = []
    for tema in selecionados_temas:
        todos_termos.extend(TEMAS[tema]["termos"])
    todos_termos.extend(st.session_state.termos_extras)
    todos_termos = list(dict.fromkeys(todos_termos))

    if not todos_termos:
        todos_termos = ["UNIVAJA", "povos indígenas Vale do Javari", "Vale do Javari"]

    q_encoded = "+OR+".join([t.replace(" ", "+") for t in todos_termos[:4]])
    q_trends  = ",".join(todos_termos[:5])

    url_gnoticias = f"https://news.google.com/search?q={q_encoded}&hl=pt-BR&gl=BR&ceid=BR:pt-BR&as_qdr={periodo_gn}"
    url_gsearch   = f"https://www.google.com/search?q={q_encoded}&tbm=nws&hl=pt-BR&tbs=qdr:{periodo_gn}"
    url_trends    = f"https://trends.google.com/trends/explore?q={q_trends}&geo=BR&date={periodo_gt}&hl=pt-BR"
    url_trends_ex = f"https://trends.google.com/trends/explore?q={todos_termos[0].replace(' ','+')}&geo=BR&hl=pt-BR"

    st.markdown(divisor("zig"), unsafe_allow_html=True)
    st.markdown("#### 4 · Abra as buscas")

    if selecionados_temas or st.session_state.termos_extras:
        st.markdown(f"""
        <div class="alerta alerta-verde">
            ✅ <strong>{len(todos_termos)} termos selecionados.</strong>
            Clique nos links abaixo para abrir as buscas já com esses termos.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alerta">
            💡 Selecione ao menos um tema acima para personalizar os links de busca.
        </div>
        """, unsafe_allow_html=True)

    if todos_termos:
        pills = " ".join([f'<span class="termo-pill">{t}</span>' for t in todos_termos])
        st.markdown(f"<div style='margin-bottom:14px'>{pills}</div>", unsafe_allow_html=True)

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown(f"""
        <a href="{url_gnoticias}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">📰 Google Notícias →</div>
            <div class="link-busca-desc">Manchetes recentes com os termos selecionados. Ideal para identificar pautas em evidência.</div>
        </a>
        <a href="{url_gsearch}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">🔎 Google Search News →</div>
            <div class="link-busca-desc">Busca de notícias com filtro de período. Complementa o Google Notícias com mais resultados.</div>
        </a>
        """, unsafe_allow_html=True)
    with col_l2:
        st.markdown(f"""
        <a href="{url_trends}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">📈 Google Trends — comparativo →</div>
            <div class="link-busca-desc">Veja qual dos termos está mais em alta no Brasil no período escolhido.</div>
        </a>
        <a href="{url_trends_ex}" target="_blank" class="link-busca">
            <div class="link-busca-titulo">🔬 Google Trends — explorar →</div>
            <div class="link-busca-desc">Explora o primeiro termo em profundidade: buscas relacionadas, regiões e interesse ao longo do tempo.</div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown(divisor("pontos"), unsafe_allow_html=True)
    st.markdown("#### 5 · O que fazer com o que encontrou")

    col_o1, col_o2 = st.columns(2)
    with col_o1:
        st.markdown(f"""
        <div class="card card-azul">
            <strong style="color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">📅 Antes da reunião de segunda</strong>
            <p style="font-size:13px;margin-top:10px;line-height:1.6;color:{CINZA}">
            Selecione 3–5 notícias relevantes e leve como sugestão de pauta.
            Anote qual temática está em alta para justificar a escolha.
            Indique o formato sugerido (card, vídeo ou boletim).
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_o2:
        st.markdown(f"""
        <div class="card card-verde">
            <strong style="color:{VERDE};text-transform:uppercase;letter-spacing:0.5px">✏️ Durante a produção (ter–qua)</strong>
            <p style="font-size:13px;margin-top:10px;line-height:1.6;color:{CINZA}">
            Use as notícias para embasar o card ou o roteiro do vídeo.
            Cite a fonte no briefing enviado ao designer.
            Verifique se o tema ainda é atual antes de publicar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ── Editor de temas ─────────────────────────────────────────────────────
    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.markdown("#### ⚙️ Personalizar temas e termos de busca")
    st.caption("Edite os temas e os termos que vão para o Google Notícias e Google Trends. Funciona para a sessão atual; baixe o JSON para preservar.")

    with st.expander("✏️ Editar temas existentes", expanded=False):
        st.caption("Formato: `TEMA: termo1, termo2, termo3` — um tema por linha.")
        temas_atuais_txt = "\n".join([
            f"{tema}: {', '.join(info['termos'])}" for tema, info in TEMAS.items()
        ])
        editor = st.text_area("Temas e termos",
            value=temas_atuais_txt, height=320, label_visibility="collapsed",
            key="editor_temas_monitor")

        col_save, col_reset = st.columns([3, 1])
        with col_save:
            if st.button("💾 Salvar alterações nos temas", type="primary", use_container_width=True):
                novos = {}
                for linha in editor.split("\n"):
                    if ":" in linha:
                        tema, termos = linha.split(":", 1)
                        tema = tema.strip()
                        termos_list = [t.strip() for t in termos.split(",") if t.strip()]
                        if tema and termos_list:
                            # preserva tag/badge se já existia
                            tag_antigo = TEMAS.get(tema, {}).get("tag", "personalizado")
                            badge_antigo = TEMAS.get(tema, {}).get("badge", "badge-perm")
                            novos[tema] = {"tag": tag_antigo, "badge": badge_antigo, "termos": termos_list}
                st.session_state.temas_monitor = novos
                st.success("✅ Temas atualizados!")
                st.rerun()
        with col_reset:
            if st.button("↺ Resetar", use_container_width=True):
                st.session_state.temas_monitor = {k: dict(v) for k, v in TEMAS_MONITOR_DEFAULT.items()}
                st.rerun()

    with st.expander("➕ Adicionar um novo tema"):
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            novo_tema_nome = st.text_input("Nome do tema", placeholder="ex: Festival cultural")
        with col_n2:
            novo_tema_termos = st.text_input("Termos (separados por vírgula)",
                placeholder="ex: festival yoxin, ritual marubo")
        if st.button("Adicionar tema", use_container_width=True):
            if novo_tema_nome and novo_tema_termos:
                termos_list = [t.strip() for t in novo_tema_termos.split(",") if t.strip()]
                st.session_state.temas_monitor[novo_tema_nome.strip()] = {
                    "tag": "personalizado", "badge": "badge-perm", "termos": termos_list,
                }
                st.success(f"✅ Tema '{novo_tema_nome}' adicionado!")
                st.rerun()

    # Backup
    import json as _json
    cfg_export = _json.dumps(st.session_state.temas_monitor, ensure_ascii=False, indent=2)
    col_bk1, col_bk2 = st.columns(2)
    with col_bk1:
        st.download_button("📥 Baixar temas (JSON)", cfg_export,
            file_name=f"temas_monitor_univaja.json", mime="application/json",
            use_container_width=True)
    with col_bk2:
        arq_t = st.file_uploader("📤 Importar temas", type=["json"],
            label_visibility="collapsed", key="upload_temas_monitor")
        if arq_t is not None:
            try:
                data = _json.loads(arq_t.read())
                if isinstance(data, dict):
                    if st.button("Confirmar importação", key="conf_temas"):
                        st.session_state.temas_monitor = data
                        st.success("✅ Temas importados!"); st.rerun()
            except Exception as ex:
                st.error(f"Erro: {ex}")


# ══════════════════════════════════════════════════════════════════════════════
#  ABA 5 — COMO USAR
# ══════════════════════════════════════════════════════════════════════════════
with aba5:

    st.markdown(section_title("Como usar esta plataforma", "padrao"), unsafe_allow_html=True)

    col_u1, col_u2 = st.columns([1.2, 1])

    with col_u1:
        st.markdown("#### O que é esta ferramenta?")
        st.markdown("""
        Esta plataforma foi criada especificamente para a ASCOM da UNIVAJA.
        Ela centraliza em um único lugar:

        - Os fluxos operacionais completos de comunicação
        - O glossário de formatos e pautas prioritárias
        - A agenda semanal com checklists
        - O monitor de notícias e tendências com links diretos

        **Identidade visual:** segue o **Manual de Marca UNIVAJA**, com cores e grafismos
        dos povos do Vale do Javari (Marubo, Matis, Kanamari, Kulina, Mayuruna)
        aplicados em bordas, divisores e elementos decorativos.

        Não precisa instalar nada. Funciona pelo navegador de qualquer
        celular ou computador com internet.
        """)

        st.markdown("#### Quem usa e quando?")

        usos = [
            ("📅 Domingo / Segunda cedo", "Comunicador responsável da semana abre o app **Monitor UNIVAJA**, seleciona os temas, filtra pelo período e salva 5–10 matérias para levar à reunião."),
            ("🤝 Reunião de segunda", "Ponto focal abre a aba **Fluxos integrados** para guiar a divisão de tarefas. Cada pessoa sai sabendo exatamente o que faz."),
            ("✏️ Terça e quarta", "Comunicadores abrem o **Monitor UNIVAJA** durante a produção para buscar notícias que embasem o card ou roteiro."),
            ("✅ Quinta e sexta", "Ponto focal usa a aba **Fluxos** para lembrar o processo de aprovação antes de enviar ao grupo ASCOM."),
            ("📋 Reunião quinzenal", "Ponto focal apresenta a aba **Fluxos integrados** para a coordenação como referência do processo."),
        ]
        for momento, desc in usos:
            st.markdown(f"""
            <div class="card-grafismo" style="margin-bottom:10px">
                <div class="card-grafismo-conteudo">
                    <strong style="font-size:13px;color:{VERDE_PRETO};text-transform:uppercase;letter-spacing:0.5px">{momento}</strong>
                    <p style="font-size:13px;margin-top:8px;line-height:1.6;color:{CINZA}">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_u2:
        st.markdown("#### 🧰 Outras plataformas UNIVAJA")
        st.markdown(f"""
        <div class="card-grafismo" style="margin-bottom:10px">
            <div class="card-grafismo-conteudo">
                <strong style="font-size:13px;color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">📰 Monitor UNIVAJA</strong>
                <p style="font-size:12px;margin-top:6px;line-height:1.5;color:{CINZA}">
                Coleta automática de notícias por RSS de 12+ fontes de mídia indígena, ambiental e geral.
                Filtros por tema, salvar favoritas e exportação para a reunião.
                </p>
            </div>
        </div>
        <div class="card-grafismo" style="margin-bottom:10px">
            <div class="card-grafismo-conteudo">
                <strong style="font-size:13px;color:{PRIMARIA};text-transform:uppercase;letter-spacing:0.5px">📋 Planner UNIVAJA</strong>
                <p style="font-size:12px;margin-top:6px;line-height:1.5;color:{CINZA}">
                Planejamento editorial colaborativo. Comunicadores propõem pautas, definem cronograma,
                redes, responsáveis. Notifica a imprensa por email e gera PDF para a reunião.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 💡 Princípios da ferramenta")
        principios = [
            ("🎨 Identidade", "Segue rigorosamente o Manual de Marca UNIVAJA — cores e grafismos dos povos do Vale."),
            ("📱 Acessível", "Funciona no navegador de qualquer celular ou computador. Não precisa instalar nada."),
            ("⚙️ Customizável", "Temas, termos, fontes e templates de email são editáveis pelos comunicadores."),
            ("🤝 Colaborativa", "Quem usa pode exportar JSON e compartilhar no grupo ASCOM."),
        ]
        for titulo_p, desc in principios:
            st.markdown(f"""
            <div class="card card-cinza" style="margin-bottom:8px">
                <strong style="font-size:13px;color:{VERDE_PRETO}">{titulo_p}</strong>
                <p style="font-size:12px;color:{CINZA};margin:4px 0 0;line-height:1.5">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(divisor("marubo"), unsafe_allow_html=True)
    st.caption("ASCOM UNIVAJA · 2026 — uso interno · Identidade visual baseada no Manual de Marca UNIVAJA")
