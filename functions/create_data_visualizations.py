import matplotlib.pyplot as plt


def create_data_visualizations(resultado):
    """Cria gráficos para visualizar diferentes aspectos dos resultados"""
    # Configurar estilo
    plt.style.use("ggplot")
    plt.rcParams.update({"font.size": 12})

    # 1. Faturamento Atual vs Potencial
    fig3, ax1 = plt.subplots(figsize=(10, 6))
    labels = ["Atual", "Potencial"]
    valores = [resultado.faturamento_atual, resultado.faturamento_potencial]
    cores = ["#3498db", "#2ecc71"]  # Azul e Verde

    barras = ax1.bar(labels, valores, color=cores)
    ax1.set_title("Faturamento Mensal (R$)")
    ax1.set_ylabel("Valor (R$)")

    # Formatar eixo Y para valores monetários
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f"R$ {x/1000:.0f}k"))

    # Adicionar rótulos nas barras
    for i, barra in enumerate(barras):
        altura = barra.get_height()
        ax1.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura + 0.05 * max(valores),
            f"R$ {altura:,.2f}".replace(",", "."),
            ha="center",
            va="bottom",
            rotation=0,
            fontsize=10,
        )

    # 2. Gráfico de ocupação (pizza/rosca)
    fig1, ax2 = plt.subplots(figsize=(8, 8))
    ocupacao = resultado.ocupacao_atual_percentual
    livre = 100 - ocupacao

    ax2.pie(
        [ocupacao, livre],
        labels=["Utilizada", "Não utilizada"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#3498db", "#95a5a6"],  # Azul e Cinza
        wedgeprops=dict(width=0.3),
    )
    ax2.set_title("Taxa de Ocupação")
    ax2.axis("equal")

    # 3. Margem de Lucro Atual vs Padrão do Setor
    fig4, ax3 = plt.subplots(figsize=(10, 6))

    margem_atual = resultado.margem_lucro
    margem_min, margem_max = 15, 25  # Valores padrão do setor

    x = ["Atual", "Mínimo Setor", "Máximo Setor"]
    y = [margem_atual, margem_min, margem_max]

    # Determinar cor para a barra atual baseado na comparação com o padrão do setor
    if margem_atual < margem_min:
        cor_atual = "#e74c3c"  # Vermelho se abaixo do mínimo
    elif margem_atual > margem_max:
        cor_atual = "#2ecc71"  # Verde se acima do máximo
    else:
        cor_atual = "#3498db"  # Azul se dentro do padrão

    cores_barras = [
        cor_atual,
        "#95a5a6",
        "#95a5a6",
    ]  # Cinza para as barras de referência

    barras = ax3.bar(x, y, color=cores_barras)
    ax3.set_title("Margem de Lucro (%)")
    ax3.set_ylabel("Porcentagem (%)")

    # Adicionar rótulos nas barras
    for i, barra in enumerate(barras):
        altura = barra.get_height()
        ax3.text(
            barra.get_x() + barra.get_width() / 2.0,
            altura + 0.5,
            f"{altura:.1f}%",
            ha="center",
            va="bottom",
        )

    # 4. Estrutura de Custos (gráfico de pizza)
    fig2, ax4 = plt.subplots(figsize=(8, 8))

    # Calcular componentes de custo
    custo_pessoal = max(0, getattr(resultado, "despesa_pessoal", 0))
    custo_produtos = max(
        0, getattr(resultado, "custo_variavel", 0)
    )  # Usar getattr para evitar AttributeError
    if custo_produtos == 0 and hasattr(resultado, "despesa_produtos"):
        custo_produtos = max(0, getattr(resultado, "despesa_produtos", 0))

    despesa_total = max(0, getattr(resultado, "despesa_total", 0))
    custo_outros = max(0, despesa_total - custo_pessoal - custo_produtos)

    custos = [custo_pessoal, custo_produtos, custo_outros]
    labels = ["Pessoal", "Produtos", "Outros"]

    # Calcular percentuais
    total = sum(custos)

    # Criar gráfico
    if total > 0:
        wedges, texts, autotexts = ax4.pie(
            custos,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#3498db", "#2ecc71", "#95a5a6"],  # Azul, Verde e Cinza
        )
    else:
        # Se não houver dados de custo, mostrar um gráfico vazio com mensagem
        ax4.text(
            0.5,
            0.5,
            "Dados de custos não disponíveis",
            ha="center",
            va="center",
            fontsize=12,
            color="#95a5a6",
        )
        ax4.axis("off")
    ax4.set_title("Estrutura de Custos")
    ax4.axis("equal")

    return [fig1, fig2, fig3, fig4]
