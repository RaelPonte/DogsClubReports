import logging

# Configurar logging
logger = logging.getLogger(__name__)


def calculate_capacity_metrics(dados, horas_operacao):
    """Calcula métricas de capacidade e ocupação"""
    logger.info(f"Calculando métricas de capacidade com: {dados}")
    logger.info(f"Horas de operação: {horas_operacao}")

    # Verificar valores importantes
    tempo_medio_banho_tosa = max(
        30, dados.tempo_medio_banho_tosa
    )  # Mínimo de 30 minutos
    funcionarios_banho_tosa = max(
        1, dados.funcionarios_banho_tosa
    )  # Mínimo de 1 funcionário

    # Calcular capacidade diária ideal por funcionário
    # Assumindo que cada funcionário de banho e tosa trabalha 85% do seu tempo em atendimentos
    eficiencia_trabalho = 0.85  # 85% do tempo é produtivo

    # Calcular horas diárias com proteção contra valores zerados
    horas_diarias = max(
        1, horas_operacao.get("diaria", 8)
    )  # Padrão de 8 horas se não for informado

    capacidade_funcionario = (
        horas_diarias * 60 * eficiencia_trabalho
    ) / tempo_medio_banho_tosa  # animais/dia

    logger.info(
        f"Capacidade por funcionário: {capacidade_funcionario} atendimentos/dia"
    )

    # Capacidade diária total da equipe de banho e tosa
    capacidade_diaria_ideal = int(capacidade_funcionario * funcionarios_banho_tosa)
    logger.info(f"Capacidade diária ideal: {capacidade_diaria_ideal} atendimentos/dia")

    # Capacidade mensal ideal
    dias_uteis = max(1, horas_operacao.get("dias_uteis", 22))  # Padrão de 22 dias úteis
    capacidade_mensal_ideal = int(capacidade_diaria_ideal * dias_uteis)
    logger.info(f"Capacidade mensal ideal: {capacidade_mensal_ideal} atendimentos/mês")

    # Certificar-se de que o número de atendimentos mensais seja válido
    numero_atendimentos_mes = max(0, dados.numero_atendimentos_mes)

    # Percentual da capacidade utilizada
    if capacidade_mensal_ideal > 0:
        percentual_capacidade = numero_atendimentos_mes / capacidade_mensal_ideal * 100
    else:
        percentual_capacidade = 0
        logger.warning(
            "Capacidade mensal ideal zerada. Percentual de capacidade não calculado."
        )

    logger.info(f"Percentual da capacidade utilizada: {percentual_capacidade}%")

    # Tempo ocioso diário em horas
    if dias_uteis > 0:
        atendimentos_diarios_atuais = numero_atendimentos_mes / dias_uteis
    else:
        atendimentos_diarios_atuais = 0
        logger.warning("Dias úteis zerados. Atendimentos diários não calculados.")

    if dados.tempo_medio_banho_tosa > 0:
        horas_produtivas_diarias = (
            atendimentos_diarios_atuais * tempo_medio_banho_tosa
        ) / 60
    else:
        horas_produtivas_diarias = 0
        logger.warning(
            "Tempo médio de banho/tosa zerado. Horas produtivas não calculadas."
        )

    horas_potenciais_diarias = (
        horas_diarias * funcionarios_banho_tosa * eficiencia_trabalho
    )

    tempo_ocioso_diario = max(0, horas_potenciais_diarias - horas_produtivas_diarias)
    logger.info(f"Tempo ocioso diário: {tempo_ocioso_diario} horas")

    return {
        "capacidade_diaria_ideal": capacidade_diaria_ideal,
        "capacidade_mensal_ideal": capacidade_mensal_ideal,
        "percentual_capacidade": percentual_capacidade,
        "tempo_ocioso_diario": tempo_ocioso_diario,
    }
