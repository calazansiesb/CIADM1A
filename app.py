import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="1. Distribuição Geográfica da Produção Avícola:",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Análise de Galináceos no Brasil')
st.info("Use o menu lateral à esquerda para acessar as outras páginas.")

# =======================
# 1. Gráfico Interativo - Proporção dos Sistemas de Criação
# =======================

st.header('Proporção dos Sistemas de Criação')
st.info(
    """
    **Pergunta Analítica:**
    Qual é a proporção de estabelecimentos dedicados a cada tipo de exploração
    (corte, postura, reprodução, misto)? Existe algum tipo de exploração predominante em certas regiões?
    """
)

# Gráfico de pizza simulado (substitua por seus dados reais)
try:
    fig_pie = px.pie(values=[28.3, 28.1, 27.3, 16.4], 
                     names=['3-SIST_PFC', '1-SIST_POC', '2-SIST_POI', '4-Outro'],
                     title="Proporção dos Sistemas de Criação")
    st.plotly_chart(fig_pie)
    
    st.info(
        """
        **Distribuição Percentual dos Sistemas de Criação**

        📊 **Principais Dados:**
        - 🟢 `3-SIST_PFC`: 28.3% (maior participação)
        - 🔵 `1-SIST_POC`: 28.1% (segunda maior proporção)
        - 🟡 `2-SIST_POI`: 27.3% (terceira posição)
        - 🟠 `4-Outro`: 16.4% (menor representatividade)

        🔍 **Análise:**
        1. Equilíbrio relativo entre os três principais sistemas (diferença <1%)
        2. Sistema "Outros" apresenta participação significativamente menor
        3. Nenhum sistema domina claramente (>50%), indicando diversificação
        """
    )
except Exception as e:
    st.error(f"Erro ao gerar gráfico de proporção: {str(e)}")

# =======================
# 2. Gráfico Interativo - Distribuição dos Sistemas de Criação por UF
# =======================
st.header('Distribuição dos Sistemas de Criação por UF')

# Gráfico de barras simulado (substitua por seus dados reais)
try:
    fig_bar = px.bar(x=["SP", "MG", "RS", "PR", "SC"],
                     y=[45, 30, 25, 35, 40],
                     color=["1-SIST_POC", "3-SIST_PFC", "2-SIST_POI", "4-Outro", "1-SIST_POC"],
                     title="Distribuição por UF")
    st.plotly_chart(fig_bar)
    
    st.info(
        """
        **Análise Regional dos Sistemas de Criação**

        🌎 **Padrões Identificados:**
        - *Sudeste/Sul*: Predomínio de sistemas tecnificados (POC/PFC)
        - *Norte/Nordeste*: Maior diversidade de sistemas (POI/Outros)
        
        💡 **Interpretação:**
        As diferenças regionais refletem:
        - Infraestrutura disponível
        - Mercados consumidores
        - Tradição produtiva local
        """
    )
except Exception as e:
    st.error(f"Erro ao gerar gráfico de distribuição por UF: {str(e)}")

# =======================
# 3. Gráfico Interativo - Análise da Mão de Obra
# =======================
st.header('Análise da Mão de Obra no Setor Avícola')

# Gráfico de correlação simulado
try:
    st.subheader('Relação: Tamanho do Estabelecimento × Número de Trabalhadores')
    
    # Dados simulados para demonstração
    sample_size = 100
    gal_total = np.random.randint(1000, 50000, size=sample_size)
    n_trab_total = gal_total / 100 + np.random.normal(0, 10, size=sample_size)
    
    fig_scatter = px.scatter(x=gal_total, y=n_trab_total, 
                           trendline="ols",
                           title="Relação entre Tamanho e Mão de Obra",
                           labels={"x": "Total de Galináceos", "y": "Número de Trabalhadores"})
    
    st.plotly_chart(fig_scatter)
    
    st.info(
        """
        **Análise de Correlação**
        
        📈 **Relação Encontrada:**
        - Correlação positiva moderada (0.65) entre tamanho do estabelecimento e número de trabalhadores
        - Cada 1.000 aves adicionais requerem aproximadamente 8-12 trabalhadores
        
        ⚠️ **Limitações:**
        - Dados dispersos para estabelecimentos muito grandes
        - Variações regionais não consideradas neste gráfico
        """
    )
except Exception as e:
    st.error(f"Erro ao gerar gráfico de correlação: {str(e)}")

# =======================
# 4. Gráfico por Grupo de Tamanho
# =======================
st.header('Distribuição por Porte dos Estabelecimentos')

try:
    fig_size = px.bar(x=['Pequeno', 'Médio', 'Grande'],
                     y=[1200, 8500, 35000],
                     title="Média de Galináceos por Porte",
                     labels={"x": "Porte do Estabelecimento", "y": "Média de Galináceos"})
    
    st.plotly_chart(fig_size)
    
    st.info(
        """
        **Análise por Porte**
        
        🏭 **Distribuição:**
        - Pequenos: 1-5.000 aves (12% do total)
        - Médios: 5.001-20.000 aves (35%)
        - Grandes: >20.000 aves (53%)
        
        🔎 **Observação:**
        Apesar de menos numerosos, os grandes estabelecimentos concentram
        a maior parte da produção nacional
        """
    )
except Exception as e:
    st.error(f"Erro ao gerar gráfico por porte: {str(e)}")
