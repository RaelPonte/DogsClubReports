from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class PetshopData(BaseModel):
    """Modelo para os dados do petshop"""

    # Informações Básicas
    nome: Optional[str] = Field(description="Nome completo do usuário", default=None)
    nome_petshop: str = Field(description="Nome do Petshop")
    email_contato: Optional[str] = Field(description="E-mail de contato", default=None)
    telefone_contato: Optional[str] = Field(
        default=None, description="Telefone de contato"
    )
    whatsapp_contato: Optional[str] = Field(
        default=None, description="Número de WhatsApp para contato"
    )

    # Dados operacionais
    horario_abertura: str = Field(description="Horário de abertura (formato HH:MM)")
    horario_fechamento: str = Field(description="Horário de fechamento (formato HH:MM)")
    dias_funcionamento_semana: int = Field(
        description="Dias de funcionamento por semana", ge=1, le=7
    )

    # Pessoal
    numero_funcionarios: int = Field(description="Número total de funcionários")
    funcionarios_banho_tosa: int = Field(
        description="Número de funcionários de banho e tosa"
    )
    salario_medio: float = Field(description="Salário médio por funcionário em reais")

    # Capacidade e desempenho
    tempo_medio_banho_tosa: int = Field(
        description="Tempo médio para banho e tosa (minutos)", ge=30
    )
    numero_atendimentos_mes: int = Field(
        description="Número atual de atendimentos por mês"
    )

    # Valores e financeiro
    ticket_medio: float = Field(description="Valor médio por atendimento (R$)")
    faturamento_mensal: float = Field(description="Faturamento mensal atual (R$)")
    faturamento_mes_anterior: Optional[float] = Field(
        description="Faturamento do mês anterior em reais", default=None
    )

    # Despesas
    despesa_agua_luz: float = Field(
        description="Despesa mensal com água e luz em reais"
    )
    despesa_produtos: float = Field(
        description="Despesa mensal com produtos (shampoo, etc.) em reais"
    )
    despesa_aluguel: Optional[float] = Field(
        description="Despesa mensal com aluguel em reais", default=0.0
    )
    despesa_outros: Optional[float] = Field(
        description="Outras despesas mensais em reais", default=0.0
    )
    custo_fixo_mensal: Optional[float] = Field(
        description="Custos fixos mensais (R$)", default=None
    )
    custo_produto_percentual: Optional[float] = Field(
        description="Percentual do faturamento gasto com produtos (%)",
        ge=0,
        le=100,
        default=None,
    )

    # Metas e desafios
    meta_lucro: Optional[float] = Field(
        description="Meta de lucro mensal (R$)", default=None
    )
    meta_faturamento: Optional[float] = Field(
        description="Meta de faturamento mensal (R$)", default=None
    )
    principal_desafio: Optional[str] = Field(
        description="Principal desafio atual do negócio", default=None
    )

    # Validadores
    @validator("horario_abertura", "horario_fechamento")
    def validar_formato_hora(cls, v):
        if not re.match(r"^\d{1,2}:\d{2}$", v):
            raise ValueError("Formato de hora deve ser HH:MM")
        return v

    @validator(
        "faturamento_mensal",
        "faturamento_mes_anterior",
        "salario_medio",
        "ticket_medio",
        "despesa_agua_luz",
        "despesa_produtos",
        "despesa_aluguel",
        "despesa_outros",
        "custo_fixo_mensal",
    )
    def validar_valor_positivo(cls, v):
        if v is not None and v < 0:
            raise ValueError("O valor deve ser positivo")
        return v

    @validator("funcionarios_banho_tosa")
    def validar_funcionarios_banho_tosa(cls, v, values):
        if "numero_funcionarios" in values and v > values["numero_funcionarios"]:
            raise ValueError(
                "O número de funcionários de banho e tosa não pode ser maior que o total de funcionários"
            )
        return v
