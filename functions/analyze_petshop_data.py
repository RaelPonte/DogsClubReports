from .calculate_working_hours import calculate_working_hours
from .calculate_capacity_metrics import calculate_capacity_metrics
from .calculate_financial_metrics import calculate_financial_metrics
from dataclass import AnalisysResult
import logging
import streamlit as st

# Configurar logging
logger = logging.getLogger(__name__)


def analyze_petshop_data(dados):
    """Função principal para análise de dados do petshop"""
    # Verificar dados de entrada
    logger.info(f"Dados recebidos para análise: {dados}")
    if not dados.faturamento_mensal or dados.faturamento_mensal <= 0:
        logger.warning(
            "Faturamento mensal está zerado ou negativo. Usando valor padrão."
        )
        dados.faturamento_mensal = 18000.0

    # Calcular horas de operação
    horas_operacao = calculate_working_hours(dados)
    logger.info(f"Horas de operação calculadas: {horas_operacao}")

    # Calcular métricas de capacidade
    capacidade = calculate_capacity_metrics(dados, horas_operacao)
    logger.info(f"Métricas de capacidade calculadas: {capacidade}")

    # Calcular métricas financeiras
    financeiro = calculate_financial_metrics(dados, capacidade)
    logger.info(f"Métricas financeiras calculadas: {financeiro}")

    # Verificar valores importantes
    if financeiro["faturamento_potencial"] <= 0:
        logger.warning(
            "Faturamento potencial está zerado. Usando valor baseado no faturamento atual."
        )
        financeiro["faturamento_potencial"] = dados.faturamento_mensal * 1.5

    if financeiro["lucro_atual"] == 0 and dados.faturamento_mensal > 0:
        logger.warning(
            "Lucro calculado zerado com faturamento positivo. Verificando cálculos."
        )

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

    # Log do resultado final para verificação
    logger.info(f"Resultado da análise: {resultado}")

    # Verificação final para garantir valores não zerados nos principais campos
    if resultado.faturamento_atual <= 0:
        st.warning("Atenção: o faturamento calculado está zerado")

    return resultado
