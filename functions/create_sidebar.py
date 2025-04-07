import streamlit as st


def create_sidebar():
    """Cria a barra lateral com informações e links úteis"""
    st.sidebar.image(
        "https://dogs-club-source.s3.us-east-1.amazonaws.com/logo.png",
        width=200,
    )

    st.sidebar.markdown("## Sobre a Dog's Club")
    st.sidebar.markdown(
        """
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 10px;">
        A Dog's Club é uma plataforma inovadora que revoluciona a forma como tutores de pets e pet shops se conectam.
        
        Nossa missão é facilitar a vida de quem ama seus pets, eliminando a frustração de telefonemas, mensagens de WhatsApp e agendamentos confusos.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("## Como usar a ferramenta")
    st.sidebar.markdown(
        """
    <div style="margin-left: 10px;">
        <ol>
            <li><b>Preencha</b> os dados do seu petshop nos formulários</li>
            <li><b>Analise</b> os resultados e visualizações</li>
            <li><b>Receba</b> recomendações personalizadas</li>
            <li><b>Exporte</b> o relatório em PDF</li>
        </ol>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("## Contato")
    st.sidebar.markdown(
        """
    <div style="background-color: #f0f7fb; padding: 15px; border-radius: 8px; border-left: 3px solid #3498db;">
        <p><b>📧 suporte@dogsclub.com.br</b></p>
        <p><b>📱 (11) 99748-5353</b></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Botão para iniciar uma nova análise
    if st.sidebar.button("Iniciar Nova Análise", type="primary"):
        st.session_state.current_page = "form"
        st.rerun()
