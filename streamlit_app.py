import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import warnings

# Importação dos módulos personalizados
from assets import (
    WORKING_DAYS_IN_THE_MONTH,
    SERVICES_TIME,
    COLORS,
    INDUSTRY_STANDARD,
)
from utils import (
    fmt_money,
    fmt_pct,
    format_currency,
    format_percent,
    format_time,
)
from dataclass import PetshopData, AnalisysResult

# Suprimir avisos
warnings.filterwarnings("ignore")

# Configurar estilo do matplotlib
plt.style.use("ggplot")

# Configuração da página
st.set_page_config(
    page_title="Dog's Club - Análise de Petshop",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Adicionar CSS personalizado
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #3498db;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #3498db;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: white;
        border-radius: 5px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #2c3e50;
        font-weight: bold;
    }
    .metric-subvalue {
        font-size: 1.2rem;
        color: #7f8c8d;
    }
    .highlight-card {
        background-color: #f8f9fa;
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #f0f0f0;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def create_sidebar():
    """Cria a barra lateral com informações e links úteis"""
    st.sidebar.image(
        "https://dogs-club-source.s3.us-east-1.amazonaws.com/logo.png",
        width=200,
    )

    st.sidebar.markdown("## Sobre a Dog's Club")
    st.sidebar.markdown(
        """
    A Dog's Club é uma plataforma inovadora que revoluciona a forma como tutores de pets e pet shops se conectam.
    
    Nossa missão é facilitar a vida de quem ama seus pets, eliminando a frustração de telefonemas, mensagens de WhatsApp e agendamentos confusos.
    """
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("## Como usar a ferramenta")
    st.sidebar.markdown(
        """
    1. Preencha os dados do seu petshop nos formulários
    2. Analise os resultados e visualizações
    3. Receba recomendações personalizadas
    4. Exporte os resultados
    """
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("## Contato")
    st.sidebar.markdown(
        """
    📧 suporte@dogsclub.com.br  
    📱 (11) 99748-5353
    """
    )

    # Botão para iniciar uma nova análise
    if st.sidebar.button("Iniciar Nova Análise", type="primary"):
        st.session_state.current_page = "form"
        st.rerun()


def extract_form_data():
    """Extrai os dados dos formulários e cria um objeto PetshopData"""
    dados = {}

    # Informações básicas
    dados["nome_petshop"] = st.session_state.get("nome_petshop", "")
    dados["email_contato"] = st.session_state.get("email_contato", "")
    dados["telefone_contato"] = st.session_state.get("telefone_contato", "")

    # Operação
    dados["horario_abertura"] = st.session_state.get("horario_abertura", "")
    dados["horario_fechamento"] = st.session_state.get("horario_fechamento", "")
    dados["dias_funcionamento_semana"] = st.session_state.get(
        "dias_funcionamento_semana", 6
    )

    # Equipe
    dados["numero_funcionarios"] = st.session_state.get("numero_funcionarios", 0)
    dados["funcionarios_banho_tosa"] = st.session_state.get(
        "funcionarios_banho_tosa", 0
    )
    dados["salario_medio"] = st.session_state.get("salario_medio", 0.0)

    # Serviços
    dados["tempo_medio_banho_tosa"] = st.session_state.get("tempo_medio_banho_tosa", 0)
    dados["numero_atendimentos_mes"] = st.session_state.get(
        "numero_atendimentos_mes", 0
    )
    dados["ticket_medio"] = st.session_state.get("ticket_medio", 0.0)

    # Financeiro
    dados["faturamento_mensal"] = st.session_state.get("faturamento_mensal", 0.0)
    dados["faturamento_mes_anterior"] = st.session_state.get(
        "faturamento_mes_anterior", 0.0
    )
    dados["despesa_agua_luz"] = st.session_state.get("despesa_agua_luz", 0.0)
    dados["despesa_produtos"] = st.session_state.get("despesa_produtos", 0.0)
    dados["despesa_aluguel"] = st.session_state.get("despesa_aluguel", 0.0)
    dados["despesa_outros"] = st.session_state.get("despesa_outros", 0.0)

    # Metas
    dados["meta_lucro"] = st.session_state.get("meta_lucro", 0.0)
    dados["principal_desafio"] = st.session_state.get("principal_desafio", "")

    # Calcular percentual de produtos sobre o faturamento
    if dados["faturamento_mensal"] > 0:
        dados["custo_produto_percentual"] = (
            dados["despesa_produtos"] / dados["faturamento_mensal"]
        ) * 100
    else:
        dados["custo_produto_percentual"] = 0

    # Calcular custo fixo total
    dados["custo_fixo_mensal"] = (
        dados["despesa_agua_luz"]
        + dados["despesa_aluguel"]
        + dados["despesa_outros"]
        + (dados["salario_medio"] * dados["numero_funcionarios"])
    )

    try:
        return PetshopData(**dados)
    except Exception as e:
        st.error(f"Erro ao validar os dados: {str(e)}")
        return None


def calculate_working_hours(dados):
    """Calcula horas de trabalho diárias e mensais"""
    formato = "%H:%M"
    hora_abertura = datetime.strptime(dados.horario_abertura, formato)
    hora_fechamento = datetime.strptime(dados.horario_fechamento, formato)

    # Ajuste para horários que passam da meia-noite
    if hora_fechamento < hora_abertura:
        hora_fechamento = datetime.strptime(f"23:59", formato)

    horas_operacao_diaria = (hora_fechamento - hora_abertura).total_seconds() / 3600
    dias_uteis = WORKING_DAYS_IN_THE_MONTH * (
        dados.dias_funcionamento_semana / 5
    )  # Ajuste baseado nos dias de funcionamento
    horas_operacao_mensal = horas_operacao_diaria * dias_uteis

    return {
        "diaria": horas_operacao_diaria,
        "mensal": horas_operacao_mensal,
        "dias_uteis": dias_uteis,
    }


def calculate_capacity_metrics(dados, horas_operacao):
    """Calcula métricas de capacidade e ocupação"""
    # Calcular capacidade diária ideal por funcionário
    # Assumindo que cada funcionário de banho e tosa trabalha 85% do seu tempo em atendimentos
    eficiencia_trabalho = 0.85  # 85% do tempo é produtivo
    capacidade_funcionario = (
        horas_operacao["diaria"] * 60 * eficiencia_trabalho
    ) / dados.tempo_medio_banho_tosa  # animais/dia

    # Capacidade diária total da equipe de banho e tosa
    capacidade_diaria_ideal = int(
        capacidade_funcionario * dados.funcionarios_banho_tosa
    )

    # Capacidade mensal ideal
    capacidade_mensal_ideal = int(
        capacidade_diaria_ideal * horas_operacao["dias_uteis"]
    )

    # Percentual da capacidade utilizada
    percentual_capacidade = (
        (dados.numero_atendimentos_mes / capacidade_mensal_ideal * 100)
        if capacidade_mensal_ideal > 0
        else 0
    )

    # Tempo ocioso diário em horas
    atendimentos_diarios_atuais = (
        dados.numero_atendimentos_mes / horas_operacao["dias_uteis"]
    )
    horas_produtivas_diarias = (
        atendimentos_diarios_atuais * dados.tempo_medio_banho_tosa
    ) / 60
    horas_potenciais_diarias = (
        horas_operacao["diaria"] * dados.funcionarios_banho_tosa * eficiencia_trabalho
    )
    tempo_ocioso_diario = max(0, horas_potenciais_diarias - horas_produtivas_diarias)

    return {
        "capacidade_diaria_ideal": capacidade_diaria_ideal,
        "capacidade_mensal_ideal": capacidade_mensal_ideal,
        "percentual_capacidade": percentual_capacidade,
        "tempo_ocioso_diario": tempo_ocioso_diario,
    }


def calculate_financial_metrics(dados, capacidade):
    """Calcula métricas financeiras"""
    # Despesas com pessoal
    despesa_pessoal = dados.salario_medio * dados.numero_funcionarios

    # Despesas totais
    despesa_total = (
        despesa_pessoal
        + dados.despesa_agua_luz
        + dados.despesa_produtos
        + (dados.despesa_aluguel or 0)
        + (dados.despesa_outros or 0)
    )

    # Faturamento potencial mensal
    faturamento_potencial = capacidade["capacidade_mensal_ideal"] * dados.ticket_medio

    # Faturamento não realizado (potencial perdido)
    faturamento_nao_realizado = faturamento_potencial - dados.faturamento_mensal

    # Lucratividade
    lucro_atual = dados.faturamento_mensal - despesa_total
    margem_lucro = (
        (lucro_atual / dados.faturamento_mensal * 100)
        if dados.faturamento_mensal > 0
        else 0
    )

    # Lucro potencial
    custo_produto_potencial = (
        faturamento_potencial * (dados.custo_produto_percentual / 100)
        if dados.custo_produto_percentual
        else 0
    )
    custo_fixo = (
        despesa_total - dados.despesa_produtos
    )  # Simplificação - considerando produtos como único custo variável
    lucro_potencial = faturamento_potencial - custo_produto_potencial - custo_fixo

    # Estrutura de Custos
    proporcao_pessoal = (
        (despesa_pessoal / despesa_total * 100) if despesa_total > 0 else 0
    )
    proporcao_produtos = (
        (dados.despesa_produtos / despesa_total * 100) if despesa_total > 0 else 0
    )
    proporcao_aluguel = (
        ((dados.despesa_aluguel or 0) / despesa_total * 100) if despesa_total > 0 else 0
    )

    # Eficiência por funcionário
    atendimentos_por_funcionario = (
        dados.numero_atendimentos_mes / dados.funcionarios_banho_tosa
        if dados.funcionarios_banho_tosa > 0
        else 0
    )
    atendimentos_potenciais_por_funcionario = (
        capacidade["capacidade_mensal_ideal"] / dados.funcionarios_banho_tosa
        if dados.funcionarios_banho_tosa > 0
        else 0
    )
    receita_por_funcionario = (
        dados.faturamento_mensal / dados.funcionarios_banho_tosa
        if dados.funcionarios_banho_tosa > 0
        else 0
    )
    receita_potencial_por_funcionario = (
        faturamento_potencial / dados.funcionarios_banho_tosa
        if dados.funcionarios_banho_tosa > 0
        else 0
    )

    # Ponto de equilíbrio
    margem_contribuicao_percentual = 100 - (dados.custo_produto_percentual or 0)
    margem_contribuicao_unitaria = dados.ticket_medio * (
        margem_contribuicao_percentual / 100
    )
    ponto_equilibrio_atendimentos = (
        int(custo_fixo / margem_contribuicao_unitaria)
        if margem_contribuicao_unitaria > 0
        else 0
    )

    # Crescimento
    crescimento_receita = None
    if dados.faturamento_mes_anterior:
        crescimento_receita = (
            (dados.faturamento_mensal - dados.faturamento_mes_anterior)
            / dados.faturamento_mes_anterior
            * 100
        )

    # Verificação de meta
    diferenca_meta = None
    if dados.meta_lucro is not None:
        diferenca_meta = lucro_atual - dados.meta_lucro

    return {
        "despesa_total": despesa_total,
        "despesa_pessoal": despesa_pessoal,
        "faturamento_potencial": faturamento_potencial,
        "faturamento_nao_realizado": faturamento_nao_realizado,
        "lucro_atual": lucro_atual,
        "lucro_potencial": lucro_potencial,
        "margem_lucro": margem_lucro,
        "proporcao_pessoal": proporcao_pessoal,
        "proporcao_produtos": proporcao_produtos,
        "proporcao_aluguel": proporcao_aluguel,
        "custo_fixo": custo_fixo,
        "custo_variavel": dados.despesa_produtos,
        "atendimentos_por_funcionario": atendimentos_por_funcionario,
        "atendimentos_potenciais_por_funcionario": atendimentos_potenciais_por_funcionario,
        "receita_por_funcionario": receita_por_funcionario,
        "receita_potencial_por_funcionario": receita_potencial_por_funcionario,
        "ponto_equilibrio_atendimentos": ponto_equilibrio_atendimentos,
        "crescimento_receita": crescimento_receita,
        "diferenca_meta": diferenca_meta,
    }


def analyze_petshop_data(dados):
    """Função principal para análise de dados do petshop"""
    # Calcular horas de operação
    horas_operacao = calculate_working_hours(dados)

    # Calcular métricas de capacidade
    capacidade = calculate_capacity_metrics(dados, horas_operacao)

    # Calcular métricas financeiras
    financeiro = calculate_financial_metrics(dados, capacidade)

    # Compilar resultados em um objeto AnalisysResult
    resultado = AnalisysResult(
        faturamento_atual=dados.faturamento_mensal,
        faturamento_potencial=financeiro["faturamento_potencial"],
        faturamento_nao_realizado=financeiro["faturamento_nao_realizado"],
        percentual_capacidade_utilizada=capacidade["percentual_capacidade"],
        projecao_anual_atual=dados.faturamento_mensal * 12,
        projecao_anual_potencial=financeiro["faturamento_potencial"] * 12,
        capacidade_diaria_ideal=capacidade["capacidade_diaria_ideal"],
        capacidade_mensal_ideal=capacidade["capacidade_mensal_ideal"],
        ocupacao_atual_percentual=capacidade["percentual_capacidade"],
        tempo_ocioso_diario=capacidade["tempo_ocioso_diario"],
        despesa_total=financeiro["despesa_total"],
        despesa_pessoal=financeiro["despesa_pessoal"],
        lucro_atual=financeiro["lucro_atual"],
        lucro_potencial=financeiro["lucro_potencial"],
        margem_lucro=financeiro["margem_lucro"],
        atendimentos_por_funcionario=financeiro["atendimentos_por_funcionario"],
        atendimentos_potenciais_por_funcionario=financeiro[
            "atendimentos_potenciais_por_funcionario"
        ],
        receita_por_funcionario=financeiro["receita_por_funcionario"],
        receita_potencial_por_funcionario=financeiro[
            "receita_potencial_por_funcionario"
        ],
        proporcao_pessoal=financeiro["proporcao_pessoal"],
        proporcao_produtos=financeiro["proporcao_produtos"],
        proporcao_aluguel=financeiro["proporcao_aluguel"],
        custo_fixo=financeiro["custo_fixo"],
        custo_variavel=financeiro["custo_variavel"],
        ponto_equilibrio_atendimentos=financeiro["ponto_equilibrio_atendimentos"],
        crescimento_receita=financeiro["crescimento_receita"],
        diferenca_meta=financeiro["diferenca_meta"],
    )

    return resultado


def create_data_visualizations(dados, resultado):
    """Cria gráficos para visualizar diferentes aspectos dos resultados"""
    # Configurar estilo
    plt.style.use("ggplot")
    plt.rcParams.update({"font.size": 12})

    # 1. Faturamento Atual vs Potencial
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    labels = ["Atual", "Potencial"]
    valores = [resultado.faturamento_atual, resultado.faturamento_potencial]
    cores = [COLORS["primaria"], COLORS["secundaria"]]

    barras = ax1.bar(labels, valores, color=cores)
    ax1.set_title("Faturamento Mensal (R$)")
    ax1.set_ylabel("Valor (R$)")

    # Formatar eixo Y para valores monetários
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f"R$ {x/1000:.0f}k"))

    # Adicionar rótulos nas barras
    for i, barra in enumerate(barras):
        altura = barra.get_height()
        ax1.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura + 0.05 * max(valores),
            f"R$ {altura:,.2f}".replace(",", "."),
            ha="center",
            va="bottom",
            rotation=0,
            fontsize=10,
        )

    # 2. Gráfico de ocupação (pizza/rosca)
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    ocupacao = resultado.ocupacao_atual_percentual
    livre = 100 - ocupacao

    ax2.pie(
        [ocupacao, livre],
        labels=["Utilizada", "Não utilizada"],
        autopct="%1.1f%%",
        startangle=90,
        colors=[COLORS["primaria"], COLORS["neutra"]],
        wedgeprops=dict(width=0.3),
    )
    ax2.set_title("Taxa de Ocupação")
    ax2.axis("equal")

    # 3. Margem de Lucro Atual vs Padrão do Setor
    fig3, ax3 = plt.subplots(figsize=(10, 6))

    margem_atual = resultado.margem_lucro
    margem_min, margem_max = INDUSTRY_STANDARD["margem_lucro"]

    x = ["Atual", "Mínimo Setor", "Máximo Setor"]
    y = [margem_atual, margem_min, margem_max]

    cores_barras = [
        (
            COLORS["destaque"]
            if margem_atual < margem_min
            else (
                COLORS["secundaria"]
                if margem_atual > margem_max
                else COLORS["primaria"]
            )
        ),
        COLORS["neutra"],
        COLORS["neutra"],
    ]

    barras = ax3.bar(x, y, color=cores_barras)
    ax3.set_title("Margem de Lucro (%)")
    ax3.set_ylabel("Porcentagem (%)")

    # Adicionar rótulos nas barras
    for i, barra in enumerate(barras):
        altura = barra.get_height()
        ax3.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura + 0.5,
            f"{altura:.1f}%",
            ha="center",
            va="bottom",
        )

    # 4. Estrutura de Custos (gráfico de pizza)
    fig4, ax4 = plt.subplots(figsize=(8, 8))

    # Calcular componentes de custo
    custo_pessoal = resultado.despesa_pessoal
    custo_produtos = resultado.custo_variavel
    custo_outros = resultado.despesa_total - custo_pessoal - custo_produtos

    custos = [custo_pessoal, custo_produtos, custo_outros]
    labels = ["Pessoal", "Produtos", "Outros"]

    # Calcular percentuais
    total = sum(custos)
    percentuais = [(c / total) * 100 for c in custos]

    # Criar gráfico
    wedges, texts, autotexts = ax4.pie(
        custos,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=[COLORS["primaria"], COLORS["secundaria"], COLORS["neutra"]],
    )
    ax4.set_title("Estrutura de Custos")
    ax4.axis("equal")

    return [fig1, fig2, fig3, fig4]


def prepare_financial_report(dados, resultado):
    """Gera um relatório financeiro com recomendações personalizadas"""
    # Exemplo de relatório - em um cenário real, isso poderia ser gerado através de uma API de IA
    relatorio = {
        "saude_financeira": f"""
O **{dados.nome_petshop}** apresenta uma saúde financeira que requer atenção. 
Com faturamento mensal de {format_currency(dados.faturamento_mensal)} e lucratividade de {format_percent(resultado.margem_lucro)}, 
o negócio está {'abaixo' if resultado.margem_lucro < INDUSTRY_STANDARD['margem_lucro'][0] else 'dentro'} da média do setor que fica entre 
{INDUSTRY_STANDARD['margem_lucro'][0]}% e {INDUSTRY_STANDARD['margem_lucro'][1]}%. 

A taxa de ocupação de {format_percent(resultado.ocupacao_atual_percentual)} indica uma 
{'subutilização significativa dos recursos' if resultado.ocupacao_atual_percentual < 70 else 'utilização adequada da capacidade'},
resultando em {'perda' if resultado.faturamento_nao_realizado > 0 else 'otimização'} potencial de 
{format_currency(resultado.faturamento_nao_realizado)} mensais ou {format_currency(resultado.faturamento_nao_realizado * 12)} anuais.
        """,
        "ineficiencias": [
            {
                "titulo": "Subutilização da Capacidade",
                "descricao": f"O petshop opera a apenas {format_percent(resultado.ocupacao_atual_percentual)} da capacidade ideal, deixando de realizar {resultado.capacidade_mensal_ideal - dados.numero_atendimentos_mes} atendimentos mensais.",
            },
            {
                "titulo": "Proporção de Custos com Pessoal",
                "descricao": f"A proporção de despesas com pessoal é de {format_percent(resultado.proporcao_pessoal)}, {'acima' if resultado.proporcao_pessoal > INDUSTRY_STANDARD['proporcao_pessoal'][1] else 'abaixo' if resultado.proporcao_pessoal < INDUSTRY_STANDARD['proporcao_pessoal'][0] else 'dentro'} da média do setor.",
            },
            {
                "titulo": "Tempo Ocioso",
                "descricao": f"São perdidas aproximadamente {resultado.tempo_ocioso_diario:.1f} horas diárias de mão de obra, o que representa um custo de ociosidade de aproximadamente {format_currency(resultado.tempo_ocioso_diario * (resultado.despesa_pessoal / 22 / 8))} por dia.",
            },
        ],
        "recomendacoes": [
            {
                "titulo": "Implementar Estratégia de Marketing Direcionada",
                "descricao": "Desenvolva promoções para dias e horários de baixa demanda. Implemente um programa de fidelidade para aumentar a recorrência de clientes.",
                "impacto": f"Aumento potencial de 15-20% no número de atendimentos, gerando aproximadamente {format_currency(dados.faturamento_mensal * 0.15)} adicionais por mês.",
                "prazo": "3 meses",
            },
            {
                "titulo": "Otimizar Estrutura de Custos",
                "descricao": "Renegocie contratos com fornecedores de produtos para banho e tosa. Implemente controle de estoque mais rigoroso para reduzir desperdícios.",
                "impacto": f"Redução de 10-15% nos custos variáveis, economia de aproximadamente {format_currency(resultado.custo_variavel * 0.12)} mensais.",
                "prazo": "2 meses",
            },
            {
                "titulo": "Aumentar Ticket Médio",
                "descricao": "Ofereça serviços complementares de maior valor agregado. Treine a equipe para realizar venda cruzada de produtos e serviços.",
                "impacto": f"Aumento de 10-20% no ticket médio, gerando receita adicional de {format_currency(dados.faturamento_mensal * 0.15)} mensais.",
                "prazo": "3 meses",
            },
        ],
        "prioridades": [
            {
                "titulo": "Análise de Horários de Pico",
                "descricao": "Identifique os horários e dias com menor ocupação e crie promoções específicas para esses períodos.",
            },
            {
                "titulo": "Revisão de Preços e Serviços",
                "descricao": "Ajuste a tabela de preços de acordo com a demanda e posicionamento de mercado. Crie pacotes de serviços para aumentar o ticket médio.",
            },
            {
                "titulo": "Campanha de Reativação",
                "descricao": "Entre em contato com clientes inativos oferecendo condições especiais para retorno.",
            },
        ],
        "metas": [
            {
                "titulo": "Aumento da Taxa de Ocupação",
                "descricao": f"Elevar a taxa de ocupação atual de {format_percent(resultado.ocupacao_atual_percentual)} para pelo menos 75% em 3 meses.",
            },
            {
                "titulo": "Melhoria da Margem de Lucro",
                "descricao": f"Aumentar a margem de lucro de {format_percent(resultado.margem_lucro)} para {format_percent(min(resultado.margem_lucro + 5, 25))} em 3 meses.",
            },
            {
                "titulo": "Redução de Custos Variáveis",
                "descricao": f"Reduzir a proporção de custos com produtos de {format_percent(resultado.proporcao_produtos)} para {format_percent(max(resultado.proporcao_produtos - 5, 15))} em 2 meses.",
            },
        ],
    }

    return relatorio


def show_results(dados, resultado):
    """Exibe os resultados da análise do petshop"""
    st.markdown(
        "<h1 class='main-header'>Análise Financeira</h1>", unsafe_allow_html=True
    )
    st.markdown(
        f"<h2 class='sub-header'>{dados.nome_petshop}</h2>", unsafe_allow_html=True
    )

    # Principais métricas
    st.markdown(
        "<div class='section-header'>Métricas Principais</div>", unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    # Coluna 1 - Faturamento
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
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
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
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
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
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
    st.markdown(
        "<div class='section-header'>Potencial Não Aproveitado</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='highlight-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>Dinheiro Deixado na Mesa</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<h2 style='color: #e74c3c;'>{format_currency(resultado.faturamento_nao_realizado * 12)}/ano</h2>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown("<h3>Capacidade Não Utilizada</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<h2 style='color: #e74c3c;'>{resultado.capacidade_mensal_ideal - dados.numero_atendimentos_mes} atendimentos/mês</h2>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Visualizações
    st.markdown(
        "<div class='section-header'>Visualizações</div>", unsafe_allow_html=True
    )

    # Criar gráficos
    figuras = create_data_visualizations(dados, resultado)

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

    # Relatório com recomendações
    st.markdown(
        "<div class='section-header'>Análise e Recomendações</div>",
        unsafe_allow_html=True,
    )

    relatorio = prepare_financial_report(dados, resultado)

    # Saúde Financeira
    st.markdown("### Saúde Financeira Atual")
    st.markdown(relatorio["saude_financeira"])

    # Ineficiências
    st.markdown("### Principais Ineficiências")
    for i, ineficiencia in enumerate(relatorio["ineficiencias"]):
        st.markdown(f"**{i+1}. {ineficiencia['titulo']}**")
        st.markdown(ineficiencia["descricao"])

    # Recomendações
    st.markdown("### Recomendações Práticas")
    for i, recomendacao in enumerate(relatorio["recomendacoes"]):
        st.markdown(f"**{i+1}. {recomendacao['titulo']}**")
        st.markdown(recomendacao["descricao"])
        st.markdown(f"**Impacto estimado:** {recomendacao['impacto']}")
        st.markdown(f"**Prazo sugerido:** {recomendacao['prazo']}")

    # Prioridades
    st.markdown("### Prioridades de Curto Prazo")
    for i, prioridade in enumerate(relatorio["prioridades"]):
        st.markdown(f"**{i+1}. {prioridade['titulo']}**")
        st.markdown(prioridade["descricao"])

    # Metas
    st.markdown("### Metas Sugeridas")
    for i, meta in enumerate(relatorio["metas"]):
        st.markdown(f"**{i+1}. {meta['titulo']}**")
        st.markdown(meta["descricao"])

    # Exportar resultados
    st.markdown(
        "<div class='section-header'>Exportar Resultados</div>", unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Exportar para CSV"):
            # Criar dados para CSV
            data = {
                # Dados básicos
                "Nome Petshop": dados.nome_petshop,
                "Data Análise": datetime.now().strftime("%d/%m/%Y"),
                # Dados operacionais
                "Funcionários Total": dados.numero_funcionarios,
                "Funcionários Banho/Tosa": dados.funcionarios_banho_tosa,
                "Atendimentos Mensais": dados.numero_atendimentos_mes,
                "Ticket Médio": dados.ticket_medio,
                # Dados financeiros
                "Faturamento Atual": resultado.faturamento_atual,
                "Faturamento Potencial": resultado.faturamento_potencial,
                "Faturamento Não Realizado": resultado.faturamento_nao_realizado,
                "Lucro Atual": resultado.lucro_atual,
                "Margem Lucro": resultado.margem_lucro,
                # Métricas de eficiência
                "Taxa Ocupação": resultado.ocupacao_atual_percentual,
                "Capacidade Mensal": resultado.capacidade_mensal_ideal,
                "Atendimentos por Funcionário": resultado.atendimentos_por_funcionario,
                # Calculadora de potencial anual
                "Potencial Anual Não Realizado": resultado.faturamento_nao_realizado
                * 12,
            }

            # Criar DataFrame
            df = pd.DataFrame([data])

            # Converter para CSV
            csv = df.to_csv(index=False)

            # Criar download
            st.download_button(
                label="Baixar arquivo CSV",
                data=csv,
                file_name=f"analise_{dados.nome_petshop.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )

    with col2:
        if st.button("Gerar PDF (em breve)"):
            st.info("Funcionalidade em desenvolvimento. Estará disponível em breve!")

    # Formulário de contato
    st.markdown(
        "<div class='section-header'>Quer melhorar os resultados do seu petshop?</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
        <h3>Agende uma consultoria com especialistas</h3>
        <p>Nossa equipe de consultores pode ajudar a implementar as recomendações e melhorar os resultados do seu negócio.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nome", placeholder="Seu nome", key="contato_nome")
        st.text_input("Email", placeholder="Seu email", key="contato_email")
    with col2:
        st.text_input("Telefone", placeholder="Seu telefone", key="contato_telefone")
        st.text_area(
            "Mensagem",
            placeholder="Digite sua mensagem",
            height=100,
            key="contato_mensagem",
        )

    if st.button("Enviar mensagem", type="primary"):
        st.success("Mensagem enviada com sucesso! Entraremos em contato em breve.")

    # Reiniciar análise
    if st.button("Iniciar Nova Análise"):
        st.session_state.current_page = "form"
        st.rerun()


def create_input_form():
    """Cria o formulário para coleta de dados do petshop"""
    st.markdown("<h1 class='main-header'>Dog's Club</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h2 class='sub-header'>Análise Financeira de Petshop</h2>",
        unsafe_allow_html=True,
    )

    # Criar um formulário com abas
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["Informações Básicas", "Operação", "Equipe", "Serviços", "Financeiro", "Metas"]
    )

    # Tab 1: Informações Básicas
    with tab1:
        st.subheader("Informações Básicas")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nome do Petshop", value="Petshop Feliz", key="nome_petshop")
            st.text_input(
                "Email de Contato",
                value="contato@petshopfeliz.com.br",
                key="email_contato",
            )
        with col2:
            st.text_input("Telefone", value="(11) 93355-7283", key="telefone_contato")

    # Tab 2: Operação
    with tab2:
        st.subheader("Operação")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Horário de Abertura", value="08:00", key="horario_abertura")
            st.text_input(
                "Horário de Fechamento", value="18:00", key="horario_fechamento"
            )
        with col2:
            st.slider(
                "Dias de Funcionamento por Semana",
                min_value=1,
                max_value=7,
                value=6,
                key="dias_funcionamento_semana",
            )

    # Tab 3: Equipe
    with tab3:
        st.subheader("Equipe")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Total de Funcionários", min_value=1, value=3, key="numero_funcionarios"
            )
        with col2:
            st.number_input(
                "Funcionários de Banho/Tosa",
                min_value=1,
                value=2,
                key="funcionarios_banho_tosa",
            )
        st.number_input(
            "Salário Médio (R$)",
            min_value=500.0,
            value=1800.0,
            step=100.0,
            key="salario_medio",
        )

    # Tab 4: Serviços
    with tab4:
        st.subheader("Serviços")
        col1, col2 = st.columns(2)
        with col1:
            st.slider(
                "Tempo Médio Banho/Tosa (min)",
                min_value=30,
                max_value=180,
                value=90,
                key="tempo_medio_banho_tosa",
            )
        with col2:
            st.number_input(
                "Atendimentos por Mês",
                min_value=1,
                value=200,
                key="numero_atendimentos_mes",
            )
        st.number_input(
            "Ticket Médio (R$)",
            min_value=10.0,
            value=90.0,
            step=5.0,
            key="ticket_medio",
        )

    # Tab 5: Financeiro
    with tab5:
        st.subheader("Financeiro")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "Faturamento Mensal (R$)",
                min_value=0.0,
                value=18000.0,
                step=1000.0,
                key="faturamento_mensal",
            )
            st.number_input(
                "Faturamento Mês Anterior (R$)",
                min_value=0.0,
                value=17000.0,
                step=1000.0,
                key="faturamento_mes_anterior",
            )
        with col2:
            st.number_input(
                "Despesa Água/Luz (R$)",
                min_value=0.0,
                value=800.0,
                step=100.0,
                key="despesa_agua_luz",
            )
            st.number_input(
                "Despesa Produtos (R$)",
                min_value=0.0,
                value=3600.0,
                step=100.0,
                key="despesa_produtos",
            )
        col3, col4 = st.columns(2)
        with col3:
            st.number_input(
                "Despesa Aluguel (R$)",
                min_value=0.0,
                value=2500.0,
                step=100.0,
                key="despesa_aluguel",
            )
        with col4:
            st.number_input(
                "Outras Despesas (R$)",
                min_value=0.0,
                value=1000.0,
                step=100.0,
                key="despesa_outros",
            )

    # Tab 6: Metas
    with tab6:
        st.subheader("Metas e Desafios")
        st.number_input(
            "Meta de Lucro Mensal (R$)",
            min_value=0.0,
            value=6000.0,
            step=1000.0,
            key="meta_lucro",
        )
        st.text_area(
            "Principal Desafio",
            value="Aumentar o número de clientes e melhorar a rentabilidade.",
            key="principal_desafio",
        )

    # Botão de análise
    if st.button("Analisar Dados", type="primary"):
        with st.spinner("Analisando dados do petshop..."):
            # Extrair dados do formulário
            dados = extract_form_data()

            if dados:
                # Realizar análise
                resultado = analyze_petshop_data(dados)

                # Armazenar resultado na sessão
                st.session_state.petshop_data = dados
                st.session_state.analysis_result = resultado
                st.session_state.current_page = "results"

                # Recarregar a página para mostrar os resultados
                st.rerun()


def main():
    """Função principal que orquestra a aplicação"""
    # Configuração inicial do estado da sessão
    if "current_page" not in st.session_state:
        st.session_state.current_page = "form"

    # Criar a barra lateral
    create_sidebar()

    # Renderizar a página apropriada
    if st.session_state.current_page == "form":
        create_input_form()
    elif st.session_state.current_page == "results":
        if "petshop_data" in st.session_state and "analysis_result" in st.session_state:
            show_results(
                st.session_state.petshop_data, st.session_state.analysis_result
            )
        else:
            st.error(
                "Não há resultados disponíveis. Por favor, faça a análise primeiro."
            )
            st.session_state.current_page = "form"
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


# Executar a aplicação
if __name__ == "__main__":
    main()
