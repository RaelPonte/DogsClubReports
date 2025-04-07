from utils import format_currency, format_percent


def prepare_financial_report(dados, resultado):
    """Gera um relatório financeiro com recomendações personalizadas"""
    # Valores padrão do setor para comparação
    INDUSTRY_STANDARD = {
        "margem_lucro": (15, 25),  # Porcentagem
        "proporcao_pessoal": (40, 50),  # Porcentagem
        "ticket_medio": (80, 150),  # R$
        "faturamento_funcionario": (5000, 8000),  # R$
        "taxa_ocupacao": (70, 85),  # Porcentagem
    }

    # Exemplo de relatório - em um cenário real, isso poderia ser gerado através de uma API de IA
    relatorio = {
        "saude_financeira": f"""
O <b>{dados.nome_petshop}</b> apresenta uma saúde financeira que requer atenção. 
Com faturamento mensal de <b>{format_currency(dados.faturamento_mensal)}</b> e lucratividade de <b>{format_percent(resultado.margem_lucro)}</b>, 
o negócio está {'abaixo' if resultado.margem_lucro < INDUSTRY_STANDARD['margem_lucro'][0] else 'dentro'} da média do setor que fica entre 
{INDUSTRY_STANDARD['margem_lucro'][0]}% e {INDUSTRY_STANDARD['margem_lucro'][1]}%. 

A taxa de ocupação de {format_percent(resultado.ocupacao_atual_percentual)} indica uma 
{'subutilização significativa dos recursos' if resultado.ocupacao_atual_percentual < 70 else 'utilização adequada da capacidade'},
resultando em {'perda' if resultado.faturamento_nao_realizado > 0 else 'otimização'} potencial de 
<b>{format_currency(resultado.faturamento_nao_realizado).replace("R$", "R\$")}</b> mensais ou aproximadamente 
<b>{format_currency(resultado.faturamento_nao_realizado * 12).replace("R$", "R\$")}</b> anuais.""",
        "ineficiencias": [
            {
                "titulo": "Subutilização da Capacidade",
                "descricao": f"O petshop opera a apenas {format_percent(resultado.ocupacao_atual_percentual)} da capacidade ideal, deixando de realizar {resultado.capacidade_mensal_ideal - dados.numero_atendimentos_mes} atendimentos mensais.",
            },
            {
                "titulo": "Proporção de Custos com Pessoal",
                "descricao": f"A proporção de despesas com pessoal é de {format_percent(resultado.proporcao_pessoal if resultado.proporcao_pessoal is not None else 0)}, {'acima' if (resultado.proporcao_pessoal or 0) > INDUSTRY_STANDARD['proporcao_pessoal'][1] else 'abaixo' if (resultado.proporcao_pessoal or 0) < INDUSTRY_STANDARD['proporcao_pessoal'][0] else 'dentro'} da média do setor.",
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
                "impacto": f"Redução de 10-15% nos custos variáveis, economia de aproximadamente {format_currency(getattr(resultado, 'custo_variavel', dados.despesa_produtos) * 0.12)} mensais.",
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
                "descricao": f"Reduzir a proporção de custos com produtos de {format_percent(resultado.proporcao_produtos if resultado.proporcao_produtos is not None else 0)} para {format_percent(max((resultado.proporcao_produtos or 0) - 5, 15))} em 2 meses.",
            },
        ],
    }

    return relatorio
