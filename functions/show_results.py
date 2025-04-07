import streamlit as st
import os

from utils import format_currency, format_percent
from .create_data_visualizations import create_data_visualizations
from .prepare_financial_report import prepare_financial_report
from .export_pdf import export_dashboard_pdf
from handlers.email_handler import EmailHandler
from handlers.lead_handler import LeadHandler

# Configuração dos handlers
email_handler = EmailHandler()
lead_handler = LeadHandler()


def handle_export_pdf(dados, resultado):
    """
    Função centralizada para lidar com a exportação de PDF que será usada por ambos os botões.
    Gera PDF e envia por email sem opção de download.

    Args:
        dados: Dados do petshop
        resultado: Resultados da análise
    """
    try:
        # Verificar se o email está disponível
        if not hasattr(dados, "email_contato") or not dados.email_contato:
            st.error(
                "É necessário informar um email de contato para receber o relatório PDF."
            )
            return

        # Gerar relatório PDF
        with st.spinner("Gerando relatório PDF e enviando para seu email..."):
            relatorio = prepare_financial_report(dados, resultado)
            figuras = create_data_visualizations(resultado)
            pdf_buffer = export_dashboard_pdf(dados, resultado, relatorio, figuras)

            # Garantir que email não seja vazio
            email = dados.email_contato
            if not email or email.strip() == "":
                raise ValueError("Email de contato não pode ser vazio")

            # Enviar email com PDF anexado
            email_result = email_handler.send_pdf_report(
                nome=(
                    dados.nome_petshop.split()[0]
                    if " " in dados.nome_petshop
                    else dados.nome_petshop
                ),
                email=email,
                petshop_name=dados.nome_petshop,
                faturamento_nao_realizado=resultado.faturamento_nao_realizado,
                pdf_buffer=pdf_buffer,
            )

            if email_result["success"]:
                st.success(
                    f"Relatório PDF enviado com sucesso para {email}! Verifique sua caixa de entrada.",
                    icon="✅",
                )
            else:
                st.error(
                    f"Não foi possível enviar o email. Erro: {email_result.get('error', 'Desconhecido')}"
                )
    except Exception as e:
        st.error(f"Erro ao gerar ou enviar o PDF: {str(e)}")


def create_pdf_email_button(dados, resultado, key_suffix, col_widths=[2, 1, 2]):
    """
    Função para criar o botão de envio de PDF por email.

    Args:
        dados: Dados do petshop
        resultado: Resultados da análise
        key_suffix: Sufixo para a chave do botão (top ou bottom)
        col_widths: Lista com as proporções das colunas (padrão [2, 1, 2])
    """
    col1, col2, col3 = st.columns(col_widths)
    with col2:
        if st.button(
            "📄 Enviar PDF por Email",
            type="primary",
            key=f"export_pdf_{key_suffix}",
            use_container_width=True,
        ):
            handle_export_pdf(dados, resultado)


def show_results(dados, resultado):
    """Exibe os resultados da análise do petshop"""
    # Adicionar logo no header

    st.markdown(
        f"<h1 class='main-header'>Análise Financeira - {dados.nome_petshop}</h1>",
        unsafe_allow_html=True,
    )

    # Botão com largura limitada e cor azul
    create_pdf_email_button(dados, resultado, "top")

    # Principais métricas
    st.markdown(
        "<div class='section-header'>Métricas Principais</div>", unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    # Coluna 1 - Faturamento
    with col1:
        st.markdown(
            "<div class='metric-label'>Faturamento Mensal</div>", unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='metric-value'>{format_currency(resultado.faturamento_atual)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='metric-subvalue'>Potencial: {format_currency(resultado.faturamento_potencial)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Coluna 2 - Lucro
    with col2:
        st.markdown(
            "<div class='metric-label'>Lucro Mensal</div>", unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='metric-value'>{format_currency(resultado.lucro_atual)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='metric-subvalue'>Margem: {format_percent(resultado.margem_lucro)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Coluna 3 - Ocupação
    with col3:
        st.markdown(
            "<div class='metric-label'>Taxa de Ocupação</div>", unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='metric-value'>{format_percent(resultado.ocupacao_atual_percentual)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='metric-subvalue'>Tempo ocioso: {resultado.tempo_ocioso_diario:.1f}h/dia</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Destaque - Dinheiro deixado na mesa
    st.html(
        f"""
        <div style='color: #e74c3c; font-weight: 700; font-size: 2rem; text-align: center; margin-bottom: 15px;'>
        ⚠️ Potencial Não Aproveitado ⚠️
        </div>
        
        <div style="background-color: #fdf2f2; border-left: 6px solid #e74c3c; padding: 25px; 
        border-radius: 10px; margin: 15px 0;">
            <p style="font-size: 16px; color: #e74c3c; margin-bottom: 20px; font-weight: 500;">
            Nossos cálculos mostram que seu petshop está deixando dinheiro na mesa e não aproveitando
            sua capacidade total. Veja abaixo o <b>quanto você está perdendo</b>:
            </p>
            
            <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
                <div style="flex: 1; min-width: 250px; text-align: center;">
                    <h3 style='color: #e74c3c; margin-top: 0;'>
                    💸 Dinheiro Deixado na Mesa</h3>
                    
                    <h2 style='color: #e74c3c; font-weight: 800; font-size: 2.5rem; text-align: center;'>
                    {format_currency(resultado.faturamento_nao_realizado * 12)}/ano</h2>
                    
                    <p style='color: #e74c3c; font-weight: 500; text-align: center;'>
                    Valor que você está <u>deixando de ganhar</u> anualmente</p>
                </div>
                
                <div style="flex: 1; min-width: 250px; text-align: center;">
                    <h3 style='color: #e74c3c; margin-top: 0;'>
                    ⏱️ Capacidade Não Utilizada</h3>
                    
                    <h2 style='color: #e74c3c; font-weight: 800; font-size: 2.5rem; text-align: center;'>
                    {resultado.capacidade_mensal_ideal - dados.numero_atendimentos_mes} atendimentos/mês</h2>
                    
                    <p style='color: #e74c3c; font-weight: 500; text-align: center;'>
                    Clientes que <u>poderiam ser atendidos</u> com sua estrutura atual</p>
                </div>
            </div>
            
            <div style='text-align: center; margin: 25px auto; padding: 15px; 
            background-color: #e74c3c; color: white; border-radius: 5px; font-weight: 600; max-width: 90%;'>
            <span style="color: white !important; font-size: 18px;">Você está perdendo aproximadamente <b>{format_currency(resultado.faturamento_nao_realizado)}</b> <b>todos os meses!</b></span>
            </div>
            
            <p style="text-align: center; margin-top: 15px; font-weight: 500;">
            Veja as <span style="color: #2ecc71;">recomendações práticas</span> abaixo para reverter esta situação.
            </p>
        </div>
        """
    )

    # Visualizações
    st.markdown(
        "<div class='section-header'>Visualizações</div>", unsafe_allow_html=True
    )

    # Criar gráficos
    figuras = create_data_visualizations(resultado)

    # Primeira linha de gráficos
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(figuras[0])
    with col2:
        st.pyplot(figuras[1])

    # Segunda linha de gráficos
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(figuras[2])
    with col2:
        st.pyplot(figuras[3])

    # Botão de exportar PDF em destaque (no topo)
    col1, col2, col3 = st.columns([1, 2, 1])

    # Relatório com recomendações
    st.markdown(
        "<div class='section-header'>Análise e Recomendações</div>",
        unsafe_allow_html=True,
    )

    relatorio = prepare_financial_report(dados, resultado)

    # Saúde Financeira com suporte a HTML
    st.markdown("### 💼 Saúde Financeira Atual")
    st.markdown(relatorio["saude_financeira"], unsafe_allow_html=True)

    # Ineficiências com emojis e cores (mantendo vermelho para ineficiências)
    st.markdown("### 🚨 Principais Ineficiências")
    for i, ineficiencia in enumerate(relatorio["ineficiencias"]):
        st.markdown(
            f"<h4 style='color: #e74c3c;'>🔴 {i+1}. {ineficiencia['titulo']}</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(ineficiencia["descricao"], unsafe_allow_html=True)

    # Recomendações com emojis, cores e suporte a HTML
    st.markdown(
        "### 💡 <span style='color: #2ecc71;'>Recomendações Práticas</span>",
        unsafe_allow_html=True,
    )
    for i, recomendacao in enumerate(relatorio["recomendacoes"]):
        st.markdown(
            f"<h4 style='color: #2ecc71;'>✅ {i+1}. {recomendacao['titulo']}</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(recomendacao["descricao"], unsafe_allow_html=True)

        # Usar HTML para formatação de negrito
        st.markdown(
            f"<p><span style='font-weight: bold; color: #27ae60;'>💰 Impacto estimado:</span> {recomendacao['impacto']}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p><span style='font-weight: bold; color: #2980b9;'>⏱️ Prazo sugerido:</span> {recomendacao['prazo']}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<hr style='margin: 15px 0; opacity: 0.3;'>", unsafe_allow_html=True
        )

    # Prioridades com emojis e cores
    st.markdown("### 🎯 Prioridades de Curto Prazo")
    for i, prioridade in enumerate(relatorio["prioridades"]):
        st.markdown(
            f"<h4 style='color: #f39c12;'>⚡ {i+1}. {prioridade['titulo']}</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(prioridade["descricao"], unsafe_allow_html=True)

    # Metas com emojis e cores
    st.markdown("### 📈 Metas Sugeridas")
    for i, meta in enumerate(relatorio["metas"]):
        st.markdown(
            f"<h4 style='color: #3498db;'>🏆 {i+1}. {meta['titulo']}</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(meta["descricao"], unsafe_allow_html=True)

    # Removido a seção "Exportar Relatório" e adicionado o botão no footer
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Estilo CSS personalizado para botão azul e padronização de tamanhos
    st.markdown(
        """
    <style>
        /* Estilo para botões primários */
        div.stButton > button[kind="primary"] {
            background-color: #3498db;
            border-color: #3498db;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #2980b9;
            border-color: #2980b9;
        }
        
        /* Padronizar tamanho dos botões */
        div.stButton > button {
            min-width: 160px;
            height: 46px;
            font-size: 16px;
            font-weight: 500;
            padding: 4px 20px;
            border-radius: 6px;
        }
        
        /* Exceção para botões de navegação */
        div.stButton > button[kind="secondary"] {
            min-width: 120px;
        }
        
        /* Todas as cores vermelhas substituídas por azul */
        .css-1qg05tj {
            color: #3498db !important;
        }
        
        /* Padrão para botões nas colunas centrais */
        [data-testid="column"]:nth-child(2) div.stButton > button {
            width: 100%;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Botão para exportar PDF no footer
    create_pdf_email_button(dados, resultado, "bottom")

    # Seção de consultoria melhorada
    st.markdown(
        "<div class='section-header'>🚀 Turbine os Resultados do Seu Petshop</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="contact-card" style="background-color: #f0f7fb; padding: 25px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #3498db;">
        <h3 style="color: #2980b9; margin-top: 0;">💼 Consultoria Especializada Dog's Club</h3>
        <div style="display: flex; gap: 20px; margin: 15px 0; flex-wrap: wrap;">
            <div style="flex: 1; min-width: 200px;">
                <h4 style="color: #2c3e50; margin-top: 0;">✅ O que oferecemos:</h4>
                <ul style="padding-left: 20px; margin-top: 10px;">
                    <li>Implementação das recomendações personalizadas</li>
                    <li>Treinamento da sua equipe para maximizar resultados</li>
                    <li>Acompanhamento mensal de indicadores</li>
                    <li>Estratégias de marketing para aumentar o fluxo de clientes</li>
                </ul>
            </div>
            <div style="flex: 1; min-width: 200px;">
                <h4 style="color: #2c3e50; margin-top: 0;">💰 Resultados esperados:</h4>
                <ul style="padding-left: 20px; margin-top: 10px;">
                    <li>Aumento do faturamento em até 30%</li>
                    <li>Melhoria da taxa de ocupação</li>
                    <li>Otimização dos custos operacionais</li>
                    <li>Maior rentabilidade e crescimento sustentável</li>
                </ul>
            </div>
        </div>
        <p style="font-style: italic; margin-top: 15px; color: #34495e;">Nossos consultores tem vasta experiência no mercado pet e já ajudaram vários petshops a alcançar seus objetivos de negócio.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Formulário de contato simplificado
    st.markdown(
        "<h3 style='color: #3498db; margin-top: 20px;'>📋 Solicite um Diagnóstico Gratuito</h3>",
        unsafe_allow_html=True,
    )

    st.text_area(
        "Como podemos ajudar?",
        placeholder="Descreva os principais desafios do seu petshop...",
        height=120,
        key="contato_mensagem",
    )

    # Botão de envio estilizado
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💬 Solicitar Contato", type="primary", use_container_width=True):
            # Se tivermos os dados do cliente
            if hasattr(dados, "nome_petshop") and hasattr(dados, "email_contato"):
                nome = (
                    dados.nome_petshop.split()[0]
                    if " " in dados.nome_petshop
                    else dados.nome_petshop
                )
                email = dados.email_contato
                telefone = getattr(dados, "telefone_contato", "")
                mensagem = st.session_state.get("contato_mensagem", "")

                # Criar lead no DynamoDB
                print("DADOS DO CLIENTE", dados)
                print(f"Email: '{email}', Tipo: {type(email)}")
                print(f"Nome: '{nome}', Telefone: '{telefone}'")

                lead_handler.create_lead(
                    name=nome,
                    email=email,
                    whatsapp=telefone,
                    petshop_name=dados.nome_petshop,
                    message=mensagem,
                    source="streamlit",
                )

                # Enviar email de confirmação para o cliente
                email_handler.send_contact_confirmation(
                    nome=nome,
                    email=email,
                    petshop_name=dados.nome_petshop,
                    mensagem=mensagem,
                )

                # Enviar notificação interna para a equipe
                internal_recipients = os.getenv("DOGS_CLUB_INTERNAL_EMAILS").split(",")
                email_handler.send_internal_notification(
                    nome=nome,
                    email=email,
                    whatsapp=telefone,
                    petshop_name=dados.nome_petshop,
                    mensagem=mensagem,
                    fonte="relatorio_financeiro_streamlit",
                    internal_recipients=internal_recipients,
                )

            st.success(
                "Solicitação enviada com sucesso! Nossa equipe entrará em contato em até 24 horas.",
                icon="✅",
            )
