import streamlit as st
from dataclass import PetshopData
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_form_data():
    """Extrai os dados dos formulários e cria um objeto PetshopData"""
    dados = {}

    # Informações básicas
    # Nome do usuário
    dados["nome"] = st.session_state.get("nome", "")
    if not dados["nome"] or dados["nome"].strip() == "":
        dados["nome"] = st.session_state.get("nome_salvo", "")

    # Nome do petshop
    dados["nome_petshop"] = st.session_state.get("nome_petshop", "")
    if not dados["nome_petshop"] or dados["nome_petshop"].strip() == "":
        dados["nome_petshop"] = st.session_state.get("nome_petshop_salvo", "")

    # Email
    dados["email_contato"] = st.session_state.get("email_contato", "")
    if not dados["email_contato"] or dados["email_contato"].strip() == "":
        dados["email_contato"] = st.session_state.get("email_salvo", "")

    # WhatsApp
    dados["whatsapp_contato"] = st.session_state.get("whatsapp_contato", "")
    if not dados["whatsapp_contato"] or dados["whatsapp_contato"].strip() == "":
        dados["whatsapp_contato"] = st.session_state.get("whatsapp_salvo", "")

    # Telefone
    dados["telefone_contato"] = st.session_state.get("telefone_contato", "")
    if not dados["telefone_contato"] or dados["telefone_contato"].strip() == "":
        dados["telefone_contato"] = st.session_state.get("telefone_salvo", "")

    # Operação
    dados["horario_abertura"] = st.session_state.get("horario_abertura", "08:00")
    dados["horario_fechamento"] = st.session_state.get("horario_fechamento", "18:00")
    dados["dias_funcionamento_semana"] = st.session_state.get(
        "dias_funcionamento_semana", 6
    )

    # Equipe
    dados["numero_funcionarios"] = st.session_state.get("numero_funcionarios", 3)
    dados["funcionarios_banho_tosa"] = st.session_state.get(
        "funcionarios_banho_tosa", 2
    )
    dados["salario_medio"] = st.session_state.get("salario_medio", 1800.0)

    # Serviços
    dados["tempo_medio_banho_tosa"] = st.session_state.get("tempo_medio_banho_tosa", 90)
    dados["numero_atendimentos_mes"] = st.session_state.get(
        "numero_atendimentos_mes", 200
    )
    dados["ticket_medio"] = st.session_state.get("ticket_medio", 90.0)

    # Financeiro
    dados["faturamento_mensal"] = st.session_state.get("faturamento_mensal", 18000.0)
    dados["faturamento_mes_anterior"] = st.session_state.get(
        "faturamento_mes_anterior", 17000.0
    )
    dados["despesa_agua_luz"] = st.session_state.get("despesa_agua_luz", 800.0)
    dados["despesa_produtos"] = st.session_state.get("despesa_produtos", 3600.0)
    dados["despesa_aluguel"] = st.session_state.get("despesa_aluguel", 2500.0)
    dados["despesa_outros"] = st.session_state.get("despesa_outros", 1000.0)

    # Metas
    dados["meta_lucro"] = st.session_state.get("meta_lucro", 6000.0)
    dados["principal_desafio"] = st.session_state.get("principal_desafio")

    # Registrar valores importantes para depuração
    logger.info(f"Faturamento mensal: {dados['faturamento_mensal']}")
    logger.info(f"Ticket médio: {dados['ticket_medio']}")
    logger.info(f"Atendimentos por mês: {dados['numero_atendimentos_mes']}")

    # Calcular percentual de produtos sobre o faturamento
    if dados["faturamento_mensal"] > 0:
        dados["custo_produto_percentual"] = (
            dados["despesa_produtos"] / dados["faturamento_mensal"]
        ) * 100
    else:
        dados["custo_produto_percentual"] = 20  # Valor padrão se faturamento for zero

    # Calcular custo fixo total
    dados["custo_fixo_mensal"] = (
        dados["despesa_agua_luz"]
        + dados["despesa_aluguel"]
        + dados["despesa_outros"]
        + (dados["salario_medio"] * dados["numero_funcionarios"])
    )

    # Certificar que não há valores zerados importantes
    for key in ["faturamento_mensal", "ticket_medio", "numero_atendimentos_mes"]:
        if not dados[key]:
            logger.warning(f"Valor crítico está zerado: {key}")
            if key == "faturamento_mensal":
                dados[key] = 18000.0
            elif key == "ticket_medio":
                dados[key] = 90.0
            elif key == "numero_atendimentos_mes":
                dados[key] = 200

    try:
        petshop_data = PetshopData(**dados)
        logger.info(f"Objeto PetshopData criado com sucesso: {petshop_data}")
        return petshop_data
    except Exception as e:
        st.error(f"Erro ao validar os dados: {str(e)}")
        logger.error(f"Erro ao criar objeto PetshopData: {str(e)}")
        return None
