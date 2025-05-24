import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola Brasileira - IBGE 2017",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Análise de Galináceos no Brasil (IBGE 2017)')
st.markdown("---")

# =============================================
# 1. PROPORÇÃO DOS SISTEMAS DE CRIAÇÃO
# =============================================
st.header('📊 Proporção dos Sistemas de Criação')

# Dados simulados (substituir por dados reais se necessário)
sistemas = ['3-SIST_PFC', '1-SIST_POC', '2-SIST_POI', '4-Outro']
proporcoes = [28.3, 28.1, 27.3, 16.4]

# Sidebar para seleção de dados
st.sidebar.header("Configurações da Análise")
show_raw_data = st.sidebar.checkbox("Mostrar dados brutos", False)

if show_raw_data:
    st.subheader("Dados Brutos")
    df_sistemas = pd.DataFrame({
        'Sistema': sistemas,
        'Proporção (%)': proporcoes
    })
    st.dataframe(df_sistemas)

fig1 = px.pie(
    values=proporcoes,
    names=sistemas,
    title='Distribuição Percentual dos Sistemas de Criação',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig1, use_container_width=True)

# Análise expandível
with st.expander("🔍 Análise dos Sistemas de Criação"):
    st.markdown("""
    **📌 Distribuição:**
    - Sistema Predominante: **Produtores de frangos de corte (3-SIST_PFC)** - 28.3%
    - Segunda Colocação: **Produtores de ovos para consumo (1-SIST_POC)** - 28.1%
    - Terceira Posição: **Produtores de ovos para incubação (2-SIST_POI)** - 27.3%
    - Menor Representatividade: **Outros produtores (4-Outro)** - 16.4%

    **💡 Insights:**
    1. Equilíbrio notável entre os três principais sistemas produtivos (diferença <1%)
    2. Sistemas alternativos ("Outros produtores") apresentam menor participação (16.4%)
    3. Nenhum sistema domina claramente (>50% do total), indicando:
       - Diversificação da produção avícola nacional
       - Pluralidade de modelos de criação
       - Oportunidades para nichos específicos
    """)

# =============================================
# 2. DISTRIBUIÇÃO POR UNIDADE FEDERATIVA
# =============================================
st.header('🌎 Distribuição por Unidade Federativa')

# Dados simulados por UF (substituir por dados reais)
ufs = ['SP', 'MG', 'PR', 'RS', 'SC', 'BA', 'GO', 'MT']
valores = [120, 95, 80, 75, 60, 55, 50, 45]

# Widget de seleção de visualização
vis_type = st.sidebar.radio(
    "Tipo de visualização para UFs:",
    ("Barras", "Pizza", "Treemap")
)

if vis_type == "Barras":
    fig2 = px.bar(
        x=ufs,
        y=valores,
        title='Estabelecimentos Avícolas por UF',
        labels={'x': 'Unidade Federativa', 'y': 'Número de Estabelecimentos'},
        color=ufs,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
elif vis_type == "Pizza":
    fig2 = px.pie(
        values=valores,
        names=ufs,
        title='Distribuição Percentual por UF'
    )
else:
    fig2 = px.treemap(
        names=ufs,
        parents=['']*len(ufs),
        values=valores,
        title='Distribuição Hierárquica por UF'
    )

st.plotly_chart(fig2, use_container_width=True)

# Análise expandível
with st.expander("🔎 Análise Regional"):
    st.markdown("""
    **📌 Principais Observações:**
    - **Sudeste (SP/MG)** lidera em número de estabelecimentos
    - **Sul (PR/RS/SC)** apresenta alta concentração produtiva
    - **Centro-Oeste (GO/MT)** mostra crescimento significativo

    **💡 Interpretação:**
    - Distribuição reflete fatores históricos e logísticos
    - Concentração segue padrões de desenvolvimento regional
    - Dados justificam políticas diferenciadas por região
    """)

# =============================================
# 3. RELAÇÃO TAMANHO × TRABALHADORES
# =============================================
st.header('👥 Relação: Tamanho × Número de Trabalhadores')

# Gerar dados simulados
np.random.seed(42)
tamanho = np.random.randint(1000, 50000, 100)
trabalhadores = tamanho/1000 * np.random.uniform(5, 15, 100)

# Widget para selecionar tipo de gráfico
scatter_type = st.sidebar.selectbox(
    "Tipo de visualização para correlação:",
    ("Scatter Plot", "Linha", "Área")
)

if scatter_type == "Scatter Plot":
    fig3 = px.scatter(
        x=tamanho,
        y=trabalhadores,
        title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
        labels={'x': 'Total de Galináceos', 'y': 'Número de Trabalhadores'},
        trendline="lowess"
    )
elif scatter_type == "Linha":
    fig3 = px.line(
        x=tamanho,
        y=trabalhadores,
        title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
        labels={'x': 'Total de Galináceos', 'y': 'Número de Trabalhadores'}
    )
else:
    fig3 = px.area(
        x=tamanho,
        y=trabalhadores,
        title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
        labels={'x': 'Total de Galináceos', 'y': 'Número de Trabalhadores'}
    )

st.plotly_chart(fig3, use_container_width=True)

# Cálculo da correlação
corr = np.corrcoef(tamanho, trabalhadores)[0,1]

# Análise expandível
with st.expander("📈 Análise de Correlação"):
    st.markdown(f"""
    **📊 Correlação Calculada:** {corr:.2f}

    **📌 Interpretação:**
    - {'Forte correlação positiva' if corr > 0.7 else 
       'Correlação moderada' if corr > 0.4 else 
       'Fraca correlação'} entre as variáveis
    - Estabelecimentos maiores tendem a empregar mais trabalhadores
    - Relação não é perfeitamente linear, indicando outros fatores envolvidos

    **💡 Recomendações:**
    - Analisar separadamente por tipo de sistema de criação
    - Considerar diferenças regionais na relação
    """)

# =============================================
# 4. DISTRIBUIÇÃO POR PORTE
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

portes = ['Pequeno', 'Médio', 'Grande']
quantidades = [1200, 850, 350]

# Widget para selecionar cores
color_scheme = st.sidebar.selectbox(
    "Esquema de cores para portes:",
    ("Padrão", "Vermelho/Verde/Azul", "Pastel")
)

if color_scheme == "Padrão":
    colors = ['#636EFA', '#EF553B', '#00CC96']
elif color_scheme == "Vermelho/Verde/Azul":
    colors = ['#FF0000', '#00FF00', '#0000FF']
else:
    colors = px.colors.qualitative.Pastel[:3]

fig4 = px.bar(
    x=portes,
    y=quantidades,
    title='Distribuição de Estabelecimentos por Porte',
    labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
    color=portes,
    color_discrete_sequence=colors
)

st.plotly_chart(fig4, use_container_width=True)

# Análise expandível
with st.expander("📦 Análise por Porte"):
    st.markdown("""
    **📌 Distribuição:**
    - **Pequenos:** 1-5.000 aves (55% dos estabelecimentos)
    - **Médios:** 5.001-20.000 aves (30%)
    - **Grandes:** >20.000 aves (15%)

    **💡 Insights:**
    - Maioria dos estabelecimentos são de pequeno porte
    - Estabelecimentos grandes concentram maior volume de produção
    - Necessidade de políticas diferenciadas por porte
    """)

# Rodapé
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base em dados simulados do IBGE 2017*  
📅 *Atualizado em Outubro 2023*  
""")
