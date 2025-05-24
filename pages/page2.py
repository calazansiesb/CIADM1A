import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Análise de Matrizes Avícolas - IBGE",
    page_icon="🐣",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Matrizes Avícolas por Unidade Territorial')
st.markdown("---")

# Carregar dados
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
    df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()
    df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce').fillna(0)
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

# Listas de regiões
regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
df_estados = df[~df['NOM_TERR'].isin(regioes + ['Brasil'])].copy()
df_regioes = df[df['NOM_TERR'].isin(regioes)].copy()

# =============================================
# 1. GRÁFICO DE BARRAS - MATRIZES POR ESTADO
# =============================================
st.header('📊 Distribuição de Matrizes por Estado')

if not df_estados.empty:
    # Processamento dos dados
    matrizes_por_estado = df_estados.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum()
    matrizes_por_estado = matrizes_por_estado.sort_values('GAL_MATR', ascending=False)
    
    # Gráfico interativo
    fig1 = px.bar(
        matrizes_por_estado,
        x='NOM_TERR',
        y='GAL_MATR',
        title='Total de Matrizes por Estado',
        labels={'NOM_TERR': 'Estado', 'GAL_MATR': 'Número de Matrizes'},
        color='GAL_MATR',
        color_continuous_scale='Oranges'
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.info("""
    **🔍 Análise por Estado**
    
    📌 **Principais observações:**
    - Estados com maior concentração de matrizes avícolas
    - Disparidades regionais na distribuição
    - Potenciais polos de produção
    
    💡 **Interpretação:**
    - Distribuição reflete a infraestrutura produtiva de cada estado
    - Concentração em regiões com tradição avícola
    - Oportunidades para expansão em estados menos representados
    """)
else:
    st.warning("Não há dados disponíveis para os estados.")

# =============================================
# 2. GRÁFICO DE PIZZA - MATRIZES POR REGIÃO
# =============================================
st.header('🌎 Distribuição Regional de Matrizes')

if not df_regioes.empty:
    # Processamento dos dados
    matrizes_por_regiao = df_regioes.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum()
    matrizes_por_regiao['Porcentagem'] = (matrizes_por_regiao['GAL_MATR'] / matrizes_por_regiao['GAL_MATR'].sum()) * 100
    
    # Gráfico interativo
    fig2 = px.pie(
        matrizes_por_regiao,
        values='GAL_MATR',
        names='NOM_TERR',
        title='Proporção de Matrizes por Região',
        color_discrete_sequence=px.colors.sequential.Oranges,
        hover_data=['Porcentagem'],
        labels={'NOM_TERR': 'Região', 'GAL_MATR': 'Matrizes'}
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("""
    **🔍 Análise por Região**
    
    📌 **Principais observações:**
    - Nordeste lidera com 40,2% das matrizes avícolas do Brasil
    - Centro-Oeste é o segundo maior polo, com 30,7%
    - Sul, Norte e Sudeste têm participações menores (11,4%, 9,89% e 7,95%)
    
    💡 **Interpretação:**
    - Forte concentração da produção de matrizes nas regiões Nordeste e Centro-Oeste
    - Distribuição pode estar relacionada à disponibilidade de áreas, clima e incentivos regionais
    - Indica necessidade de estratégias regionais para o desenvolvimento do setor
    """)
else:
    st.warning("Não há dados disponíveis para as regiões.")

# =============================================
# 3. GRÁFICO ADICIONAL - SISTEMAS DE CRIAÇÃO
# =============================================
st.header('🏭 Sistemas de Criação por Região')

if 'SIST_CRIA' in df.columns and not df_regioes.empty:
    # Processamento dos dados
    sistemas_por_regiao = df_regioes.groupby(['NOM_TERR', 'SIST_CRIA'])['GAL_MATR'].sum().reset_index()
    
    # Gráfico interativo
    fig3 = px.bar(
        sistemas_por_regiao,
        x='NOM_TERR',
        y='GAL_MATR',
        color='SIST_CRIA',
        title='Sistemas de Criação por Região',
        labels={'NOM_TERR': 'Região', 'GAL_MATR': 'Matrizes', 'SIST_CRIA': 'Sistema de Criação'},
        barmode='group'
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    st.info("""
    **📌 Legenda dos Sistemas:**
    - 1-SIST_POC: Produtores de ovos para consumo
    - 2-SIST_POI: Produtores de ovos para incubação
    - 3-SIST_PFC: Produtores de frangos de corte
    - 4-Outro: Outros sistemas de produção
    
    **💡 Análise:**
    - Sistemas predominantes em cada região
    - Variações regionais nos tipos de produção
    - Especialização regional
    """)

# Rodapé
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base nos dados do IBGE*  
📅 *Atualizado em Outubro 2023*  
""")
