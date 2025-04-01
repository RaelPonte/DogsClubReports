prompt = """
Você é um consultor financeiro especializado em petshops e pequenos negócios no Brasil.
Analise a saúde financeira deste petshop e forneça recomendações específicas e práticas.

### DADOS DO PETSHOP ###
Nome: {nome_petshop}
Faturamento mensal: {faturamento_mensal:.2f}
Faturamento mês anterior: {faturamento_mes_anterior:.2f}
Horário de funcionamento: {horario_abertura} às {horario_fechamento}, {dias_funcionamento_semana} dias por semana
Número de funcionários: {numero_funcionarios}
Funcionários de banho e tosa: {funcionarios_banho_tosa}
Salário médio: {salario_medio:.2f}

### DESPESAS MENSAIS ###
Água e luz: {despesa_agua_luz:.2f}
Produtos (shampoo, etc.): {despesa_produtos:.2f}
Aluguel: {despesa_aluguel:.2f}
Outras despesas: {despesa_outros:.2f}

### OPERAÇÃO ###
Número de atendimentos mensais: {numero_atendimentos_mes}
Tempo médio de banho e tosa: {tempo_medio_banho_tosa} minutos
Ticket médio: {ticket_medio:.2f}
Meta de lucro mensal: {meta_lucro:.2f}

### MÉTRICAS CALCULADAS ###
Despesa total: {despesa_total:.2f}
Despesa com pessoal: {despesa_pessoal:.2f}
Lucro atual: {lucro_atual:.2f}
Margem de lucro: {margem_lucro:.2f}%
Horas de operação diárias: {tempo_ocioso_diario:.1f}h
Faturamento potencial: {faturamento_potencial:.2f}
Faturamento não realizado: {faturamento_nao_realizado:.2f}
Proporção de despesas com pessoal: {proporcao_pessoal:.2f}%
Proporção de despesas com produtos: {proporcao_produtos:.2f}%
Proporção de despesas com aluguel: {proporcao_aluguel:.2f}%
Custo fixo mensal: {custo_fixo:.2f}
Custo variável mensal: {custo_variavel:.2f}

{metricas_condicionais}

### PADRÕES DO SETOR PARA COMPARAÇÃO ###
Margem de lucro saudável para petshops: 15-25%
Proporção típica de despesas com pessoal: 40-50%
Ticket médio típico em petshops: R$ 80-150
Faturamento médio por funcionário no setor: R$ 5.000-8.000
Taxa de ocupação ideal: 70-85%

### PRINCIPAL DESAFIO ###
{principal_desafio if principal_desafio else "Não informado"}

### INSTRUÇÕES DE ANÁLISE ###

1. SAÚDE FINANCEIRA ATUAL:
Elabore uma análise detalhada da saúde financeira atual do petshop em dois parágrafos.
Compare os dados com os padrões do setor. Mencione pontos fortes e fracos identificados.
Seja específico e objetivo, focando nas métricas mais relevantes.

2. DIAGNÓSTICO DE EFICIÊNCIA:
Identifique as três principais ineficiências operacionais ou financeiras.
Para cada uma, explique o impacto nos resultados e quantifique quando possível.
Considere aspectos como produtividade dos funcionários, utilização da capacidade, estrutura de custos.

3. RECOMENDAÇÕES PRÁTICAS:
Forneça cinco recomendações específicas, detalhadas e aplicáveis para melhorar o desempenho financeiro.
Para cada recomendação:
   a) Explique exatamente o que deve ser feito
   b) Estime o impacto financeiro potencial (em R$ ou %)
   c) Sugira como implementar (passos práticos, ferramentas, processos)
   d) Indique um prazo razoável para implementação e resultados

4. PRIORIDADES DE CURTO PRAZO:
Destaque as três ações mais urgentes que o dono deve tomar nos próximos 30 dias.
Explique por que são prioritárias e qual o impacto esperado.

5. METAS SUGERIDAS:
Defina três metas financeiras realistas para os próximos 3 meses, com valores específicos.
Por exemplo: "Aumentar a margem de lucro de 12% para 18% em 3 meses".

Seja detalhado, objetivo e prático. Evite generalidades como "melhorar o marketing" ou "reduzir custos".
Use números específicos e percentuais sempre que possível.
Considere o contexto de um petshop brasileiro de pequeno porte.
Suas recomendações devem ser viáveis para um negócio deste tamanho e setor.
"""


def get_financial_consultor_prompt(
    dados,
    fmt_currency,
    fmt_percent,
    resultado,
    metricas_condicionais,
    principal_desafio,
):
    return prompt.format(
        **dados.__dict__,
        fmt_currency=fmt_currency,
        fmt_percent=fmt_percent,
        **resultado.__dict__,
        metricas_condicionais=metricas_condicionais,
        principal_desafio=principal_desafio
    )
