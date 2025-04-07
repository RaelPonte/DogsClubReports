import logging

# Configurar logging
logger = logging.getLogger(__name__)


def calculate_financial_metrics(dados, capacidade):
    """Calcula métricas financeiras"""
    # Log dos dados recebidos
    logger.info(f"Calculando métricas financeiras para: {dados}")
    logger.info(f"Capacidade calculada: {capacidade}")

    # Verificar faturamento mensal
    if dados.faturamento_mensal <= 0:
        logger.warning("Faturamento mensal zerado ou negativo. Usando valor padrão.")
        faturamento_mensal = 18000.0
    else:
        faturamento_mensal = dados.faturamento_mensal

    # Despesas com pessoal
    despesa_pessoal = dados.salario_medio * dados.numero_funcionarios
    logger.info(f"Despesa com pessoal calculada: {despesa_pessoal}")

    # Despesas totais
    despesa_total = (
        despesa_pessoal
        + dados.despesa_agua_luz
        + dados.despesa_produtos
        + (dados.despesa_aluguel or 0)
        + (dados.despesa_outros or 0)
    )
    logger.info(f"Despesa total calculada: {despesa_total}")

    # Faturamento potencial mensal
    ticket_medio = dados.ticket_medio if dados.ticket_medio > 0 else 90.0
    if capacidade["capacidade_mensal_ideal"] <= 0:
        logger.warning("Capacidade mensal ideal zerada. Usando valor mínimo.")
        capacidade_mensal_ideal = 200  # Valor padrão se a capacidade for zero
    else:
        capacidade_mensal_ideal = capacidade["capacidade_mensal_ideal"]

    faturamento_potencial = capacidade_mensal_ideal * ticket_medio
    logger.info(f"Faturamento potencial calculado: {faturamento_potencial}")

    # Faturamento não realizado (potencial perdido)
    faturamento_nao_realizado = max(0, faturamento_potencial - faturamento_mensal)
    logger.info(f"Faturamento não realizado calculado: {faturamento_nao_realizado}")

    # Lucratividade
    lucro_atual = faturamento_mensal - despesa_total
    logger.info(f"Lucro atual calculado: {lucro_atual}")

    if faturamento_mensal > 0:
        margem_lucro = lucro_atual / faturamento_mensal * 100
    else:
        margem_lucro = 0
        logger.warning("Faturamento zerado ao calcular margem de lucro.")

    logger.info(f"Margem de lucro calculada: {margem_lucro}%")

    # Lucro potencial
    if dados.custo_produto_percentual and dados.custo_produto_percentual > 0:
        custo_produto_percentual = dados.custo_produto_percentual
    else:
        # Valor padrão se não informado ou zerado
        custo_produto_percentual = 20
        logger.warning(
            f"Percentual de custo de produto não válido, usando padrão: {custo_produto_percentual}%"
        )

    custo_produto_potencial = faturamento_potencial * (custo_produto_percentual / 100)

    # Simplificação - considerando produtos como único custo variável
    custo_fixo = despesa_total - dados.despesa_produtos
    lucro_potencial = faturamento_potencial - custo_produto_potencial - custo_fixo
    logger.info(f"Lucro potencial calculado: {lucro_potencial}")

    # Estrutura de Custos
    if despesa_total > 0:
        proporcao_pessoal = despesa_pessoal / despesa_total * 100
        proporcao_produtos = dados.despesa_produtos / despesa_total * 100
        proporcao_aluguel = (dados.despesa_aluguel or 0) / despesa_total * 100
    else:
        proporcao_pessoal = 60  # Valores padrão
        proporcao_produtos = 20
        proporcao_aluguel = 15
        logger.warning(
            "Despesa total zerada ao calcular proporções. Usando valores padrão."
        )

    # Eficiência por funcionário
    if dados.funcionarios_banho_tosa > 0:
        atendimentos_por_funcionario = (
            dados.numero_atendimentos_mes / dados.funcionarios_banho_tosa
        )
        atendimentos_potenciais_por_funcionario = (
            capacidade_mensal_ideal / dados.funcionarios_banho_tosa
        )
        receita_por_funcionario = faturamento_mensal / dados.funcionarios_banho_tosa
        receita_potencial_por_funcionario = (
            faturamento_potencial / dados.funcionarios_banho_tosa
        )
    else:
        atendimentos_por_funcionario = 0
        atendimentos_potenciais_por_funcionario = 0
        receita_por_funcionario = 0
        receita_potencial_por_funcionario = 0
        logger.warning(
            "Número de funcionários de banho/tosa zerado ao calcular eficiência."
        )

    # Ponto de equilíbrio
    margem_contribuicao_percentual = 100 - custo_produto_percentual
    margem_contribuicao_unitaria = ticket_medio * (margem_contribuicao_percentual / 100)

    if margem_contribuicao_unitaria > 0:
        ponto_equilibrio_atendimentos = int(custo_fixo / margem_contribuicao_unitaria)
    else:
        ponto_equilibrio_atendimentos = 0
        logger.warning(
            "Margem de contribuição unitária zerada ao calcular ponto de equilíbrio."
        )

    # Crescimento
    if dados.faturamento_mes_anterior and dados.faturamento_mes_anterior > 0:
        crescimento_receita = (
            (faturamento_mensal - dados.faturamento_mes_anterior)
            / dados.faturamento_mes_anterior
            * 100
        )
    else:
        crescimento_receita = None
        logger.info(
            "Faturamento do mês anterior não informado ou zerado. Crescimento não calculado."
        )

    # Verificação de meta
    if dados.meta_lucro is not None:
        diferenca_meta = lucro_atual - dados.meta_lucro
    else:
        diferenca_meta = None

    # Log do resultado final
    logger.info("Métricas financeiras calculadas com sucesso")

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
