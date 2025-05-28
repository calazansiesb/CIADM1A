import streamlit as st
import base64

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Análise Avícola - CIADM1A",
        page_icon="🐔",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS incorporado diretamente no código
    st.markdown("""
    <style>
    /* Estilos gerais */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Cards interativos */
    .custom-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        cursor: pointer;
        height: 100%;
        margin-bottom: 1rem;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Títulos */
    .custom-title {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .custom-subtitle {
        color: #7f8c8d;
        text-align: center;
        margin-top: 0;
    }
    
    /* Seções */
    .custom-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Dicas */
    .custom-tip {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #1976d2;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Cabeçalho com estilo aprimorado
    st.markdown("""
    <div style="padding:2rem;border-radius:10px;">
        <h1 class="custom-title">Trabalho Final - Introdução à Ciência de Dados</h1>
        <h3 class="custom-subtitle">CIADM1A-CIA001-20251</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    
    # Seção de informações da equipe
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="custom-section">
            <h3 style="color:#2c3e50;border-bottom:2px solid #f0f0f0;padding-bottom:10px;">Professor</h3>
            <div style="display:flex;align-items:center;margin-top:1rem;">
                <div style="margin-left:1rem;">
                    <p style="font-size:1.1rem;margin-bottom:0;">Alexandre Vaz Roriz</p>
                </div>
            </div>
            
            <h3 style="color:#2c3e50;border-bottom:2px solid #f0f0f0;padding-bottom:10px;margin-top:1.5rem;">Alunos</h3>
            <div style="display:flex;align-items:center;margin-top:1rem;">
                <div style="margin-left:1rem;">
                    <p style="font-size:1.1rem;margin-bottom:0.5rem;">Diego Sá</p>
                    <p style="font-size:1.1rem;margin-bottom:0;">Ewerton Calazans</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-section" style="height:100%;">
            <h3 style="color:#2c3e50;border-bottom:2px solid #f0f0f0;padding-bottom:10px;">Sobre o Trabalho</h3>
            <p style="font-size:1rem;line-height:1.6;">
                Este trabalho foi desenvolvido com base em um <strong>dataset do IBGE de 2017 sobre avicultura</strong>.
                Exploramos diversos aspectos da produção avícola no Brasil, utilizando técnicas de ciência de dados para extrair insights valiosos.
            </p>
            
            <div class="custom-tip">
                <p style="font-size:0.9rem;margin-bottom:0;">
                    <strong>💡 Dica:</strong> Navegue pelo menu lateral para acessar cada tópico da análise.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    
    # Seção de navegação com cards interativos
    st.markdown("""
    <h3 style="color:#2c3e50;margin-bottom:1rem;">Explore Nossas Análises</h3>
    <p style="font-size:1rem;margin-bottom:1.5rem;">Clique nos cards abaixo para navegar diretamente para cada seção</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <a href="/Fatores_Lucratividade" style="text-decoration:none;">
            <div class="custom-card">
                <h4 style="color:#2c3e50;margin-bottom:1rem;">📈 Fatores de Lucratividade</h4>
                <p style="color:#7f8c8d;font-size:0.9rem;">Análise dos elementos-chave que influenciam o desempenho financeiro</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <a href="/Matrizes_Avicolas" style="text-decoration:none;">
            <div class="custom-card">
                <h4 style="color:#2c3e50;margin-bottom:1rem;">🗺️ Matrizes Avícolas</h4>
                <p style="color:#7f8c8d;font-size:0.9rem;">Distribuição das matrizes avícolas por região</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <a href="/Modelo_Regressao" style="text-decoration:none;">
            <div class="custom-card">
                <h4 style="color:#2c3e50;margin-bottom:1rem;">🔮 Modelo de Regressão</h4>
                <p style="color:#7f8c8d;font-size:0.9rem;">Previsão da produção avícola usando regressão</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <a href="/Sistemas_Criacao" style="text-decoration:none;">
            <div class="custom-card">
                <h4 style="color:#2c3e50;margin-bottom:1rem;">🏭 Sistemas de Criação</h4>
                <p style="color:#7f8c8d;font-size:0.9rem;">Comparação entre diferentes sistemas de criação</p>
            </div>
        </a>
        """, unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("""
    <div style="margin-top:3rem;padding:1rem;text-align:center;color:#7f8c8d;font-size:0.9rem;">
        <p>Trabalho desenvolvido para a disciplina de Introdução à Ciência de Dados - 2025/1</p>
        <p>Dados: IBGE - Pesquisa da Pecuária Municipal 2017</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
