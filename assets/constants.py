WORKING_DAYS_IN_THE_MONTH = 22  # Média de dias úteis por mês
SERVICES_TIME = {
    'banho': 60,  # tempo em minutos
    'tosa_simples': 75,
    'tosa_completa': 90,
    'banho_tosa': 120,
    'hidratacao': 40,
    'desembolo': 120,
    'tosa_higienica': 30
}

# Cores para visualizações
COLORS = {
    'primaria': '#3498db',     # Azul
    'secundaria': '#2ecc71',   # Verde
    'destaque': '#e74c3c',     # Vermelho
    'neutra': '#95a5a6',       # Cinza
    'alerta': '#f39c12',       # Laranja
    'fundo': '#f9f9f9',        # Cinza claro
    'texto': '#2c3e50'         # Azul escuro
}

# Padrões do setor
INDUSTRY_STANDARD = {
    'margem_lucro': (15, 25),            # Porcentagem
    'proporcao_pessoal': (40, 50),       # Porcentagem
    'ticket_medio': (80, 150),           # R$
    'faturamento_funcionario': (5000, 8000),  # R$
    'taxa_ocupacao': (70, 85)            # Porcentagem
}