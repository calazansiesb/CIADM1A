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
    </style>
    """, unsafe_allow_html=True)
    
    # Cabeçalho
    st.title("Trabalho Final - Introdução à Ciência de Dados")
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
    
    with col2:
        # Sobre o trabalho
        st.subheader("Sobre o Trabalho")
        st.markdown("""
        <div class="custom-card">
            <p>Este trabalho foi desenvolvido com base em um <strong>dataset do IBGE de 2017 sobre avicultura</strong>.
            Exploramos diversos aspectos da produção avícola no Brasil, utilizando técnicas de ciência de dados para extrair insights valiosos.</p>
            
            <div style="background-color:#e3f2fd; padding:1rem; border-radius:8px; margin-top:1rem;">
                <p style="margin:0;"><strong>💡 Dica:</strong> Navegue pelo menu lateral para acessar cada tópico da análise.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Divisor
    st.write("---")
    
    # Seção de navegação
    st.subheader("Explore Nossas Análises")
    st.write("Selecione uma seção no menu lateral para visualizar as análises:")
    
    cols = st.columns(4)
    sections = [
        ("📈", "Fatores de Lucratividade", "Elementos que influenciam o desempenho financeiro"),
        ("🗺️", "Matrizes Avícolas", "Distribuição por região"),
        ("🔮", "Modelo de Regressão", "Previsão da produção"),
        ("🏭", "Sistemas de Criação", "Comparação entre sistemas"),
        ("📊", "Análise da Pecuária", "Galináceos no Brasil"),
        ("🔍", "Gráfico de Dispersão", "Correlação entre Métricas"),
        ("🏢", "Dimensão do Estabelecimento", "Quantidade de Empregados"),
        ("📦", "Distribuição por Porte", "Estabelecimentos")
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
