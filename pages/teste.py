import streamlit as st
import pandas as pd
import plotly.express as px

# Função para gerar gráfico de densidade interativo
def gerar_grafico_densidade_aves_por_sistema(df):
    st.subheader("Gráfico de Densidade: Aves por Sistema de Criação Teste com diego")

    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas 'SIST_CRIA' ou 'GAL_TOTAL'.")
        return

    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
        return

    fig = px.histogram(df_plot, x="GAL_TOTAL", color="SIST_CRIA", histnorm="density",
                       barmode="overlay", opacity=0.6, title="Densidade de Aves por Sistema de Criação",
                       labels={"GAL_TOTAL": "Total de Aves", "SIST_CRIA": "Sistema de Criação"})
    
    st.plotly_chart(fig)

# Função para gerar gráfico de distribuição interativo (aves ou ovos)
def gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao='aves'):
    if tipo_producao == 'aves':
        coluna_producao = 'GAL_VEND'
        rotulo_eixo_y = 'Quantidade de Aves Vendidas (Cabeça)'
        titulo_grafico = 'Distribuição da Venda de Aves por Sistema de Criação'
    elif tipo_producao == 'ovos':
        coluna_producao = 'Q_DZ_PROD'
        rotulo_eixo_y = 'Quantidade de Ovos Produzidos (Dúzia)'
        titulo_grafico = 'Distribuição da Produção de Ovos por Sistema de Criação'
    else:
        st.warning("Tipo de produção inválido. Escolha 'aves' ou 'ovos'.")
        return

    if 'SIST_CRIA' not in df.columns or coluna_producao not in df.columns:
        st.warning(f"O DataFrame não contém as colunas 'SIST_CRIA' ou '{coluna_producao}'.")
        return

    producao_por_sistema = df.groupby('SIST_CRIA')[coluna_producao].sum().reset_index()

    st.subheader(titulo_grafico)
    fig = px.bar(producao_por_sistema, x='SIST_CRIA', y=coluna_producao, color='SIST_CRIA', 
                 title=titulo_grafico, labels={"SIST_CRIA": "Sistema de Criação", coluna_producao: rotulo_eixo_y},
                 hover_data=[coluna_producao])
    
    st.plotly_chart(fig)

# Função para gerar histograma interativo
def gerar_histograma_aves_por_sistema(df):
    st.subheader("Histograma de Aves por Sistema de Criação")

    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas 'SIST_CRIA' ou 'GAL_TOTAL'.")
        return

    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o histograma.")
        return

    fig = px.histogram(df_plot, x="GAL_TOTAL", color="SIST_CRIA", barmode="overlay", 
                       title="Histograma de Aves por Sistema de Criação",
                       labels={"GAL_TOTAL": "Total de Aves", "SIST_CRIA": "Sistema de Criação"},
                       hover_data=["GAL_TOTAL"])
    
    st.plotly_chart(fig)

# DataFrame de exemplo
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
        10000, 12000, 11000, 5000,
        13000, 14000, 6000, 9000,
        11500, 12500
    ],
    'Q_DZ_PROD': [
        5000, 6000, 5500, 2000,
        6500, 7000, 2500, 4500,
        5750, 6250
    ]
}
df = pd.DataFrame(data)

# Gráfico 1: Densidade (Interativo)
gerar_grafico_densidade_aves_por_sistema(df)

# Gráfico 2: Distribuição da produção (usuário pode alternar entre aves/ovos)
tipo = st.radio(
    "Escolha o tipo de produção para visualizar por sistema de criação:",
    ('aves', 'ovos'),
    format_func=lambda x: "Aves vendidas" if x == "aves" else "Ovos produzidos"
)
gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao=tipo)

# Gráfico 3: Histograma (Interativo)
gerar_histograma_aves_por_sistema(df)
