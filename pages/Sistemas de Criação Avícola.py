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
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado. Por favor, certifique-se de que o arquivo está no mesmo diretório da aplicação.")
    st.stop()

# =============================================
# ✨ NOVIDADE: Mapeamento e Limpeza da coluna SIST_CRIA
# =============================================
if 'SIST_CRIA' in df.columns:
    # Limpar espaços em branco e garantir que é string antes de mapear
    df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()

    # Dicionário de mapeamento das abreviações para descrições completas
    mapeamento_sistemas = {
        '1-SIST_POC': 'Produtores de ovos para consumo',
        '2-SIST_POI': 'Produtores de ovos para incubação',
        '3-SIST_PFC': 'Produtores de frangos de corte',
        '4-Outro': 'Outros produtores'
    }
    
    # Aplicar o mapeamento
    df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)
    
else:
    st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset. Verifique o nome da coluna.")

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
    
    # Adicionado st.expander para a interpretação do gráfico de barras
    with st.expander("💡 Interpretação do Gráfico de Barras"):
        st.markdown("""
        **🔍 Análise por Estado**
        
        📌 **Principais observações:**
        - **Mato Grosso do Sul** e **Pernambuco** lideram em número absoluto de matrizes avícolas.
        - **Distrito Federal** e **Pará** também apresentam valores expressivos, compondo o grupo dos quatro estados com maior concentração.
        - A distribuição é bastante desigual, com alguns estados apresentando números significativamente mais baixos.
        
        💡 **Interpretação:**
        - A concentração de matrizes em poucos estados pode refletir fatores como infraestrutura, tradição produtiva e incentivos regionais.
        - Estados do **Centro-Oeste** e **Nordeste** se destacam como polos importantes na produção de matrizes.
        - Estados com menor número de matrizes podem representar oportunidades para crescimento e investimento no setor avícola.
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
    
    # Adicionado st.expander para a interpretação do gráfico de pizza
    with st.expander("💡 Interpretação do Gráfico de Pizza"):
        st.info("""
        **🔍 Análise por Região**
        
        📌 **Principais observações:**
        - **Nordeste** lidera com **40,2%** das matrizes avícolas do Brasil.
        - **Centro-Oeste** é o segundo maior polo, com **30,7%**.
        - Sul, Norte e Sudeste têm participações menores (11,4%, 9,89% e 7,95%).
        
        💡 **Interpretação:**
        - Forte concentração da produção de matrizes nas regiões **Nordeste** e **Centro-Oeste**.
        - A distribuição pode estar relacionada à disponibilidade de áreas, clima e incentivos regionais.
        - Indica a necessidade de estratégias regionais para o desenvolvimento do setor.
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
        color='SIST_CRIA', # Esta coluna agora terá os nomes completos
        title='Sistemas de Criação por Região',
        labels={'NOM_TERR': 'Região', 'GAL_MATR': 'Matrizes', 'SIST_CRIA': 'Sistema de Criação'},
        barmode='group'
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # Adicionado st.expander para a interpretação do gráfico de sistemas de criação
    with st.expander("💡 Interpretação dos Sistemas de Criação por Região"):
        st.info("""
        **🔍 Análise por Região — Sistemas de Criação**

        📌 **Principais observações:**
        - O sistema de produção de ovos para consumo (**Produtores de ovos para consumo**) é predominante no **Centro-Oeste**, **Nordeste** e **Sul**.
        - O **Nordeste** apresenta a maior quantidade de matrizes, especialmente no sistema **Produtores de ovos para consumo**, seguido por relevante participação do sistema **Produtores de frangos de corte**.
        - O **Sudeste** e o **Norte** possuem menor representatividade, com destaque para o Sudeste na produção de frangos de corte.
        - Baixa expressão dos sistemas **Produtores de ovos para incubação** e **Outros produtores** em todas as regiões.

        💡 **Interpretação:**
        - Há especialização regional nos sistemas de criação, com o **Centro-Oeste** e **Nordeste** se destacando na produção de ovos e o **Sudeste** e **Sul** mostrando variações nos tipos de produção.
        - As diferenças refletem fatores como tradição produtiva, demanda de mercado e adequação das condições regionais.
        - Os resultados indicam a necessidade de estratégias regionais para aprimorar a competitividade e a sustentabilidade do setor avícola.
        """)
else:
    st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset ou não há dados para regiões.")

# Rodapé
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base nos dados do IBGE* 📅 *Atualizado em Outubro 2023* """)
