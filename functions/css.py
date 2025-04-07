import streamlit as st


# Configuração adicional para forçar o tema branco
def define_css():
    st.markdown(
        """
    <style>
        /* Oculta o seletor de tema no menu */
        #MainMenu {visibility: hidden;}
        [data-testid="collapsedControl"] {display: none}
        
        /* Força o tema claro */
        .stApp {
            background-color: white;
        }
        
        /* Remove opção de mudar tema */
        [data-testid="collapsedControl"] .css-hxt7ib {
            display: none;
        }
        
        /* Forçando tema claro permanentemente */
        [data-testid="stAppViewContainer"] {
            background-color: white;
        }
        
        /* Desabilitar botão de tema escuro */
        button[title="View fullscreen"], button[data-testid="dark-theme-button"] {
            display: none;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Adicionar CSS personalizado aprimorado
    st.markdown(
        """
    <style>
        body {
            font-family: 'Roboto', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #2c3e50;
        }
        .main-header {
            font-size: 2.5rem;
            color: #3498db;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
        }
        .section-header {
            font-size: 1.8rem;
            color: #3498db;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #f0f0f0;
            font-weight: 500;
        }
        .form-caption {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            color: #2c3e50;
            border-left: 4px solid #3498db;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .progress-container {
            margin: 25px 0;
        }
        .stProgress > div > div {
            background-color: #3498db;
        }
        /* Estilização para todos os botões (padrão) */
        .stButton > button {
            width: 100%;
            border-radius: 6px;
            font-weight: 500;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
            border: none;
            background-color: #3498db;
            color: white;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background-color: #2980b9;
        }
        /* Estilização para botões primários em azul */
        .stButton > button[kind="primary"] {
            background-color: #3498db;
            color: white;
        }
        .stButton > button[kind="primary"]:hover {
            background-color: #2980b9;
        }
        /* Estilização para botões secundários - agora também azuis com texto branco */
        .stButton > button[kind="secondary"] {
            background-color: #3498db;
            color: white;
            border: 1px solid #2980b9;
        }
        .stButton > button[kind="secondary"]:hover {
            background-color: #2980b9;
        }
        /* Estilização aprimorada de sliders */
        .stSlider [data-baseweb="slider"] div div div div {
            background-color: #3498db;
        }
        .stSlider [data-baseweb="slider"] div div div {
            background-color: rgba(52, 152, 219, 0.3);
        }
        .stSlider [data-baseweb="slider"] [role="slider"] {
            background-color: #3498db;
            border-color: #3498db;
        }
        /* Melhorias para os sliders */
        .stSlider [data-baseweb="slider"] {
            height: 8px;
        }
        .stSlider [data-baseweb="slider"] [role="slider"] {
            width: 18px;
            height: 18px;
            top: -5px;
        }
        /* Cor do texto do slider e números */
        .stSlider label, .stSlider p, .stSlider span {
            color: #3498db !important;
        }
        /* Ajustar valores mínimo/máximo para evitar sobreposição com botões */
        .stSlider [data-baseweb="slider"] [data-testid="stTickBarMin"],
        .stSlider [data-baseweb="slider"] [data-testid="stTickBarMax"] {
            color: #3498db !important;
        }
        /* Adicionar margem inferior nos sliders para evitar sobreposição com botões */
        .stSlider {
            margin-bottom: 40px !important;
            padding-bottom: 20px !important;
            position: relative;
        }
        .stSlider [data-baseweb="slider"] {
            margin-bottom: 30px !important;
        }
        /* Melhorar espaçamento entre componentes */
        .row-widget {
            margin-bottom: 25px !important;
        }
        /* Evitar que ícones vermelhos apareçam com cor incorreta */
        [data-testid="stImage"] {
            z-index: 1;
        }
        /* Estilização de radio buttons, checkboxes e selectboxes */
        .stRadio label span span:first-child,
        .stCheckbox label span span:first-child {
            background-color: #3498db;
            border-color: #3498db;
        }
        /* Uniformização dos textos de radio buttons e checkboxes */
        .stRadio label, .stCheckbox label {
            color: #3498db !important;
            font-weight: 500 !important;
        }
        /* Uniformização dos selectboxes */
        .stSelectbox [data-baseweb="select"] {
            background-color: #3498db;
            color: white;
            border-radius: 6px;
            border: none;
        }
        .stSelectbox [data-baseweb="select"] div, 
        .stSelectbox [data-baseweb="select"] span {
            color: white;
        }
        .stSelectbox [data-baseweb="select"]:hover {
            background-color: #2980b9;
        }
        .navigation-button {
            margin-top: 25px;
        }
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.8rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 1.5rem;
            border: 1px solid #f0f0f0;
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        }
        .metric-label {
            font-size: 1.1rem;
            color: #7f8c8d;
            margin-bottom: 0.7rem;
            font-weight: 500;
        }
        .metric-value {
            font-size: 2rem;
            color: #2c3e50;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .metric-subvalue {
            font-size: 1.2rem;
            color: #7f8c8d;
            font-weight: 400;
        }
        .highlight-card {
            background-color: #fff8f8;
            border-left: 5px solid #e74c3c;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .contact-card {
            background-color: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #3498db;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .footer {
            text-align: center;
            margin-top: 4rem;
            padding: 1.5rem;
            border-top: 1px solid #f0f0f0;
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        .help-text {
            color: #7f8c8d;
            font-size: 0.9rem;
            font-style: italic;
            margin-top: 5px;
            background-color: #fafafa;
            padding: 8px 12px;
            border-radius: 4px;
        }
        .submit-button {
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 25px;
            transition: all 0.3s ease;
        }
        .submit-button:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }
        input[type="text"], input[type="number"], textarea, select {
            border-radius: 6px !important;
            border: 1px solid #e0e0e0 !important;
            padding: 10px !important;
            transition: all 0.3s ease;
        }
        input[type="text"]:focus, input[type="number"]:focus, textarea:focus, select:focus {
            border-color: #3498db !important;
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2) !important;
        }
        /* Estilo para o botão de exportar PDF */
        .pdf-button {
            background-color: #3498db;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 12px 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            width: 100%;
            transition: all 0.3s ease;
        }
        .pdf-button:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }
        /* Estilo para tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            border-radius: 6px 6px 0 0;
            background-color: #3498db;
            color: white;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2980b9;
            font-weight: 600;
            color: white;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <style>
        :root {
            --background-color: #ffffff;
            --secondary-background-color: #f0f2f6;
            --text-color: #31333F;
            --font: "Source Sans Pro", sans-serif;
        }
        
        /* Impedir que o tema escuro seja usado */
        [data-testid="stSidebar"] .css-sg054d {
            display: none;
        }
        
        /* Certificar que o texto permaneça escuro */
        body {
            color: #31333F;
            background-color: #ffffff;
        }
        
        .stApp {
            background-color: #ffffff;
        }
        
        /* Melhorias adicionais para negrito em textos */
        b {
            font-weight: 600;
        }
        
        /* Substitua todas as cores vermelhas por azul em todo o sistema */
        h2, h3, h4 {
            color: #3498db !important;
        }
        
        /* Exceções para as cores das ineficiências e recomendações */
        h4[style*="color: #e74c3c"], [style*="color: #e74c3c"] {
            color: #e74c3c !important;
        }
        
        h4[style*="color: #2ecc71"], [style*="color: #2ecc71"], [style*="color: #27ae60"] {
            color: #2ecc71 !important;
        }
        
        /* Garantir que a seção "Potencial Não Aproveitado" e seus componentes apareçam em vermelho */
        .section-header[style*="color: #e74c3c"] {
            color: #e74c3c !important;
            font-weight: 700 !important;
        }
        
        h3[style*="color: #e74c3c"], h2[style*="color: #e74c3c"] {
            color: #e74c3c !important;
        }
        
        /* Efeitos de alerta para a seção de prejuízo */
        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }
            100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
        }
        
        [style*="background-color: #fdf2f2"] {
            animation: pulse-red 2s infinite;
        }
        
        /* Efeito de destaque para o alerta principal vermelho */
        [style*="background-color: #e74c3c"] {
            box-shadow: 0 4px 8px rgba(231, 76, 60, 0.4);
            transform: scale(1.02);
            transition: all 0.3s ease;
            margin: 25px auto !important;
            color: white !important;
        }
        
        /* Garantir que qualquer texto dentro do alerta vermelho seja branco */
        [style*="background-color: #e74c3c"] * {
            color: white !important;
        }
        
        /* Adicionar um pouco de espaço entre os elementos para melhor legibilidade */
        [style*="color: #e74c3c; margin-top: 0;"] {
            margin-bottom: 10px !important;
        }
        
        /* Deixar valores grandes mais impactantes */
        h2[style*="font-weight: 800; font-size: 2.5rem"] {
            margin: 10px 0 !important;
        }
        
        /* Garantir cor verde para o título "Recomendações Práticas" */
        h3 span[style*="color: #2ecc71"] {
            color: #2ecc71 !important;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
