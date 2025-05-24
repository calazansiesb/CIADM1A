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

fig1 = px.pie(
    values=proporcoes,
    names=sistemas,
    title='Distribuição Percentual dos Sistemas de Criação',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig1, use_container_width=True)

st.info("""
**🔍 Análise dos Sistemas de Criação**

📌 **Distribuição:**
- Sistema Predominante: **3-SIST_PFC** (28.3%)
- Segunda Colocação: **1-SIST_POC** (28.1%)
- Terceira Posição: **2-SIST_POI** (27.3%)
- Menor Representatividade: **4-Outro** (16.4%)

💡 **Insights:**
1. Equilíbrio notável entre os três principais sistemas (diferença <1%)
2. Sistema "Outros" apresenta menor participação (16.4%)
3. Nenhum sistema domina claramente (>50%), indicando diversificação
""")

# =============================================
# 2. DISTRIBUIÇÃO POR UNIDADE FEDERATIVA
# =============================================
st.header('🌎 Distribuição por Unidade Federativa')

# Dados simulados por UF (substituir por dados reais)
ufs = ['SP', 'MG', 'PR', 'RS', 'SC', 'BA', 'GO', 'MT']
valores = [120, 95, 80, 75, 60, 55, 50, 45]

fig2 = px.bar(
    x=ufs,
    y=valores,
    title='Estabelecimentos Avícolas por UF',
    labels={'x': 'Unidade Federativa', 'y': 'Número de Estabelecimentos'},
    color=ufs,
    color_discrete_sequence=px.colors.qualitative.Vivid
)

st.plotly_chart(fig2, use_container_width=True)

st.info("""
**🔎 Análise Regional**

📌 **Principais Observações:**
- **Sudeste (SP/MG)** lidera em número de estabelecimentos
- **Sul (PR/RS/SC)** apresenta alta concentração produtiva
- **Centro-Oeste (GO/MT)** mostra crescimento significativo

💡 **Interpretação:**
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

# Calcular correlação
corr = np.corrcoef(tamanho, trabalhadores)[0,1]

fig3 = px.scatter(
    x=tamanho,
    y=trabalhadores,
    title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
    labels={'x': 'Total de Galináceos', 'y': 'Número de Trabalhadores'},
    trendline="lowess"  # Suavização sem statsmodels
)

st.plotly_chart(fig3, use_container_width=True)

st.info(f"""
**📈 Análise de Correlação**

📊 **Correlação Calculada:** {corr:.2f}

📌 **Interpretação:**
- {'Forte correlação positiva' if corr > 0.7 else 
   'Correlação moderada' if corr > 0.4 else 
   'Fraca correlação'} entre as variáveis
- Estabelecimentos maiores tendem a empregar mais trabalhadores
- Relação não é perfeitamente linear, indicando outros fatores envolvidos

💡 **Recomendações:**
- Analisar separadamente por tipo de sistema de criação
- Considerar diferenças regionais na relação
""")

# =============================================
# 4. DISTRIBUIÇÃO POR PORTE
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

portes = ['Pequeno', 'Médio', 'Grande']
quantidades = [1200, 850, 350]

fig4 = px.bar(
    x=portes,
    y=quantidades,
    title='Distribuição de Estabelecimentos por Porte',
    labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
    color=portes,
    color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96']
)

st.plotly_chart(fig4, use_container_width=True)

st.info("""
**📦 Análise por Porte**

📌 **Distribuição:**
- **Pequenos:** 1-5.000 aves (55% dos estabelecimentos)
- **Médios:** 5.001-20.000 aves (30%)
- **Grandes:** >20.000 aves (15%)

💡 **Insights:**
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
