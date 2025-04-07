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

            # Usar o nome do usuário se disponível, caso contrário usar o nome do petshop
            nome_usuario = ""
            if hasattr(dados, "nome") and dados.nome:
                nome_usuario = dados.nome
            else:
                # Fallback para o nome do petshop como antes
                nome_usuario = (
                    dados.nome_petshop.split()[0]
                    if " " in dados.nome_petshop
                    else dados.nome_petshop
                )

            # Enviar email com PDF anexado
            email_result = email_handler.send_pdf_report(
                nome=nome_usuario,
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


def create_pdf_email_button(dados, resultado, key_suffix, col_widths=[2, 3, 2]):
    """
    Função para criar o botão de envio de PDF por email.

    Args:
        dados: Dados do petshop
        resultado: Resultados da análise
        key_suffix: Sufixo para a chave do botão (top ou bottom)
        col_widths: Lista com as proporções das colunas
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
            Veja as <span style="color: #0a8a40;">recomendações práticas</span> abaixo para reverter esta situação.
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

    # Vamos adicionar um estilo CSS específico para o layout de tabela
    st.markdown(
        """
    <style>
        /* Estilo de tabela com linhas alternadas para as seções de análise */
        .table-container {
            border-collapse: collapse;
            width: 100%;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .table-header {
            padding: 15px;
            font-weight: 600;
            color: #fff;
            text-align: center;
            font-size: 18px;
        }
        
        .table-row {
            display: flex;
            flex-wrap: wrap;
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }
        
        .table-row:last-child {
            border-bottom: none;
        }
        
        .table-cell {
            flex: 1;
            min-width: 300px;
            padding: 15px;
        }
        
        /* Cores específicas para cada tipo de tabela */
        .inefficiencies-header { background-color: #e74c3c; }
        .inefficiencies-row:nth-child(odd) { background-color: #fff0f0; }
        .inefficiencies-row:nth-child(even) { background-color: #fff8f8; }
        
        .recommendations-header { background-color: #0a8a40; }
        .recommendations-row:nth-child(odd) { background-color: #e8f8e8; }
        .recommendations-row:nth-child(even) { background-color: #f0fff4; }
        
        .priorities-header { background-color: #0a8a40; }
        .priorities-row:nth-child(odd) { background-color: #e8f8e8; }
        .priorities-row:nth-child(even) { background-color: #f0fff4; }
        
        .goals-header { background-color: #3498db; }
        .goals-row:nth-child(odd) { background-color: #e3f2fd; }
        .goals-row:nth-child(even) { background-color: #ebf5fb; }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Relatório com recomendações
    st.markdown(
        """
        <h2 style="color: #2c3e50; font-size: 26px; margin: 40px 0 25px 0; 
                  text-align: center; font-weight: 700; position: relative; padding-bottom: 12px;">
            Análise e Recomendações
            <span style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); 
                   width: 100px; height: 4px; background-color: #3498db;"></span>
        </h2>
        """,
        unsafe_allow_html=True,
    )

    relatorio = prepare_financial_report(dados, resultado)

    # Saúde Financeira com suporte a HTML
    st.markdown(
        """
        <h3 style="color: #3498db; font-size: 22px; margin: 35px 0 20px 0; 
                  position: relative; text-align: left; padding-left: 15px; font-weight: 600;">
            <span style="position: relative; display: inline-block;">
                💼 Saúde Financeira Atual
                <span style="position: absolute; bottom: -8px; left: 0; width: 100%; height: 3px; background-color: #3498db;"></span>
            </span>
        </h3>
        """,
        unsafe_allow_html=True,
    )

    # Card moderno para a Saúde Financeira
    saude_financeira_conteudo = (
        relatorio["saude_financeira"].replace("</div>", "").strip()
    )

    st.markdown(
        f"""
    <div style="background-color: #f8fafc; border-radius: 8px; 
                border-left: 4px solid #3498db; padding: 20px; margin-bottom: 30px; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
        {saude_financeira_conteudo}
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Novo layout tipo tabela para Ineficiências
    st.markdown(
        """
        <h3 style="color: #e74c3c; font-size: 22px; margin: 35px 0 20px 0; 
                  position: relative; text-align: left; padding-left: 15px; font-weight: 600;">
            <span style="position: relative; display: inline-block; color: #e74c3c;">
                🚨 Principais Ineficiências
                <span style="position: absolute; bottom: -8px; left: 0; width: 100%; height: 3px; background-color: #e74c3c;"></span>
            </span>
        </h3>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="table-container" style="border-radius: 8px; margin-top: 10px;">
    """,
        unsafe_allow_html=True,
    )

    for i, ineficiencia in enumerate(relatorio["ineficiencias"]):
        st.markdown(
            f"""
        <div class="table-row inefficiencies-row">
            <div class="table-cell">
                <h5 style="color: #e74c3c; margin-top: 0;">🔴 {i+1}. {ineficiencia['titulo']}</h5>
                <p style="margin-bottom: 0;">{ineficiencia['descricao']}</p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Novo layout tipo tabela para Recomendações
    st.markdown(
        """
        <h3 style="color: #0a8a40; font-size: 22px; margin: 35px 0 20px 0; 
                  position: relative; text-align: left; padding-left: 15px; font-weight: 600;">
            <span style="position: relative; display: inline-block; color: #0a8a40">
                💡 Recomendações Práticas
                <span style="position: absolute; bottom: -8px; left: 0; width: 100%; height: 3px; background-color: #0a8a40;"></span>
            </span>
        </h3>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="table-container" style="border-radius: 8px; margin-top: 10px;">
    """,
        unsafe_allow_html=True,
    )

    for i, recomendacao in enumerate(relatorio["recomendacoes"]):
        st.markdown(
            f"""
        <div class="table-row recommendations-row">
            <div class="table-cell">
                <h5 style="color: #0a8a40; margin-top: 0;">✅ {i+1}. {recomendacao['titulo']}</h5>
                <p>{recomendacao['descricao']}</p>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 15px;">
                    <div style="background-color: rgba(46, 204, 113, 0.15); padding: 8px 12px; border-radius: 20px;">
                        <span style="font-weight: bold; color: #27ae60;">💰 Impacto:</span> {recomendacao['impacto']}
                    </div>
                    <div style="background-color: rgba(52, 152, 219, 0.15); padding: 8px 12px; border-radius: 20px;">
                        <span style="font-weight: bold; color: #2980b9;">⏱️ Prazo:</span> {recomendacao['prazo']}
                    </div>
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Novo layout tipo tabela para Prioridades
    st.markdown(
        """
        <h3 style="color: #0a8a40; font-size: 22px; margin: 35px 0 20px 0; 
                  position: relative; text-align: left; padding-left: 15px; font-weight: 600;">
            <span style="position: relative; display: inline-block; color: #0a8a40">
                🎯 Prioridades de Curto Prazo
                <span style="position: absolute; bottom: -8px; left: 0; width: 100%; height: 3px; background-color: #0a8a40;"></span>
            </span>
        </h3>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="table-container" style="border-radius: 8px; margin-top: 10px;">
    """,
        unsafe_allow_html=True,
    )

    for i, prioridade in enumerate(relatorio["prioridades"]):
        st.markdown(
            f"""
        <div class="table-row priorities-row">
            <div class="table-cell">
                <h5 style="color: #0a8a40; margin-top: 0;">⚡ {i+1}. {prioridade['titulo']}</h5>
                <p style="margin-bottom: 0;">{prioridade['descricao']}</p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Novo layout tipo tabela para Metas
    st.markdown(
        """
        <h3 style="color: #3498db; font-size: 22px; margin: 35px 0 20px 0; 
                  position: relative; text-align: left; padding-left: 15px; font-weight: 600;">
            <span style="position: relative; display: inline-block;">
                📈 Metas Sugeridas
                <span style="position: absolute; bottom: -8px; left: 0; width: 100%; height: 3px; background-color: #3498db;"></span>
            </span>
        </h3>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="table-container" style="border-radius: 8px; margin-top: 10px;">
    """,
        unsafe_allow_html=True,
    )

    for i, meta in enumerate(relatorio["metas"]):
        st.markdown(
            f"""
        <div class="table-row goals-row">
            <div class="table-cell">
                <h5 style="color: #3498db; margin-top: 0;">🏆 {i+1}. {meta['titulo']}</h5>
                <p style="margin-bottom: 0;">{meta['descricao']}</p>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

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
                <h5 style="color: #2c3e50; margin-top: 0;">✅ O que oferecemos:</h5>
                <ul style="padding-left: 20px; margin-top: 10px;">
                    <li>Implementação das recomendações personalizadas</li>
                    <li>Treinamento da sua equipe para maximizar resultados</li>
                    <li>Acompanhamento mensal de indicadores</li>
                    <li>Estratégias de marketing para aumentar o fluxo de clientes</li>
                </ul>
            </div>
            <div style="flex: 1; min-width: 200px;">
                <h5 style="color: #2c3e50; margin-top: 0;">💰 Resultados esperados:</h5>
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
                # Usar o nome do usuário se disponível, caso contrário usar o nome do petshop
                nome_usuario = ""
                if hasattr(dados, "nome") and dados.nome:
                    nome_usuario = dados.nome
                else:
                    # Fallback para o nome do petshop como antes
                    nome_usuario = (
                        dados.nome_petshop.split()[0]
                        if " " in dados.nome_petshop
                        else dados.nome_petshop
                    )

                email = dados.email_contato
                telefone = getattr(dados, "telefone_contato", "")
                mensagem = st.session_state.get("contato_mensagem", "")

                lead_handler.create_lead(
                    name=nome_usuario,
                    email=email,
                    whatsapp=telefone,
                    petshop_name=dados.nome_petshop,
                    message=mensagem,
                    source="streamlit",
                )

                # Enviar email de confirmação para o cliente
                email_handler.send_contact_confirmation(
                    nome=nome_usuario,
                    email=email,
                    petshop_name=dados.nome_petshop,
                    mensagem=mensagem,
                )

                # Enviar notificação interna para a equipe
                internal_recipients = os.getenv("DOGS_CLUB_INTERNAL_EMAILS").split(",")
                email_handler.send_internal_notification(
                    nome=nome_usuario,
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
