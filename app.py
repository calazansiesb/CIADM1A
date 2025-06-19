import streamlit as st

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Análise Avícola - CIADM1A",
        page_icon="🐔",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS incorporado para estilização mínima
    st.markdown("""
    <style>
    .custom-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .highlight-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Cabeçalho
    st.title("Análise Exploratória do Dataset: Censo da Avicultura 2017 - IBGE")
    st.subheader("CIADM1A-CIA001-20251")
    
    # Divisor
    st.write("---")

    # Seção de informações da equipe
    col1, col2 = st.columns([1, 2])

    with col1:
        # Professor
        st.subheader("Professor:")
        st.markdown("""
        <div class="custom-card">
            Alexandre Vaz Roriz
        </div>
        """, unsafe_allow_html=True)
        
        # Alunos
        st.subheader("Alunos:")
        st.markdown("""
        <div class="custom-card">
            Diego Sá<br>
            Ewerton Calazans
        </div>
        """, unsafe_allow_html=True)

    # Introdução
    with st.expander("📌 Introdução"):
        st.markdown("""
        A avicultura desempenha um papel fundamental no setor agropecuário brasileiro, sendo uma das principais atividades econômicas ligadas à produção de proteína animal. Para compreender melhor os fatores que influenciam a produção avícola, este trabalho apresenta uma análise baseada no **dataset do IBGE de 2017 sobre avicultura**, explorando diferentes características do setor por meio de técnicas de ciência de dados.
        
        O objetivo principal é identificar padrões e tendências significativas que possam impactar a lucratividade, estrutura dos estabelecimentos e desempenho da produção. Para isso, foram formuladas **oito perguntas-chave**, abordando aspectos essenciais do conjunto de dados e possibilitando insights visuais por meio de gráficos e modelagens.

        ### **Entre os tópicos explorados, destacamos:**
        - 📈 **Fatores de Lucratividade** – Quais elementos têm maior impacto no desempenho financeiro dos estabelecimentos avícolas?
        - 🏢 **Dimensão do Estabelecimento** – Existe uma relação entre o tamanho do estabelecimento e o número de trabalhadores?
        - 📦 **Distribuição por Porte** – Como os diferentes portes de estabelecimentos estão distribuídos geograficamente?
        - 🗺️ **Matrizes Avícolas** – Qual é a concentração da produção de matrizes avícolas no Brasil?
        - 🔮 **Modelo de Regressão** – É possível prever a produção avícola com base em variáveis históricas?
        - 📊 **Análise da Pecuária** – Qual a representatividade dos galináceos na pecuária nacional?
        - 🔍 **Gráfico de Dispersão** – Quais métricas possuem correlação significativa dentro do conjunto de dados?
        - 🏭 **Sistemas de Criação** – Quais diferenças existem entre os sistemas de produção utilizados?

        Utilizando ferramentas como análise exploratória de dados, visualização gráfica e modelagem estatística, buscamos responder cada uma dessas questões, transformando números em **informações acionáveis** que possam agregar valor à compreensão do setor.

        Ao longo deste trabalho, os resultados serão organizados de forma clara e objetiva, permitindo que tendências relevantes sejam facilmente identificadas. Esperamos que esta análise contribua para uma visão aprofundada da avicultura brasileira e auxilie na tomada de decisões estratégicas para a otimização da produção.

        <div class="highlight-box">
            <p><strong>💡 Dica:</strong> Navegue pelo menu lateral para acessar cada tópico da análise.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Divisor
    st.write("---")
    
    # Seção de navegação
    st.subheader("Explore Nossas Análises")
    st.write("Selecione uma seção no menu lateral para visualizar as análises:")
    
    sections = [
        ("📈", "Fatores de Lucratividade", "Elementos que influenciam o desempenho financeiro"),
        ("🏢", "Dimensão do Estabelecimento", "Quantidade de Empregados"),
        ("📦", "Distribuição por Porte", "Estabelecimentos"),
        ("🗺️", "Matrizes Avícolas", "Distribuição por região"),
        ("🔮", "Modelo de Regressão", "Previsão da produção"),
        ("📊", "Análise da Pecuária", "Galináceos no Brasil"),
        ("🔍", "Gráfico de Dispersão", "Correlação entre Métricas"),
        ("🏭", "Sistemas de Criação", "Comparação entre sistemas")
    ]
    
    for i in range(0, len(sections), 4):
        cols = st.columns(4)
        for col, (icon, title, desc) in zip(cols, sections[i:i+4]):
            with col:
                st.markdown(f"""
                <div class="custom-card">
                    <h4>{icon} {title}</h4>
                    <p style="color:#7f8c8d; font-size:0.9em;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Rodapé
    st.write("---")
    st.caption("Trabalho desenvolvido para a disciplina de Introdução à Ciência de Dados - 2025/1")
    st.caption("Dados: IBGE - Pesquisa da Pecuária Municipal 2017")

if __name__ == "__main__":
    main()
