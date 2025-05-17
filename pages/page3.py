import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_grafico_densidade_aves_por_sistema(df):
    """
    Exibe no Streamlit um gráfico de densidade da distribuição do total de aves (GAL_TOTAL)
    por sistema de criação (SIST_CRIA).
    """
    st.subheader("Gráfico de Densidade: Aves por Sistema de Criação")

    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas 'SIST_CRIA' ou 'GAL_TOTAL'.")
        return

    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    sistemas = df_plot['SIST_CRIA'].unique()
    cores = sns.color_palette("Set2", len(sistemas))
    for cor, sist in zip(cores, sistemas):
        sns.kdeplot(
            data=df_plot[df_plot['SIST_CRIA'] == sist],
            x='GAL_TOTAL',
            fill=True,
            label=sist,
            alpha=0.5,
            ax=ax,
            color=cor
        )
    ax.set_title('Densidade de Aves por Sistema de Criação')
    ax.set_xlabel('Total de Aves (Cabeça)')
    ax.set_ylabel('Densidade')
    ax.legend(title='SIST_CRIA')
    st.pyplot(fig)
    plt.close(fig)

def gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao='aves'):
    """
    Exibe no Streamlit um gráfico da distribuição da produção (aves ou ovos) por sistema de criação.
    """
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
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='SIST_CRIA', y=coluna_producao, data=producao_por_sistema, palette="Set2", ax=ax)
    ax.set_title(titulo_grafico)
    ax.set_xlabel('Sistema de Criação')
    ax.set_ylabel(rotulo_eixo_y)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

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

# Gráfico 1: Densidade (igual à imagem fornecida)
gerar_grafico_densidade_aves_por_sistema(df)

# Gráfico 2: Distribuição da produção (usuário pode alternar entre aves/ovos)
tipo = st.radio(
    "Escolha o tipo de produção para visualizar por sistema de criação:",
    ('aves', 'ovos'),
    format_func=lambda x: "Aves vendidas" if x=="aves" else "Ovos produzidos"
)
gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao=tipo)
