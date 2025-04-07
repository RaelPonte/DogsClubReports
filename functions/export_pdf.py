from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.units import inch
from datetime import datetime
import io
from reportlab.lib.enums import TA_CENTER
from utils import format_currency, format_percent


def export_dashboard_pdf(dados, resultado, relatorio, figuras):
    """Exporta o dashboard como PDF, mantendo a aparência visual do Streamlit"""
    # Criar buffer para o PDF
    buffer = io.BytesIO()

    # Configurar o documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,  # Margens menores para maior espaço
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
        title=f"Análise Financeira - {dados.nome_petshop}",
    )

    # Lista de elementos do PDF
    elements = []

    # Estilos aprimorados
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=26,
        spaceAfter=20,
        textColor=colors.HexColor("#3498db"),
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        italic=False,
    )
    subtitle_style = ParagraphStyle(
        "CustomSubTitle",
        parent=styles["Heading2"],
        fontSize=20,
        spaceAfter=15,
        textColor=colors.HexColor("#2c3e50"),
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        italic=False,
    )
    section_style = ParagraphStyle(
        "CustomSection",
        parent=styles["Heading3"],
        fontSize=16,
        spaceAfter=10,
        textColor=colors.HexColor("#3498db"),
        borderPadding=(0, 0, 5, 0),
        borderWidth=0,
        borderColor=colors.HexColor("#e0e0e0"),
        borderRadius=5,
        fontName="Helvetica-Bold",
        italic=False,
    )

    # Criar estilo para texto normal com quebra de linha adequada
    normal_style_wrapped = ParagraphStyle(
        "NormalWrapped",
        parent=styles["Normal"],
        wordWrap="CJK",
        alignment=0,  # Alinhamento à esquerda
        firstLineIndent=0,
        leading=14,  # Espaçamento entre linhas
        spaceAfter=6,  # Espaço após o parágrafo
    )

    # Estilo que permite processamento de tags HTML
    html_style = ParagraphStyle(
        "HTMLStyle",
        parent=styles["Normal"],
        wordWrap="CJK",
        leading=14,
    )

    # Adicionar logo e cabeçalho
    # Logo do Dogs Club - Criar um buffer para a imagem (substitua pelo caminho correto da logo)
    try:
        logo_path = "https://dogs-club-source.s3.us-east-1.amazonaws.com/logo.png"  # Ajuste o caminho conforme necessário
        logo = Image(logo_path)

        scale_factor = 0.3
        logo.drawWidth = logo.drawWidth * scale_factor
        logo.drawHeight = logo.drawHeight * scale_factor

        logo.hAlign = "CENTER"
        elements.append(logo)
    except:
        # Se não conseguir carregar a logo, continue sem ela
        pass

    elements.append(Paragraph("Análise Financeira", title_style))
    elements.append(Paragraph(dados.nome_petshop, subtitle_style))
    elements.append(
        Paragraph(
            f"Data de geração do relatório: {datetime.now().strftime('%d/%m/%Y')}",
            ParagraphStyle("Date", parent=styles["Normal"], alignment=TA_CENTER),
        )
    )
    elements.append(Spacer(1, 20))

    # Métricas Principais - Agora com layout moderno e cores
    elements.append(Paragraph("Métricas Principais", section_style))
    elements.append(Spacer(1, 10))

    # Criar tabela de métricas com cores e formatação aprimorada
    metrics_data = [
        ["Faturamento Mensal", "Lucro Mensal", "Taxa de Ocupação"],
        [
            format_currency(resultado.faturamento_atual),
            format_currency(resultado.lucro_atual),
            format_percent(resultado.ocupacao_atual_percentual),
        ],
        [
            f"Potencial: {format_currency(resultado.faturamento_potencial)}",
            f"Margem: {format_percent(resultado.margem_lucro)}",
            f"Tempo ocioso: {resultado.tempo_ocioso_diario:.1f}h/dia",
        ],
    ]
    ROW_HEIGHTS = 30
    metrics_table = Table(
        metrics_data,
        colWidths=[160] * 3,
        rowHeights=ROW_HEIGHTS,
        hAlign="CENTER",
        vAlign="MIDDLE",
    )
    metrics_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, 1),
                    14,
                ),  # Tamanho maior para valores principais
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),  # Valores em negrito
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#3498db"),
                ),  # Azul Dogs Club
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),  # Texto branco no cabeçalho
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, 1),
                    colors.HexColor("#f8f9fa"),
                ),  # Fundo claro
                ("BACKGROUND", (0, 2), (-1, 2), colors.white),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e0e0e0")),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e0e0e0")),
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, 0),
                    2,
                    colors.HexColor("#3498db"),
                ),  # Linha mais grossa abaixo do cabeçalho
                ("ROUNDEDCORNERS", [10, 10, 10, 10]),
            ]
        )
    )
    elements.append(metrics_table)
    elements.append(Spacer(1, 25))

    # Potencial Não Aproveitado com design aprimorado
    elements.append(Paragraph("Potencial Não Aproveitado", section_style))
    elements.append(Spacer(1, 10))

    potential_data = [
        ["Dinheiro Deixado na Mesa", "Capacidade Não Utilizada"],
        [
            f"{format_currency(resultado.faturamento_nao_realizado * 12)}/ano",
            f"{resultado.capacidade_mensal_ideal - dados.numero_atendimentos_mes} atendimentos/mês",
        ],
    ]

    potential_table = Table(
        potential_data,
        colWidths=[240] * 2,
        rowHeights=ROW_HEIGHTS,
    )
    potential_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("FONTSIZE", (0, 1), (-1, 1), 16),  # Valores destacados maiores
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#e74c3c"),
                ),  # Vermelho para alertar
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, 1),
                    colors.HexColor("#fff8f8"),
                ),  # Vermelho bem claro
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, 1),
                    colors.HexColor("#e74c3c"),
                ),  # Texto vermelho para os valores
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e0e0e0")),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#e0e0e0")),
            ]
        )
    )
    elements.append(potential_table)
    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "<h2><b>Observe os gráficos abaixo na página seguinte para entender melhor o potencial de aumento de lucro.</b></h2>",
            html_style,
        )
    )
    elements.append(Spacer(1, 190))

    # Visualizações - Adicionar gráficos aprimorados
    elements.append(Paragraph("Visualizações", section_style))
    elements.append(Spacer(1, 15))

    # Para colocar duas figuras lado a lado, usaremos uma tabela
    fig_count = len(figuras)
    for i in range(0, fig_count, 2):
        # Processar a primeira imagem
        img_buffer1 = io.BytesIO()
        figuras[i].savefig(img_buffer1, format="png", bbox_inches="tight", dpi=150)
        img_buffer1.seek(0)

        img1 = Image(img_buffer1)
        scale_factor = 0.2
        img1.drawWidth = img1.drawWidth * scale_factor
        img1.drawHeight = img1.drawHeight * scale_factor

        # Verificar se há uma segunda imagem
        if i + 1 < fig_count:
            # Processar a segunda imagem
            img_buffer2 = io.BytesIO()
            figuras[i + 1].savefig(
                img_buffer2, format="png", bbox_inches="tight", dpi=150
            )
            img_buffer2.seek(0)
            img2 = Image(img_buffer2)
            img2.drawWidth = img2.drawWidth * scale_factor
            img2.drawHeight = img2.drawHeight * scale_factor
            # Criar tabela com duas imagens lado a lado
            fig_table_data = [[img1, img2]]
        else:
            # Criar tabela com apenas uma imagem e uma célula vazia
            fig_table_data = [[img1, ""]]

        # Criar a tabela para esta linha de imagens
        fig_table = Table(
            fig_table_data,
            colWidths=[3.7 * inch, 3.7 * inch],
            hAlign="CENTER",
            vAlign="MIDDLE",
        )
        fig_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        # Adicionar a tabela ao documento
        elements.append(fig_table)
        elements.append(Spacer(1, 20))

    # Análise e Recomendações
    elements.append(Paragraph("Análise e Recomendações", section_style))
    elements.append(Spacer(1, 10))

    # Saúde Financeira
    heading4_bold = ParagraphStyle(
        "Heading4Bold",
        parent=styles["Heading4"],
        fontName="Helvetica-Bold",
        italic=False,
    )
    elements.append(Paragraph("Saúde Financeira Atual", heading4_bold))

    # Usar estilo que processa tags HTML para o texto da saúde financeira
    elements.append(Paragraph(relatorio["saude_financeira"], html_style))
    elements.append(Spacer(1, 15))

    # Ineficiências com design melhorado
    elements.append(Paragraph("Principais Ineficiências", heading4_bold))
    elements.append(Spacer(1, 5))

    # Tabela de ineficiências
    for i, ineficiencia in enumerate(relatorio["ineficiencias"], 1):
        inef_title = ParagraphStyle(
            "InefTitle",
            parent=styles["Heading5"],
            textColor=colors.HexColor("#e74c3c"),
            fontName="Helvetica-Bold",
            italic=False,
        )
        elements.append(Paragraph(f"{i}. {ineficiencia['titulo']}", inef_title))
        # Limitar a largura do texto para evitar que saia da página
        desc_text = Paragraph(ineficiencia["descricao"], normal_style_wrapped)
        elements.append(desc_text)
        elements.append(Spacer(1, 5))

    # Recomendações com design aprimorado
    elements.append(Paragraph("Recomendações Práticas", heading4_bold))
    elements.append(Spacer(1, 10))

    # Adicionar cada recomendação como um bloco
    for i, recomendacao in enumerate(relatorio["recomendacoes"], 1):
        rec_title = ParagraphStyle(
            "RecTitle",
            parent=styles["Heading5"],
            textColor=colors.HexColor("#2ecc71"),
            fontName="Helvetica-Bold",
            italic=False,
        )
        elements.append(Paragraph(f"{i}. {recomendacao['titulo']}", rec_title))

        # Aplicar estilo com quebra de texto adequada para a descrição
        desc_text = Paragraph(recomendacao["descricao"], normal_style_wrapped)
        elements.append(desc_text)
        elements.append(Spacer(1, 5))

        # Modificar o estilo para incluir formatação HTML para negrito
        impact_data = [
            Paragraph(
                "<b>Impacto estimado: </b>" + recomendacao["impacto"], html_style
            ),
            Paragraph(
                "<b>Prazo sugerido para implementação: </b>" + recomendacao["prazo"],
                html_style,
            ),
        ]
        for p in impact_data:
            elements.append(p)
        elements.append(Spacer(1, 15))

        # Se não for o último elemento, adicionar quebra maior para separação
        if i < len(relatorio["recomendacoes"]):
            elements.append(Spacer(1, 10))

    # Rodapé com informações de contato
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#7f8c8d"),
        alignment=TA_CENTER,
    )

    elements.append(
        Paragraph(
            "Dog's Club - Conectando Pets e Cuidados com Simplicidade", footer_style
        )
    )
    elements.append(
        Paragraph("✉ suporte@dogsclub.com.br | ✆ (11) 9 9748-5353", footer_style)
    )
    elements.append(
        Paragraph(
            f"© {datetime.now().year} Dog's Club. Todos os direitos reservados.",
            footer_style,
        )
    )

    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
