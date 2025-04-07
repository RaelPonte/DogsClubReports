"""
Dog's Club - Aplicativo de Análise Financeira para Petshops

Este aplicativo Streamlit permite a análise financeira detalhada de petshops
com visualizações, métricas e recomendações personalizadas.

Principais funcionalidades:
- Coleta de dados estruturados em etapas
- Análise de métricas financeiras e operacionais
- Visualizações gráficas dos resultados
- Recomendações personalizadas
- Exportação do relatório em PDF

Desenvolvido para a Dog's Club
© 2025 Dog's Club. Todos os direitos reservados.
"""

import streamlit as st
import warnings
import re
from dotenv import load_dotenv

load_dotenv()

# Importação dos módulos personalizados
from functions import (
    extract_form_data,
    analyze_petshop_data,
    show_results,
    define_css,
)

# Suprimir avisos
warnings.filterwarnings("ignore")

# Configuração da página - DEVE SER A PRIMEIRA CHAMADA STREAMLIT
st.set_page_config(
    page_title="Dog's Club - Análise de Petshop",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="collapsed",  # Mantém o sidebar fechado inicialmente
    menu_items={
        "Get Help": "mailto:suporte@dogsclub.com.br",
        "Report a bug": "mailto:suporte@dogsclub.com.br",
        "About": "Dog's Club - Análise Financeira de Petshops. Todos os direitos reservados.",
    },
)

define_css()


def on_email_change():
    """Função callback para garantir que o email seja salvo"""
    st.session_state["email_salvo"] = st.session_state.get("email_contato", "")
    # Também registrar no log para depuração
    print(f"Email salvo: {st.session_state['email_salvo']}")


# Função para validar formato de hora
def validar_formato_hora(hora):
    if not hora or not hora.strip():
        return False
    return bool(re.match(r"^\d{1,2}:\d{2}$", hora))


# Função para criar o cabeçalho do formulário
def create_header():
    st.markdown("<h1 class='main-header'>Dog's Club</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h2 class='sub-header'>Análise Financeira de Petshop</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='form-caption'>
            <h3 style="margin-top: 0; color: #3498db;">📊 Analise o desempenho do seu Petshop</h3>
            <p>Este formulário possui <b>5 etapas</b> com perguntas sobre seu petshop. Ao final, clique no botão <b>Analisar Dados</b> para receber um relatório completo.</p>
            <p><b>⏱️ Tempo de preenchimento:</b> 5 minutos</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Função para mostrar a barra de progresso
def show_progress(step_number, total_steps=5):
    st.markdown("<div class='progress-container'>", unsafe_allow_html=True)
    progress = step_number / total_steps
    st.progress(progress)
    st.markdown(
        f"<p style='text-align: center;'>Etapa {step_number} de {total_steps}</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# Função para o Passo 1 - Informações Básicas
def step_1_basic_info():
    st.markdown("### 📝 Etapa 1: Informações Básicas")
    st.markdown("Preencha os dados de identificação do seu petshop.")

    # Recuperar valor da sessão, se existir
    nome_petshop_valor = st.session_state.get("nome_petshop", "Petshop Feliz")
    st.text_input(
        "Nome do Petshop",
        value=nome_petshop_valor,
        key="nome_petshop",
        help="Nome comercial do seu estabelecimento",
    )

    col1, col2 = st.columns(2)
    with col1:
        # Recuperar valor da sessão, se existir
        if "email_salvo" not in st.session_state:
            st.session_state["email_salvo"] = st.session_state.get("email_contato", "")

        email_contato_valor = st.session_state.get("email_contato", "")
        # Simples campo de email sem manipulações complexas
        st.text_input(
            "Email de Contato",
            value=email_contato_valor,
            key="email_contato",
            help="Email principal para contato",
            on_change=on_email_change,
        )
    with col2:
        # Recuperar valor da sessão, se existir
        telefone_contato_valor = st.session_state.get("telefone_contato", "")
        st.text_input(
            "Telefone",
            value=telefone_contato_valor,
            key="telefone_contato",
            help="Número de telefone com DDD",
        )

    st.markdown("</div>", unsafe_allow_html=True)
    navigation_buttons(1)


# Função para o Passo 2 - Operação
def step_2_operation():
    st.markdown("### ⏰ Etapa 2: Horário de Funcionamento")
    st.markdown("Informe os horários e dias de funcionamento do seu petshop.")

    col1, col2 = st.columns(2)
    with col1:
        horario_abertura = st.text_input(
            "Horário de Abertura (formato HH:MM)",
            value=st.session_state.get("horario_abertura", "08:00"),
            key="horario_abertura",
            help="Digite o horário no formato HH:MM, por exemplo: 08:00",
        )
        # Garantir formato válido
        if not validar_formato_hora(horario_abertura):
            st.warning(
                "Por favor, preencha o horário de abertura no formato HH:MM (exemplo: 08:00)"
            )
            st.session_state["horario_abertura"] = "08:00"
    with col2:
        horario_fechamento = st.text_input(
            "Horário de Fechamento (formato HH:MM)",
            value=st.session_state.get("horario_fechamento", "18:00"),
            key="horario_fechamento",
            help="Digite o horário no formato HH:MM, por exemplo: 18:00",
        )
        # Garantir formato válido
        if not validar_formato_hora(horario_fechamento):
            st.warning(
                "Por favor, preencha o horário de fechamento no formato HH:MM (exemplo: 18:00)"
            )
            st.session_state["horario_fechamento"] = "18:00"

    st.slider(
        "Dias de Funcionamento por Semana",
        min_value=1,
        max_value=7,
        value=st.session_state.get("dias_funcionamento_semana", 6),
        key="dias_funcionamento_semana",
        help="Quantos dias por semana seu petshop funciona?",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    navigation_buttons(2)


# Função para o Passo 3 - Equipe e Serviços
def step_3_team_services():
    st.markdown("### 👥 Etapa 3: Equipe e Serviços")

    st.markdown("#### Equipe")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input(
            "Total de Funcionários",
            min_value=1,
            value=st.session_state.get("numero_funcionarios", 3),
            key="numero_funcionarios",
            help="Número total de funcionários, incluindo administrativo",
        )
    with col2:
        st.number_input(
            "Funcionários de Banho/Tosa",
            min_value=1,
            value=st.session_state.get("funcionarios_banho_tosa", 2),
            key="funcionarios_banho_tosa",
            help="Quantos funcionários trabalham diretamente com banho e tosa",
        )

    st.number_input(
        "Salário Médio (R$)",
        min_value=500.0,
        value=st.session_state.get("salario_medio", 1800.0),
        step=100.0,
        key="salario_medio",
        help="Valor médio do salário por funcionário, incluindo encargos",
    )

    st.markdown("#### Serviços")
    col1, col2 = st.columns(2)
    with col1:
        st.slider(
            "Tempo Médio de Banho/Tosa (minutos)",
            min_value=30,
            max_value=180,
            value=st.session_state.get("tempo_medio_banho_tosa", 90),
            key="tempo_medio_banho_tosa",
            help="Tempo médio de atendimento para banho e tosa, em minutos",
        )
        # Garantir valor mínimo
        if (
            "tempo_medio_banho_tosa" not in st.session_state
            or st.session_state["tempo_medio_banho_tosa"] < 30
        ):
            st.session_state["tempo_medio_banho_tosa"] = 30
    with col2:
        st.number_input(
            "Atendimentos por Mês",
            min_value=1,
            value=st.session_state.get("numero_atendimentos_mes", 200),
            key="numero_atendimentos_mes",
            help="Número total de atendimentos de banho e tosa realizados por mês",
        )

    st.number_input(
        "Ticket Médio (R$)",
        min_value=10.0,
        value=st.session_state.get("ticket_medio", 90.0),
        step=5.0,
        key="ticket_medio",
        help="Valor médio gasto por cliente em cada atendimento",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    navigation_buttons(3)


# Função para o Passo 4 - Financeiro
def step_4_financial():
    st.markdown("### 💰 Etapa 4: Informações Financeiras")

    st.markdown("#### Receitas")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input(
            "Faturamento Mensal (R$)",
            min_value=0.0,
            value=st.session_state.get("faturamento_mensal", 18000.0),
            step=1000.0,
            key="faturamento_mensal",
            help="Faturamento total do último mês",
        )
    with col2:
        st.number_input(
            "Faturamento Mês Anterior (R$)",
            min_value=0.0,
            value=st.session_state.get("faturamento_mes_anterior", 17000.0),
            step=1000.0,
            key="faturamento_mes_anterior",
            help="Faturamento total do mês anterior ao último",
        )

    st.markdown("#### Despesas")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input(
            "Despesa Água/Luz (R$)",
            min_value=0.0,
            value=st.session_state.get("despesa_agua_luz", 800.0),
            step=100.0,
            key="despesa_agua_luz",
            help="Gastos mensais com água e energia elétrica",
        )
        st.number_input(
            "Despesa Produtos (R$)",
            min_value=0.0,
            value=st.session_state.get("despesa_produtos", 3600.0),
            step=100.0,
            key="despesa_produtos",
            help="Gastos com produtos utilizados nos serviços (shampoo, etc.)",
        )
    with col2:
        st.number_input(
            "Despesa Aluguel (R$)",
            min_value=0.0,
            value=st.session_state.get("despesa_aluguel", 2500.0),
            step=100.0,
            key="despesa_aluguel",
            help="Valor mensal do aluguel do imóvel",
        )
        st.number_input(
            "Outras Despesas (R$)",
            min_value=0.0,
            value=st.session_state.get("despesa_outros", 1000.0),
            step=100.0,
            key="despesa_outros",
            help="Outros gastos mensais não categorizados",
        )

    st.markdown("</div>", unsafe_allow_html=True)
    navigation_buttons(4)


# Função para o Passo 5 - Metas e Desafios
def step_5_goals():
    st.markdown("### 🎯 Etapa 5: Metas e Desafios")

    st.number_input(
        "Meta de Lucro Mensal (R$)",
        min_value=0.0,
        value=st.session_state.get("meta_lucro", 6000.0),
        step=1000.0,
        key="meta_lucro",
        help="Qual é o lucro mensal que você deseja alcançar",
    )

    st.text_area(
        "Principal Desafio",
        value=st.session_state.get(
            "principal_desafio",
            "Aumentar o número de clientes e melhorar a rentabilidade.",
        ),
        key="principal_desafio",
        help="Descreva o principal desafio que seu petshop enfrenta atualmente",
    )

    st.markdown(
        """
    <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px; border-left: 3px solid #3498db;">
        <h4 style="color: #3498db; margin-top: 0;">✅ Pronto para analisar!</h4>
        <p>Você completou todas as etapas do formulário. Clique no botão "Analisar Dados" abaixo para receber seu relatório completo.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
    navigation_buttons(5)


# Função para os botões de navegação
def navigation_buttons(step):
    col1, col2 = st.columns(2)

    with col1:
        if step > 1:
            if st.button("← Voltar", key=f"back_{step}"):
                # Garante que os dados da etapa atual sejam salvos antes de voltar
                st.session_state["current_step"] = step - 1
                st.rerun()

    with col2:
        if step < 5:
            if st.button("Próximo →", key=f"next_{step}", type="primary"):
                # Os dados já estão automaticamente salvos em session_state pelo Streamlit
                # quando os widgets são criados com a opção "key"
                st.session_state["current_step"] = step + 1
                st.rerun()
        else:
            if st.button("📊 Analisar Dados", key="submit", type="primary"):
                with st.spinner("Analisando dados do petshop..."):
                    email = st.session_state.get(
                        "email_contato", st.session_state.get("email_salvo", "")
                    )
                    if not email or email.strip() == "":
                        st.error(
                            "O campo de Email de Contato é obrigatório. Por favor, volte à Etapa 1 e preencha o email."
                        )
                    # Verificar e garantir que os dados estão válidos antes de processar
                    if (
                        "horario_abertura" not in st.session_state
                        or not validar_formato_hora(
                            st.session_state["horario_abertura"]
                        )
                    ):
                        st.session_state["horario_abertura"] = "08:00"

                    if (
                        "horario_fechamento" not in st.session_state
                        or not validar_formato_hora(
                            st.session_state["horario_fechamento"]
                        )
                    ):
                        st.session_state["horario_fechamento"] = "18:00"

                    if (
                        "tempo_medio_banho_tosa" not in st.session_state
                        or st.session_state["tempo_medio_banho_tosa"] < 30
                    ):
                        st.session_state["tempo_medio_banho_tosa"] = 30

                    # Extrair dados do formulário
                    try:
                        dados = extract_form_data()

                        if dados:
                            # Realizar análise
                            resultado = analyze_petshop_data(dados)

                            # Armazenar resultado na sessão
                            st.session_state["petshop_data"] = dados
                            st.session_state["analysis_result"] = resultado
                            st.session_state["current_page"] = "results"

                            # Recarregar a página para mostrar os resultados
                            st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao processar os dados: {str(e)}")
                        st.info(
                            "Por favor, verifique se todos os campos obrigatórios estão preenchidos corretamente."
                        )


# Criar uma versão simplificada da barra lateral
def create_simple_sidebar():
    with st.sidebar:
        st.image(
            "https://dogs-club-source.s3.us-east-1.amazonaws.com/logo.png",
            width=180,
        )

        st.markdown("## Ajuda")
        st.markdown(
            """
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
            <h4 style="margin-top: 0;">Como preencher o formulário:</h4>
            <ol>
                <li>Preencha cada etapa com as informações do seu petshop</li>
                <li>Use os botões "Próximo" e "Voltar" para navegar entre as etapas</li>
                <li>No final, clique em "Analisar Dados"</li>
                <li>Receba seu relatório completo!</li>
            </ol>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("## Contato")
        st.markdown(
            """
        <div style="background-color: #f0f7fb; padding: 15px; border-radius: 8px; border-left: 3px solid #3498db;">
            <p><b>📧 suporte@dogsclub.com.br</b></p>
            <p><b>📱 (11) 99748-5353</b></p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Verificar se current_page existe e se está na página de resultados
        if (
            "current_page" in st.session_state
            and st.session_state["current_page"] == "results"
        ):
            if st.button(
                "🔄 Iniciar Nova Análise",
                key="sidebar_new",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["current_page"] = "form"
                st.session_state["current_step"] = 1
                st.rerun()


# Função principal que orquestra a aplicação
def main():
    # Configuração inicial do estado da sessão
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "form"

    if "current_step" not in st.session_state:
        st.session_state["current_step"] = 1

    # Capturar a URL de referência para identificação da fonte de tráfego
    if "referrer" not in st.session_state:
        # Tenta obter o referrer dos query parameters
        try:
            query_params = st.query_params
            if "ref" in query_params:
                st.session_state["referrer"] = query_params["ref"]
            elif "utm_source" in query_params:
                st.session_state["referrer"] = query_params["utm_source"]
            else:
                st.session_state["referrer"] = "direct"
        except:
            st.session_state["referrer"] = "direct"

    # Inicializar todos os campos do formulário que serão necessários em todas as etapas
    # Etapa 1: Informações Básicas
    if "nome_petshop" not in st.session_state:
        st.session_state["nome_petshop"] = "Petshop Feliz"
    if "email_contato" not in st.session_state:
        st.session_state["email_contato"] = ""
    if "telefone_contato" not in st.session_state:
        st.session_state["telefone_contato"] = ""

    # Etapa 2: Operação
    if "horario_abertura" not in st.session_state:
        st.session_state["horario_abertura"] = "08:00"
    if "horario_fechamento" not in st.session_state:
        st.session_state["horario_fechamento"] = "18:00"
    if "dias_funcionamento_semana" not in st.session_state:
        st.session_state["dias_funcionamento_semana"] = 6

    # Etapa 3: Equipe e Serviços
    if "numero_funcionarios" not in st.session_state:
        st.session_state["numero_funcionarios"] = 3
    if "funcionarios_banho_tosa" not in st.session_state:
        st.session_state["funcionarios_banho_tosa"] = 2
    if "salario_medio" not in st.session_state:
        st.session_state["salario_medio"] = 1800.0
    if "tempo_medio_banho_tosa" not in st.session_state:
        st.session_state["tempo_medio_banho_tosa"] = 90
    if "numero_atendimentos_mes" not in st.session_state:
        st.session_state["numero_atendimentos_mes"] = 200
    if "ticket_medio" not in st.session_state:
        st.session_state["ticket_medio"] = 90.0

    # Etapa 4: Financeiro
    if "faturamento_mensal" not in st.session_state:
        st.session_state["faturamento_mensal"] = 18000.0
    if "faturamento_mes_anterior" not in st.session_state:
        st.session_state["faturamento_mes_anterior"] = 17000.0
    if "despesa_agua_luz" not in st.session_state:
        st.session_state["despesa_agua_luz"] = 800.0
    if "despesa_produtos" not in st.session_state:
        st.session_state["despesa_produtos"] = 3600.0
    if "despesa_aluguel" not in st.session_state:
        st.session_state["despesa_aluguel"] = 2500.0
    if "despesa_outros" not in st.session_state:
        st.session_state["despesa_outros"] = 1000.0

    # Etapa 5: Metas
    if "meta_lucro" not in st.session_state:
        st.session_state["meta_lucro"] = 6000.0
    if "principal_desafio" not in st.session_state:
        st.session_state["principal_desafio"] = (
            "Aumentar o número de clientes e melhorar a rentabilidade."
        )

    # Renderizar o formulário ou resultados
    if st.session_state["current_page"] == "form":
        # Opção 1: Usar o fluxo de etapas
        create_header()
        show_progress(st.session_state["current_step"])

        # Mostrar a etapa atual do formulário
        if st.session_state["current_step"] == 1:
            step_1_basic_info()
        elif st.session_state["current_step"] == 2:
            step_2_operation()
        elif st.session_state["current_step"] == 3:
            step_3_team_services()
        elif st.session_state["current_step"] == 4:
            step_4_financial()
        elif st.session_state["current_step"] == 5:
            step_5_goals()

    elif st.session_state["current_page"] == "results":
        if "petshop_data" in st.session_state and "analysis_result" in st.session_state:

            show_results(
                st.session_state["petshop_data"], st.session_state["analysis_result"]
            )

            # Botão para iniciar uma nova análise
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button(
                    "🔄 Iniciar Nova Análise", type="primary", use_container_width=True
                ):
                    st.session_state["current_page"] = "form"
                    st.session_state["current_step"] = 1
                    st.rerun()
        else:
            st.error(
                "Não há resultados disponíveis. Por favor, faça a análise primeiro."
            )
            st.session_state["current_page"] = "form"
            st.session_state["current_step"] = 1
            st.rerun()

    # Adicionar rodapé da página
    st.markdown(
        """
        <div class="footer">
            <p>Dog's Club - Conectando Pets e Cuidados com Simplicidade</p>
            <p>© 2025 Dog's Club. Todos os direitos reservados.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def debug_session_state():
    with st.expander("Debug Session State", expanded=False):
        st.write(st.session_state)


# debug_session_state()
# Adicionar a barra lateral simplificada
create_simple_sidebar()

# Executar a aplicação
if __name__ == "__main__":
    main()
