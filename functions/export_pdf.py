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
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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

    # Definir cores principais com base no tema atualizado
    AZUL_PRINCIPAL = colors.HexColor("#3498db")
    AZUL_SECUNDARIO = colors.HexColor("#2980b9")
    AZUL_ESCURO = colors.HexColor("#082f42")
    CINZA_TEXTO = colors.HexColor("#2c3e50")
    CINZA_CLARO = colors.HexColor("#f5f5f5")
    VERMELHO = colors.HexColor("#e74c3c")
    VERDE = colors.HexColor("#2ecc71")
    VERDE_ESCURO = colors.HexColor("#0a8a40")

    # Estilos aprimorados
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=26,
        spaceAfter=20,
        textColor=AZUL_ESCURO,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        italic=False,
    )
    subtitle_style = ParagraphStyle(
        "CustomSubTitle",
        parent=styles["Heading2"],
        fontSize=20,
        spaceAfter=15,
        textColor=CINZA_TEXTO,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        italic=False,
    )
    section_style = ParagraphStyle(
        "CustomSection",
        parent=styles["Heading3"],
        fontSize=16,
        spaceAfter=10,
        textColor=AZUL_PRINCIPAL,
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
        textColor=CINZA_TEXTO,
    )

    # Estilo para seção de ineficiências
    inefficiency_section_style = ParagraphStyle(
        "InefficiencySection",
        parent=section_style,
        textColor=VERMELHO,
        fontName="Helvetica-Bold",
        fontSize=16,
        alignment=TA_LEFT,
    )

    # Estilo para seção de recomendações
    recommendation_section_style = ParagraphStyle(
        "RecommendationSection",
        parent=section_style,
        textColor=VERDE_ESCURO,
        fontName="Helvetica-Bold",
        fontSize=16,
        alignment=TA_LEFT,
    )

    # Estilo para seção de prioridades
    priority_section_style = ParagraphStyle(
        "PrioritySection",
        parent=section_style,
        textColor=VERDE_ESCURO,
        fontName="Helvetica-Bold",
        fontSize=16,
        alignment=TA_LEFT,
    )

    # Estilo para seção de metas
    goal_section_style = ParagraphStyle(
        "GoalSection",
        parent=section_style,
        textColor=AZUL_PRINCIPAL,
        fontName="Helvetica-Bold",
        fontSize=16,
        alignment=TA_LEFT,
    )

    # Estilo que permite processamento de tags HTML
    html_style = ParagraphStyle(
        "HTMLStyle",
        parent=styles["Normal"],
        wordWrap="CJK",
        leading=14,
        textColor=CINZA_TEXTO,
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
            ParagraphStyle(
                "Date",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                textColor=CINZA_TEXTO,
            ),
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
                    AZUL_PRINCIPAL,
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
                    AZUL_PRINCIPAL,
                ),  # Linha mais grossa abaixo do cabeçalho
                ("ROUNDEDCORNERS", [10, 10, 10, 10]),
            ]
        )
    )
    elements.append(metrics_table)
    elements.append(Spacer(1, 25))

    # Potencial Não Aproveitado com design aprimorado
    potential_section_style = ParagraphStyle(
        "PotentialSection",
        parent=section_style,
        textColor=VERMELHO,
        fontName="Helvetica-Bold",
        fontSize=16,
    )
    elements.append(Paragraph("Potencial Não Aproveitado", potential_section_style))
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
                    VERMELHO,
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
                    VERMELHO,
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
            "Seu petshop está deixando de ganhar dinheiro devido à capacidade não utilizada.",
            ParagraphStyle(
                "RedAlert",
                parent=normal_style_wrapped,
                textColor=VERMELHO,
                fontName="Helvetica-Bold",
                fontSize=12,
            ),
        )
    )
    elements.append(Spacer(1, 15))

    # Adicionar gráficos se disponíveis
    if figuras and len(figuras) > 0:
        elements.append(Paragraph("Visualizações", section_style))
        elements.append(Spacer(1, 10))

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
            elements.append(Spacer(1, 15))

    # Principais Ineficiências
    elements.append(Paragraph("Principais Ineficiências", inefficiency_section_style))
    elements.append(Spacer(1, 10))

    # Criar tabela de ineficiências
    for i, ineficiencia in enumerate(relatorio["ineficiencias"]):
        elements.append(
            Paragraph(
                f"● {i+1}. {ineficiencia['titulo']}",
                ParagraphStyle(
                    "InefficiencyTitle",
                    parent=normal_style_wrapped,
                    textColor=VERMELHO,
                    fontName="Helvetica-Bold",
                    fontSize=12,
                    spaceBefore=10,
                    spaceAfter=2,
                ),
            )
        )
        elements.append(
            Paragraph(
                ineficiencia["descricao"],
                ParagraphStyle(
                    "InefficiencyDescription",
                    parent=normal_style_wrapped,
                    leftIndent=15,
                    textColor=CINZA_TEXTO,
                ),
            )
        )

    elements.append(Spacer(1, 20))

    # Recomendações práticas
    elements.append(Paragraph("Recomendações Práticas", recommendation_section_style))
    elements.append(Spacer(1, 10))

    # Parágrafos de recomendações
    for i, rec in enumerate(relatorio["recomendacoes"]):
        elements.append(
            Paragraph(
                f"✓ {i+1}. {rec['titulo']}",
                ParagraphStyle(
                    "RecommendationTitle",
                    parent=normal_style_wrapped,
                    textColor=VERDE_ESCURO,
                    fontName="Helvetica-Bold",
                    fontSize=12,
                    spaceBefore=10,
                    spaceAfter=2,
                ),
            )
        )
        elements.append(
            Paragraph(
                rec["descricao"],
                ParagraphStyle(
                    "RecommendationDescription",
                    parent=normal_style_wrapped,
                    leftIndent=15,
                    textColor=CINZA_TEXTO,
                ),
            )
        )

        # Adicionar impacto e prazo em parágrafos separados para melhor legibilidade
        elements.append(Spacer(1, 5))

        # Criar um estilo para impacto
        impact_style = ParagraphStyle(
            "ImpactStyle",
            parent=normal_style_wrapped,
            textColor=VERDE_ESCURO,
            fontName="Helvetica-Bold",
            fontSize=10,
            leftIndent=15,
            backgroundColor=colors.HexColor("#e8f8e8"),
            borderPadding=(5, 5, 5, 5),
            borderRadius=5,
        )

        # Criar um estilo para prazo
        deadline_style = ParagraphStyle(
            "DeadlineStyle",
            parent=normal_style_wrapped,
            textColor=AZUL_PRINCIPAL,
            fontName="Helvetica-Bold",
            fontSize=10,
            leftIndent=15,
            backgroundColor=colors.HexColor("#e3f2fd"),
            borderPadding=(5, 5, 5, 5),
            borderRadius=5,
        )

        # Adicionar impacto e prazo como parágrafos separados
        elements.append(Paragraph(f"IMPACTO: {rec['impacto']}", impact_style))

        elements.append(Spacer(1, 5))

        elements.append(Paragraph(f"PRAZO: {rec['prazo']}", deadline_style))

        elements.append(Spacer(1, 10))

    # Adicionar espaçamento após a seção de recomendações
    elements.append(Spacer(1, 20))

    # Prioridades de Curto Prazo
    elements.append(Paragraph("Prioridades de Curto Prazo", priority_section_style))
    elements.append(Spacer(1, 10))

    for i, prioridade in enumerate(relatorio["prioridades"]):
        elements.append(
            Paragraph(
                f"! {i+1}. {prioridade['titulo']}",
                ParagraphStyle(
                    "PriorityTitle",
                    parent=normal_style_wrapped,
                    textColor=VERDE_ESCURO,
                    fontName="Helvetica-Bold",
                    fontSize=12,
                    spaceBefore=10,
                    spaceAfter=2,
                ),
            )
        )
        elements.append(
            Paragraph(
                prioridade["descricao"],
                ParagraphStyle(
                    "PriorityDescription",
                    parent=normal_style_wrapped,
                    leftIndent=15,
                    textColor=CINZA_TEXTO,
                ),
            )
        )

    elements.append(Spacer(1, 20))

    # Metas Sugeridas
    elements.append(Paragraph("Metas Sugeridas", goal_section_style))
    elements.append(Spacer(1, 10))

    for i, meta in enumerate(relatorio["metas"]):
        elements.append(
            Paragraph(
                f"* {i+1}. {meta['titulo']}",
                ParagraphStyle(
                    "GoalTitle",
                    parent=normal_style_wrapped,
                    textColor=AZUL_PRINCIPAL,
                    fontName="Helvetica-Bold",
                    fontSize=12,
                    spaceBefore=10,
                    spaceAfter=2,
                ),
            )
        )
        elements.append(
            Paragraph(
                meta["descricao"],
                ParagraphStyle(
                    "GoalDescription",
                    parent=normal_style_wrapped,
                    leftIndent=15,
                    textColor=CINZA_TEXTO,
                ),
            )
        )

    elements.append(Spacer(1, 25))

    # Rodapé com informações de contato
    elements.append(
        Paragraph(
            """
            <para alignment="center">
            <font size="10" color="#7f8c8d">
            Para mais informações ou agendar uma consultoria gratuita, entre em contato conosco:
            </font>
            </para>
            """,
            html_style,
        )
    )
    elements.append(Spacer(1, 5))
    elements.append(
        Paragraph(
            f"""
            <para alignment="center">
            <font size="10" color="#3498db">
            <b>contato@dogsclub.com.br</b> | <b>www.dogsclub.com.br</b>
            </font>
            </para>
            """,
            html_style,
        )
    )
    elements.append(Spacer(1, 10))
    elements.append(
        Paragraph(
            """
            <para alignment="center">
            <font size="8" color="#7f8c8d">
            © 2025 Dog's Club. Todos os direitos reservados.
            </font>
            </para>
            """,
            html_style,
        )
    )

    # Construir o PDF
    doc.build(elements)

    # Obter o valor do buffer e retornar
    buffer.seek(0)
    return buffer
