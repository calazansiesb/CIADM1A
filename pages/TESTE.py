import streamlit as st

def main():
    st.set_page_config(layout="wide") # Define o layout da página como largo

    st.title("Trabalho Final - Introdução à Ciência de Dados")
    st.header("CIADM1A-CIA001-20251")

    st.write("---") # Linha horizontal para separar as seções

    st.subheader("Professor:")
    st.write("Alexandre Vaz Roriz")

    st.subheader("Alunos:")
    st.write("Diego Sá")
    st.write("Ewerton Calazans")

    st.write("---")

    st.markdown(
        """
        Este trabalho foi desenvolvido com base em um **dataset do IBGE de 2017 sobre avicultura**.
        Exploramos diversos aspectos da produção avícola no Brasil, utilizando técnicas de ciência de dados para extrair insights valiosos.
        """
    )

    st.markdown(
        """
        ### Para explorar os gráficos e análises, por favor, utilize o menu à esquerda.
        Lá você encontrará as seguintes seções:
        """
    )

    st.markdown(
        """
        - **Fatores que Mais Impactam a Lucratividade da Granja**: Uma análise dos elementos-chave que influenciam o desempenho financeiro das granjas avícolas.
        - **Matrizes Avícolas por Unidade Territorial**: Visualização e análise da distribuição das matrizes avícolas em diferentes regiões.
        - **Análise de Produção Avícola modelo de regressão**: Aplicação de modelos de regressão para entender e prever a produção avícola.
        - **Análise de Sistemas de Criação Avícola**: Um olhar sobre os diferentes sistemas de criação e suas características.
        """
    )

    st.info("Navegue pelo menu lateral para acessar cada tópico.")

if __name__ == "__main__":
    main()
