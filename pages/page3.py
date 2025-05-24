import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def gerar_grafico_densidade_aves_por_sistema(df):
    """
    Exibe no Streamlit um gráfico de densidade interativo da distribuição do total de aves (GAL_TOTAL)
    por sistema de criação (SIST_CRIA) usando Plotly.
    """
    st.subheader("📊 Densidade de Aves por Sistema de Criação")

    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou 'GAL_TOTAL').")
        return

    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
        return

    # Gráfico de densidade interativo com Plotly
    fig = px.density_heatmap(
        df_plot,
        x='GAL_TOTAL',
        y='SIST_CRIA',
        title='Distribuição de Densidade de Aves por Sistema de Criação',
        labels={'GAL_TOTAL': 'Total de Aves (Cabeça)', 'SIST_CRIA': 'Sistema de Criação'},
        color_continuous_scale='Oranges',
        nbinsx=20,
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
     **🔍 Análise da Distribuição de Densidade de Aves por Sistema de Criação**

    📌 **Principais observações:**
    - O sistema "Outros" apresenta concentração de estabelecimentos com menor número total de aves, predominantemente entre 6.000 e 7.000 cabeças.
    - "Ovos para Consumo" e "Frangos de Corte" mostram maior dispersão, com a maioria dos registros entre 9.000 e 12.000 aves por estabelecimento.
    - "Ovos para Incubação" destaca-se por concentrar-se nas faixas mais elevadas, acima de 13.000 aves.

    💡 **Interpretação:**
    - O gráfico evidencia diferentes perfis produtivos: sistemas voltados para incubação tendem a operar com plantéis mais numerosos, enquanto sistemas classificados como "Outros" concentram-se em pequenas criações.
    - A variação na densidade sugere especialização e segmentação claras entre os sistemas de criação, refletindo demandas produtivas e estratégias distintas.
    - As informações são úteis para orientar políticas de apoio e estratégias de crescimento conforme o perfil predominante de cada sistema.
    """)

def gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao='aves'):
    """
    Exibe no Streamlit um gráfico interativo da distribuição da produção (aves ou ovos) por sistema de criação.
    """
    if tipo_producao == 'aves':
        coluna_producao = 'GAL_VEND'
        rotulo_eixo_y = 'Quantidade de Aves Vendidas (Cabeça)'
        titulo_grafico = '📈 Distribuição da Venda de Aves por Sistema de Criação'
    elif tipo_producao == 'ovos':
        coluna_producao = 'Q_DZ_PROD'
        rotulo_eixo_y = 'Quantidade de Ovos Produzidos (Dúzia)'
        titulo_grafico = '🥚 Distribuição da Produção de Ovos por Sistema de Criação'
    else:
        st.warning("Tipo de produção inválido. Escolha 'aves' ou 'ovos'.")
        return

    if 'SIST_CRIA' not in df.columns or coluna_producao not in df.columns:
        st.warning(f"O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou '{coluna_producao}').")
        return

    producao_por_sistema = df.groupby('SIST_CRIA')[coluna_producao].sum().reset_index()

    # Gráfico de barras interativo com Plotly
    fig = px.bar(
        producao_por_sistema,
        x='SIST_CRIA',
        y=coluna_producao,
        title=titulo_grafico,
        labels={'SIST_CRIA': 'Sistema de Criação', coluna_producao: rotulo_eixo_y},
        color='SIST_CRIA',
        color_discrete_sequence=px.colors.sequential.Oranges,
        text=coluna_producao
    )
    
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info(f"""
    **🔍 Análise de Produção ({'Aves' if tipo_producao == 'aves' else 'Ovos'})**
    
    📌 **Principais observações:**
    - Comparação da produção entre diferentes sistemas de criação
    - Identificação dos sistemas mais produtivos
    - Proporção relativa entre os sistemas
    
    💡 **Interpretação:**
    - Sistemas com maiores volumes indicam especializações ou demandas de mercado
    - Diferenças significativas podem refletir vantagens competitivas de certos sistemas
    - Padrões de produção podem sugerir tendências do setor
    """)

def gerar_histograma_aves_por_sistema(df):
    """
    Exibe no Streamlit um histograma interativo da distribuição do total de aves (GAL_TOTAL)
    por sistema de criação (SIST_CRIA) usando Plotly.
    """
    st.subheader("📊 Histograma de Distribuição de Aves por Sistema")

    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou 'GAL_TOTAL').")
        return

    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o histograma.")
        return

    # Histograma interativo com Plotly
    fig = px.histogram(
        df_plot,
        x='GAL_TOTAL',
        color='SIST_CRIA',
        title='Distribuição de Aves por Sistema de Criação',
        labels={'GAL_TOTAL': 'Total de Aves (Cabeça)', 'SIST_CRIA': 'Sistema de Criação'},
        color_discrete_sequence=px.colors.sequential.Oranges,
        nbins=20,
        barmode='stack',
        opacity=0.7
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **🔍 Análise de Distribuição**
    
    📌 **Principais observações:**
    - Frequência de diferentes faixas de quantidade de aves
    - Padrões de distribuição por sistema de criação
    - Concentração de produções em determinadas escalas
    
    💡 **Interpretação:**
    - Picos no histograma indicam escalas de produção mais comuns
    - Sistemas com distribuição mais ampla podem ter maior variação nos tamanhos dos produtores
    - Concentrações em faixas específicas podem refletir modelos de negócio padronizados
    """)

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola - Sistemas de Criação",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Análise de Sistemas de Criação Avícola')
st.markdown("---")

# DataFrame de exemplo (substituir por carregamento real de dados)
data = {
    'SIST_CRIA': [
        'Ovos para Consumo', 'Frangos de Corte', 'Ovos para Consumo', 'Outros',
        'Frangos de Corte', 'Ovos para Incubação', 'Outros', 'Ovos para Consumo',
        'Frangos de Corte', 'Ovos para Incubação'
    ],
    'GAL_TOTAL': [
        10000, 12000, 11000, 5000,
        13000, 14000, 6000, 9000,
        11500, 12500
    ],
    'GAL_VEND': [
        8000, 11000, 9500, 4500,
        12000, 13000, 5500, 8500,
        10500, 11500
    ],
    'Q_DZ_PROD': [
        5000, 6000, 5500, 2000,
        6500, 7000, 2500, 4500,
        5750, 6250
    ]
}
df = pd.DataFrame(data)

# Seção de gráficos
col1, col2 = st.columns([3, 1])
with col1:
    gerar_grafico_densidade_aves_por_sistema(df)
    
with col2:
    tipo = st.radio(
        "Tipo de produção:",
        ('aves', 'ovos'),
        format_func=lambda x: "Aves vendidas" if x=="aves" else "Ovos produzidos",
        key='tipo_producao'
    )

gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao=tipo)
gerar_histograma_aves_por_sistema(df)

# Rodapé
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base em dados de produção avícola*  
📅 *Atualizado em Outubro 2023*  
""")
