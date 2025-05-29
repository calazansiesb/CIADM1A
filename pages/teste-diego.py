# 1. CONFIGURAÇÃO DA PÁGINA - DEVE SER A PRIMEIRA LINHA EXECUTÁVEL
import streamlit as st
st.set_page_config(
    layout="wide",
    page_title="Análise de Galináceos",
    page_icon="🐔",
    initial_sidebar_state="expanded"
)

# 2. IMPORTAÇÕES (APÓS A CONFIGURAÇÃO DA PÁGINA)
import pandas as pd
import numpy as np
import plotly.express as px
import unicodedata

# 3. CARREGAMENTO DE DADOS COM TRATAMENTO DE ERRO ROBUSTO
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"
    try:
        # Tentativa com encoding mais comum primeiro
        df = pd.read_csv(url, sep=";", encoding="latin1")
    except UnicodeDecodeError:
        try:
            # Segunda tentativa com UTF-8
            df = pd.read_csv(url, sep=";", encoding="utf-8")
        except Exception as e:
            st.error(f"Falha crítica ao carregar dados: {str(e)}")
            st.stop()
    
    # Pré-processamento seguro
    numeric_cols = []
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                # Converter vírgulas para pontos em números
                df[col] = df[col].astype(str).str.replace(',', '.')
                # Tentar converter para numérico
                df[col] = pd.to_numeric(df[col], errors='ignore')
                if pd.api.types.is_numeric_dtype(df[col]):
                    numeric_cols.append(col)
            except Exception as e:
                st.warning(f"Não foi possível converter a coluna {col}: {str(e)}")
    
    return df, numeric_cols

# Carrega os dados
df, numeric_cols = load_data()

# 4. CONFIGURAÇÃO DA INTERFACE PRINCIPAL
st.title("🐔 Análise de Dados de Galináceos")
st.markdown("""
**Fonte:** IBGE - Pesquisa da Pecuária Municipal 2017  
**Dashboard interativo** para análise de estabelecimentos avícolas brasileiros
""")

# 5. DEFINIÇÃO DE ABAS
tab1, tab2 = st.tabs(["Análise Exploratória", "Correlações"])

with tab1:
    st.header("Exploração Interativa")
    
    # Seletores em colunas
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox(
            "Selecione a variável para o Eixo X:",
            options=numeric_cols,
            index=0,
            key='x_axis'
        )
    
    with col2:
        y_axis = st.selectbox(
            "Selecione a variável para o Eixo Y:",
            options=numeric_cols,
            index=1 if len(numeric_cols) > 1 else 0,
            key='y_axis'
        )
    
    # Gráfico de dispersão
    if x_axis and y_axis:
        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            hover_name="NOM_TERR" if "NOM_TERR" in df.columns else None,
            hover_data=numeric_cols,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Análise de Correlações")
    
    if len(numeric_cols) > 1:
        # Calcula matriz de correlação apenas com colunas numéricas
        corr_matrix = df[numeric_cols].corr()
        
        # Heatmap interativo
        fig = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="RdBu",
            aspect="auto",
            labels=dict(color="Correlação"),
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            height=700
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Número insuficiente de colunas numéricas para análise de correlação")

# 6. RODAPÉ
st.markdown("---")
st.caption("""
**Desenvolvido por:** CIADM1A - Análise de Dados  
**Atualizado em:** Junho 2025
""")
