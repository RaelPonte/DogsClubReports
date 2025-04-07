import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.patheffects import withStroke
from matplotlib.colors import LinearSegmentedColormap


def create_data_visualizations(resultado):
    """Cria gráficos para visualizar diferentes aspectos dos resultados com estilo moderno"""
    # Configurar estilo moderno
    plt.style.use("seaborn-v0_8-whitegrid")

    # Configurações globais para todos os gráficos
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 12,
            "axes.titlesize": 16,
            "axes.titleweight": "bold",
            "axes.labelsize": 13,
            "axes.labelweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
        }
    )

    # Paleta de cores moderna
    color_palette = {
        "primary": "#0a8a40",  # Verde principal
        "secondary": "#3498db",  # Azul
        "accent": "#f39c12",  # Laranja
        "error": "#e74c3c",  # Vermelho
        "neutral": "#95a5a6",  # Cinza
        "light": "#ecf0f1",  # Cinza claro
        "dark": "#2c3e50",  # Azul escuro
    }

    # Função helper para criar degradês
    def create_gradient_color(color, num_colors=10):
        """Cria uma lista de cores em degradê a partir de uma cor base"""
        base_rgb = mpl.colors.to_rgb(color)
        white_rgb = mpl.colors.to_rgb("#ffffff")
        return [
            mpl.colors.to_hex(
                (
                    base_rgb[0] + (white_rgb[0] - base_rgb[0]) * i / num_colors,
                    base_rgb[1] + (white_rgb[1] - base_rgb[1]) * i / num_colors,
                    base_rgb[2] + (white_rgb[2] - base_rgb[2]) * i / num_colors,
                )
            )
            for i in range(num_colors)
        ]

    # Função helper para estilizar títulos
    def style_title(ax, title):
        ax.set_title(
            title,
            pad=20,
            fontsize=18,
            fontweight="bold",
            color=color_palette["dark"],
            backgroundcolor="#f8f9fa",
            bbox=dict(boxstyle="round,pad=0.5", ec="#dddddd", fc="#f8f9fa"),
        )

    # Função helper para estilizar as bordas dos gráficos
    def style_chart(ax):
        # Remover o frame direito e superior
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Estilizar os spines restantes
        ax.spines["bottom"].set_color("#dddddd")
        ax.spines["left"].set_color("#dddddd")

        # Estilizar a grade
        ax.grid(True, linestyle="-", alpha=0.2, color="#cccccc")

        # Estilizar os ticks
        ax.tick_params(colors=color_palette["dark"])

    # 1. Faturamento Atual vs Potencial - Gráfico de barras moderno
    fig3, ax1 = plt.subplots(figsize=(10, 8), facecolor="white")
    labels = ["Atual", "Potencial"]
    valores = [resultado.faturamento_atual, resultado.faturamento_potencial]

    # Gradiente de cores para as barras
    atual_color = color_palette["secondary"]
    potencial_color = color_palette["primary"]

    # Criar gradientes para as barras
    atual_gradient = create_gradient_color(atual_color, 5)
    potencial_gradient = create_gradient_color(potencial_color, 5)

    # Criar gradientes para as barras usando um LinearGradient
    atual_cmap = LinearSegmentedColormap.from_list(
        "atual_cmap", [atual_color, "#ffffff"]
    )
    potencial_cmap = LinearSegmentedColormap.from_list(
        "potencial_cmap", [potencial_color, "#ffffff"]
    )

    # Desenhar barras com gradiente de cores
    for i, (valor, cmap, label) in enumerate(
        zip(valores, [atual_cmap, potencial_cmap], labels)
    ):
        # Criar a barra com gradiente
        for j in range(100):
            height_fraction = j / 100
            bar_height = valor * height_fraction
            bar_bottom = valor * (1 - height_fraction)
            ax1.bar(
                label,
                bar_height,
                bottom=bar_bottom,
                color=cmap(height_fraction * 0.8),
                width=0.6,
                edgecolor=None,
                linewidth=0,
            )

        # Adicionar borda à barra completa
        ax1.bar(label, valor, width=0.6, fill=False, edgecolor="white", linewidth=2)

    # Adicionar valor de crescimento potencial
    if resultado.faturamento_potencial > resultado.faturamento_atual:
        crescimento = resultado.faturamento_potencial - resultado.faturamento_atual
        percentual = (crescimento / resultado.faturamento_atual) * 100

        # Fundo para o texto
        ax1.annotate(
            f"+{percentual:.1f}%",
            xy=(1, resultado.faturamento_atual + crescimento / 2),
            xytext=(1.4, resultado.faturamento_atual + crescimento / 2),
            arrowprops=dict(
                arrowstyle="->",
                color=color_palette["primary"],
                connectionstyle="arc3,rad=.2",
                lw=2,
            ),
            fontsize=14,
            fontweight="bold",
            color=color_palette["primary"],
            bbox=dict(
                boxstyle="round,pad=0.3",
                fc="white",
                ec=color_palette["primary"],
                alpha=0.9,
            ),
            path_effects=[withStroke(linewidth=3, foreground="white")],
        )

    # Estilizar o gráfico
    style_title(ax1, "Faturamento Mensal")
    ax1.set_ylabel(
        "Valor (R$)", fontweight="bold", color=color_palette["dark"], labelpad=15
    )
    style_chart(ax1)

    # Eixo Y com formatação monetária
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f"R$ {x/1000:.0f}k"))

    # Adicionar rótulos nas barras
    for i, (label, valor) in enumerate(zip(labels, valores)):
        ax1.text(
            i,  # índice da barra (0 para Atual, 1 para Potencial)
            valor * 1.02,  # ligeiramente acima do topo da barra
            f"R$ {valor:,.2f}".replace(",", "."),
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
            color=color_palette["dark"],
            path_effects=[withStroke(linewidth=3, foreground="white")],
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#dddddd", alpha=0.7),
        )

    # Ajustar limites do eixo Y para dar mais espaço vertical
    bottom, top = ax1.get_ylim()
    ax1.set_ylim(bottom, top * 1.15)  # 15% mais alto para acomodar textos

    fig3.tight_layout(pad=3.5)

    # 2. Gráfico de ocupação - Donut chart
    fig1, ax2 = plt.subplots(figsize=(8, 9), facecolor="white")
    ocupacao = resultado.ocupacao_atual_percentual
    livre = 100 - ocupacao

    # Definir cores baseadas no nível de ocupação
    if ocupacao < 50:
        ocupacao_color = color_palette["error"]  # Vermelho para baixa ocupação
    elif ocupacao < 70:
        ocupacao_color = color_palette["accent"]  # Laranja para ocupação média
    else:
        ocupacao_color = color_palette["primary"]  # Verde para boa ocupação

    # Criar gráfico de donut com efeito 3D
    wedges, texts = ax2.pie(
        [ocupacao, livre],
        labels=None,  # Sem rótulos automáticos
        autopct=None,  # Sem percentuais automáticos
        startangle=90,
        colors=[ocupacao_color, color_palette["light"]],
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
        shadow=True,
        counterclock=False,
    )

    # Círculo central para efeito de donut
    circle = plt.Circle((0, 0), 0.2, fc="white")
    ax2.add_artist(circle)

    # Adicionar texto central no donut com fundo para melhor visibilidade
    central_bg = plt.Circle((0, 0), 0.18, fc="white", ec="#dddddd", alpha=0.9)
    ax2.add_patch(central_bg)

    ax2.text(
        0,
        0,
        f"{ocupacao:.1f}%",
        ha="center",
        va="center",
        fontsize=32,
        fontweight="bold",
        color=ocupacao_color,
        path_effects=[withStroke(linewidth=4, foreground="white")],
    )
    ax2.text(
        0,
        -0.11,
        "ocupação",
        ha="center",
        va="center",
        fontsize=14,
        color=color_palette["dark"],
        path_effects=[withStroke(linewidth=3, foreground="white")],
    )

    # Adicionar legendas personalizadas com melhor posicionamento
    labels = ["Utilizada", "Não utilizada"]
    legend_elements = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=ocupacao_color,
            markersize=12,
            label=f"{labels[0]}: {ocupacao:.1f}%",
        ),
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color_palette["light"],
            markersize=12,
            label=f"{labels[1]}: {livre:.1f}%",
        ),
    ]
    ax2.legend(
        handles=legend_elements,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=2,
        frameon=True,
        fancybox=True,
        shadow=True,
        fontsize=12,
    )

    # Título
    style_title(ax2, "Taxa de Ocupação")
    ax2.axis("equal")

    fig1.tight_layout(pad=4.0)

    # 3. Margem de Lucro Atual vs Padrão do Setor
    fig4, ax3 = plt.subplots(figsize=(10, 8), facecolor="white")

    margem_atual = resultado.margem_lucro
    margem_min, margem_max = 15, 25  # Valores padrão do setor

    x = ["Atual", "Mínimo\nSetor", "Máximo\nSetor"]
    y = [margem_atual, margem_min, margem_max]

    # Determinar cor para a barra atual baseado na comparação com o padrão do setor
    if margem_atual < margem_min:
        cor_atual = color_palette["error"]  # Vermelho se abaixo do mínimo
    elif margem_atual > margem_max:
        cor_atual = color_palette["primary"]  # Verde se acima do máximo
    else:
        cor_atual = color_palette["accent"]  # Laranja se dentro do padrão

    # Criar gradientes para as barras
    atual_cmap = LinearSegmentedColormap.from_list("atual_cmap", [cor_atual, "#ffffff"])
    setor_cmap = LinearSegmentedColormap.from_list(
        "setor_cmap", [color_palette["neutral"], "#ffffff"]
    )

    cmaps = [atual_cmap, setor_cmap, setor_cmap]

    # Desenhar barras com gradiente
    for i, (valor, label, cmap) in enumerate(zip(y, x, cmaps)):
        # Criar a barra com gradiente
        for j in range(100):
            height_fraction = j / 100
            bar_height = valor * height_fraction
            bar_bottom = valor * (1 - height_fraction)
            ax3.bar(
                label,
                bar_height,
                bottom=bar_bottom,
                color=cmap(height_fraction * 0.8),
                width=0.5,
                edgecolor=None,
                linewidth=0,
            )

        # Adicionar borda à barra completa
        ax3.bar(label, valor, width=0.5, fill=False, edgecolor="white", linewidth=2)

    # Adicionar área sombreada para a faixa ideal com gradiente
    x_span = np.arange(-0.5, 2.5, 0.01)
    y_min = np.ones_like(x_span) * margem_min
    y_max = np.ones_like(x_span) * margem_max

    # Preenchimento com degradê para a área ideal
    ax3.fill_between(
        x_span,
        y_min,
        y_max,
        color=color_palette["primary"],
        alpha=0.15,
        zorder=0,
        label="Faixa Ideal",
    )

    # Adicionar linha de contorno para a área ideal
    ax3.plot(
        x_span, y_min, "--", color=color_palette["primary"], alpha=0.5, lw=1.5, zorder=1
    )
    ax3.plot(
        x_span, y_max, "--", color=color_palette["primary"], alpha=0.5, lw=1.5, zorder=1
    )

    # Adicionar linha tracejada na margem atual com melhor visibilidade
    ax3.plot(
        [-0.5, 2.5],
        [margem_atual, margem_atual],
        linestyle="--",
        color=cor_atual,
        lw=2,
        alpha=0.7,
        zorder=2,
    )

    # Estilização do gráfico
    style_title(ax3, "Margem de Lucro")
    ax3.set_ylabel(
        "Porcentagem (%)", fontweight="bold", color=color_palette["dark"], labelpad=15
    )
    style_chart(ax3)

    # Clarificar a área ideal com fundo para melhor visibilidade
    if margem_atual >= margem_min and margem_atual <= margem_max:
        status_message = "✓ Dentro da média do setor"
        color_message = color_palette["primary"]
    elif margem_atual < margem_min:
        status_message = "! Abaixo da média do setor"
        color_message = color_palette["error"]
    else:
        status_message = "✓ Acima da média do setor"
        color_message = color_palette["primary"]

    # Ajustar limites do eixo Y para acomodar melhor todos os textos
    y_min_value = 0
    y_max_value = (
        max(margem_atual, margem_max) * 1.5
    )  # Aumentado de 1.3 para 1.5 (50% mais alto)
    ax3.set_ylim(y_min_value, y_max_value)

    # Adicionar texto explicativo em posição mais visível
    ax3.text(
        1.5,  # Centralizado entre as duas últimas barras
        y_max_value * 0.9,  # Posição um pouco mais abaixo (de 0.95 para 0.9)
        "Faixa ideal do setor",
        ha="center",
        va="top",
        color=color_palette["primary"],
        fontsize=14,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.5", fc="white", ec=color_palette["primary"], alpha=0.9
        ),
        zorder=5,
    )

    # Mostrar status atual com destaque maior
    ax3.text(
        0,  # Alinhado com a primeira barra
        y_max_value * 0.9,  # Posição um pouco mais abaixo (de 0.95 para 0.9)
        status_message,
        ha="center",
        va="top",
        color=color_message,
        fontsize=14,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=color_message, alpha=0.9),
        path_effects=[withStroke(linewidth=3, foreground="white")],
        zorder=5,
    )

    # Adicionar rótulos explícitos para os limites da faixa ideal no lado direito
    ax3.text(
        2.5,  # Fora do gráfico à direita
        margem_min,
        f"{margem_min}%",
        ha="left",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=color_palette["primary"],
        bbox=dict(
            boxstyle="round,pad=0.3", fc="white", ec=color_palette["primary"], alpha=0.8
        ),
        zorder=5,
    )

    ax3.text(
        2.5,  # Fora do gráfico à direita
        margem_max,
        f"{margem_max}%",
        ha="left",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=color_palette["primary"],
        bbox=dict(
            boxstyle="round,pad=0.3", fc="white", ec=color_palette["primary"], alpha=0.8
        ),
        zorder=5,
    )

    # Adicionar rótulos nas barras com maior destaque
    for i, (label, valor) in enumerate(zip(x, y)):
        # Posicionar texto bem acima da barra para evitar sobreposições
        ax3.text(
            i,  # índice da barra
            valor * 1.15,  # Posicionado mais acima (de 1.1 para 1.15)
            f"{valor:.1f}%",
            ha="center",
            va="bottom",
            fontsize=14,
            fontweight="bold",
            color=color_palette["dark"],
            path_effects=[withStroke(linewidth=4, foreground="white")],
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#dddddd", alpha=0.95),
            zorder=5,
        )

    # Aumentar o contraste das linhas de referência
    ax3.plot(
        x_span, y_min, "--", color=color_palette["primary"], alpha=0.7, lw=2.5, zorder=1
    )
    ax3.plot(
        x_span, y_max, "--", color=color_palette["primary"], alpha=0.7, lw=2.5, zorder=1
    )

    # Adicionar um rótulo semitransparente na área preenchida
    ax3.text(
        1.0,  # Centro do gráfico
        (margem_min + margem_max) / 2,  # Centro da faixa ideal
        "Faixa Ideal",
        ha="center",
        va="center",
        fontsize=16,
        color=color_palette["primary"],
        alpha=0.4,
        fontweight="bold",
        rotation=0,
        zorder=2,
    )

    fig4.tight_layout(pad=4.0)

    # 4. Estrutura de Custos - Gráfico de pizza moderno
    fig2, ax4 = plt.subplots(figsize=(8, 9), facecolor="white")

    # Calcular componentes de custo
    custo_pessoal = max(0, getattr(resultado, "despesa_pessoal", 0))
    custo_produtos = max(0, getattr(resultado, "custo_variavel", 0))
    if custo_produtos == 0 and hasattr(resultado, "despesa_produtos"):
        custo_produtos = max(0, getattr(resultado, "despesa_produtos", 0))

    despesa_total = max(0, getattr(resultado, "despesa_total", 0))
    custo_outros = max(0, despesa_total - custo_pessoal - custo_produtos)

    custos = [custo_pessoal, custo_produtos, custo_outros]
    labels = ["Pessoal", "Produtos", "Outros"]
    custo_colors = [
        color_palette["secondary"],
        color_palette["primary"],
        color_palette["neutral"],
    ]

    # Criar gráfico
    if sum(custos) > 0:
        # Destacar maior componente puxando-o para fora
        explode = [0, 0, 0]
        max_idx = custos.index(max(custos))
        explode[max_idx] = 0.1

        # Criar o gráfico com efeito 3D e explode
        wedges, texts = ax4.pie(
            custos,
            labels=None,
            autopct=None,
            startangle=90,
            colors=custo_colors,
            explode=explode,
            shadow=True,
            wedgeprops=dict(edgecolor="white", linewidth=2),
        )

        # Adicionar legendas com percentuais
        total = sum(custos)
        percents = [c / total * 100 for c in custos]

        legend_elements = []
        for i, (label, pct) in enumerate(zip(labels, percents)):
            # Criar elemento da legenda com percentual
            legend_elements.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor=custo_colors[i],
                    markersize=12,
                    label=f"{label}: {pct:.1f}%",
                )
            )

        ax4.legend(
            handles=legend_elements,
            loc="center",
            bbox_to_anchor=(0.5, -0.05),
            ncol=len(legend_elements),
            frameon=True,
            fancybox=True,
            shadow=True,
            fontsize=12,
        )

        # Adicionar valor total no centro com fundo para melhor visibilidade
        central_bg = plt.Circle((0, 0), 0.25, fc="white", ec="#dddddd", alpha=0.9)
        ax4.add_patch(central_bg)

        ax4.text(
            0,
            0.02,
            "R$ " + f"{total/1000:.1f}k",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
            color=color_palette["dark"],
            path_effects=[withStroke(linewidth=4, foreground="white")],
        )
        ax4.text(
            0,
            -0.08,
            "Total de Despesas",
            ha="center",
            va="center",
            fontsize=12,
            color=color_palette["dark"],
            path_effects=[withStroke(linewidth=3, foreground="white")],
        )

    else:
        # Se não houver dados de custo, mostrar um gráfico vazio com mensagem
        ax4.text(
            0.5,
            0.5,
            "Dados de custos não disponíveis",
            ha="center",
            va="center",
            fontsize=14,
            color=color_palette["neutral"],
            fontweight="bold",
        )
        ax4.axis("off")

    style_title(ax4, "Estrutura de Custos")
    ax4.axis("equal")

    fig2.tight_layout(pad=4.0)

    return [fig1, fig2, fig3, fig4]
