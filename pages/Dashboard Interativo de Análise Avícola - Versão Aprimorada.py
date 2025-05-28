import streamlit as st
from PIL import Image
import base64

# Configuração de estilo CSS personalizado
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Função para adicionar imagem de fundo
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-color: rgba(255, 255, 255, 0.9);
            background-blend-mode: lighten;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Análise Avícola - CIADM1A",
        page_icon="🐔",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Carregar estilos e imagens
    local_css("style.css")  # Crie um arquivo style.css com seus estilos personalizados
    # add_bg_from_local('background.jpg')  # Descomente se quiser uma imagem de fundo
    
    # Cabeçalho com estilo aprimorado
    st.markdown("""
    <div style="background-color:#f8f9fa;padding:2rem;border-radius:10px;box-shadow:0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="color:#2c3e50;text-align:center;margin-bottom:0.5rem;">Trabalho Final - Introdução à Ciência de Dados</h1>
        <h3 style="color:#7f8c8d;text-align:center;margin-top:0;">CIADM1A-CIA001-20251</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    
    # Seção de informações da equipe
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background-color:#ffffff;padding:1.5rem;border-radius:10px;box-shadow:0 2px 4px rgba(0,0,0,0.05);">
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
        <div style="background-color:#ffffff;padding:1.5rem;border-radius:10px;box-shadow:0 2px
