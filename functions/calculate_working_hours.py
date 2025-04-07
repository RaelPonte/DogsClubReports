from datetime import datetime
import logging
import re

from assets import WORKING_DAYS_IN_THE_MONTH

# Configurar logging
logger = logging.getLogger(__name__)


def validar_formato_hora(hora_str):
    """Valida se a string está no formato HH:MM"""
    return bool(re.match(r"^\d{1,2}:\d{2}$", hora_str))


def calculate_working_hours(dados):
    """Calcula horas de trabalho diárias e mensais"""
    logger.info(f"Calculando horas de trabalho para: {dados}")

    formato = "%H:%M"

    # Validar formato das horas
    if not validar_formato_hora(dados.horario_abertura):
        logger.warning(
            f"Formato de horário de abertura inválido: {dados.horario_abertura}. Usando padrão 08:00."
        )
        hora_abertura_str = "08:00"
    else:
        hora_abertura_str = dados.horario_abertura

    if not validar_formato_hora(dados.horario_fechamento):
        logger.warning(
            f"Formato de horário de fechamento inválido: {dados.horario_fechamento}. Usando padrão 18:00."
        )
        hora_fechamento_str = "18:00"
    else:
        hora_fechamento_str = dados.horario_fechamento

    try:
        hora_abertura = datetime.strptime(hora_abertura_str, formato)
        hora_fechamento = datetime.strptime(hora_fechamento_str, formato)

        # Ajuste para horários que passam da meia-noite
        if hora_fechamento < hora_abertura:
            logger.warning(
                "Horário de fechamento anterior ao de abertura. Ajustando para 23:59."
            )
            hora_fechamento = datetime.strptime("23:59", formato)

        horas_operacao_diaria = (hora_fechamento - hora_abertura).total_seconds() / 3600

        # Garantir valor mínimo para horas de operação
        if horas_operacao_diaria < 1:
            logger.warning(
                "Horas de operação diária muito baixas. Ajustando para mínimo de 6 horas."
            )
            horas_operacao_diaria = 6

        # Verificar valores de dias de funcionamento
        dias_funcionamento_semana = max(1, min(7, dados.dias_funcionamento_semana or 5))
        dias_uteis = WORKING_DAYS_IN_THE_MONTH * (
            dias_funcionamento_semana / 5
        )  # Ajuste baseado nos dias de funcionamento

        # Garantir no mínimo 20 dias úteis
        dias_uteis = max(20, dias_uteis)

        horas_operacao_mensal = horas_operacao_diaria * dias_uteis

        logger.info(f"Horas de operação diária: {horas_operacao_diaria}")
        logger.info(f"Dias úteis por mês: {dias_uteis}")
        logger.info(f"Horas de operação mensal: {horas_operacao_mensal}")

        return {
            "diaria": horas_operacao_diaria,
            "mensal": horas_operacao_mensal,
            "dias_uteis": dias_uteis,
        }
    except Exception as e:
        logger.error(f"Erro ao calcular horas de trabalho: {str(e)}")
        # Valores padrão caso ocorra algum erro
        return {
            "diaria": 8,  # 8 horas por dia
            "mensal": 176,  # 22 dias x 8 horas
            "dias_uteis": 22,  # 22 dias úteis por mês
        }
