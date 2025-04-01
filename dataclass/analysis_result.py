from pydantic import BaseModel
from typing import Optional


class AnalisysResult(BaseModel):
    """Modelo para armazenar os resultados da análise"""

    # Métricas básicas
    faturamento_atual: float
    faturamento_potencial: float
    faturamento_nao_realizado: float
    percentual_capacidade_utilizada: float

    # Projeções
    projecao_anual_atual: float
    projecao_anual_potencial: float

    # Métricas operacionais
    capacidade_diaria_ideal: int
    capacidade_mensal_ideal: int
    ocupacao_atual_percentual: float
    tempo_ocioso_diario: float  # em horas

    # Métricas financeiras
    despesa_total: float
    despesa_pessoal: float
    lucro_atual: float
    lucro_potencial: float
    margem_lucro: float

    # Dados de eficiência
    atendimentos_por_funcionario: float
    atendimentos_potenciais_por_funcionario: float
    receita_por_funcionario: float
    receita_potencial_por_funcionario: float

    # Estrutura de custos
    proporcao_pessoal: Optional[float] = None
    proporcao_produtos: Optional[float] = None
    proporcao_aluguel: Optional[float] = None
    custo_fixo: Optional[float] = None
    custo_variavel: Optional[float] = None
    ponto_equilibrio_atendimentos: Optional[int] = None

    # Crescimento
    crescimento_receita: Optional[float] = None
    diferenca_meta: Optional[float] = None
