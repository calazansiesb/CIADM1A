import streamlit as st

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Análise Avícola - CIADM1A",
        page_icon="🐔",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Título e subtítulo
    st.title("Trabalho Final - Introdução à Ciência de Dados")
    st.subheader("CIADM1A-CIA001-20251")

    st.write("")
    st.write("")

    # Colunas para equipe e sobre o trabalho
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header("Professor")
        st.write("Alexandre Vaz Roriz")

        st.header("Alunos")
        st.write("- Diego Sá")
        st.write("- Ewerton Calazans")

    with col2:
        st.header("Sobre o Trabalho")
        st.write(
            "Este trabalho foi desenvolvido com base em um **dataset do IBGE de 2017 sobre avicultura**. "
            "Exploramos diversos aspectos da produção avícola no Brasil, utilizando técnicas de ciência de dados para extrair insights valiosos."
        )
        st.info("💡 Dica: Navegue pelo menu lateral para acessar cada tópico da análise.")

    st.write("")
    st.write("---")
    st.write("")

    st.header("Explore Nossas Análises")
    st.write("Clique nos botões abaixo para navegar diretamente para cada seção:")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📈 Fatores de Lucratividade"):
            st.session_state['page'] = 'Fatores_Lucratividade'
    with col2:
        if st.button("🗺️ Matrizes Avícolas"):
            st.session_state['page'] = 'Matrizes_Avicolas'
    with col3:
        if st.button("🔮 Modelo de Regressão"):
            st.session_state['page'] = 'Modelo_Regressao'
    with col4:
        if st.button("🏭 Sistemas de Criação"):
            st.session_state['page'] = 'Sistemas_Criacao'

    st.write("")
    st.write("---")
    st.write("")

    st.markdown(
        "<div style='text-align:center; color:#7f8c8d; font-size:0.9rem;'>"
        "Trabalho desenvolvido para a disciplina de Introdução à Ciência de Dados - 2025/1<br>"
        "Dados: IBGE - Pesquisa da Pecuária Municipal 2017"
        "</div>", unsafe_allow_html=True
    )

    # Navegação simulada (em produção, crie múltiplas páginas ou use st.experimental_rerun com session_state)
    if 'page' in st.session_state:
        if st.session_state['page'] == 'Fatores_Lucratividade':
            st.success("Página: Fatores de Lucratividade")
        elif st.session_state['page'] == 'Matrizes_Avicolas':
            st.success("Página: Matrizes Avícolas")
        elif st.session_state['page'] == 'Modelo_Regressao':
            st.success("Página: Modelo de Regressão")
        elif st.session_state['page'] == 'Sistemas_Criacao':
            st.success("Página: Sistemas de Criação")

if __name__ == "__main__":
    main()
