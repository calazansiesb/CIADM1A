import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def gerar_grafico_densidade_aves_por_sistema(df):
    """
    Exibe no Streamlit um gráfico de densidade da distribuição do total de aves (GAL_TOTAL)
    por sistema de criação (SIST_CRIA).
    Args:
        df (pd.DataFrame): DataFrame contendo os dados.
    """
    st.subheader("Gráfico de Densidade: Aves por Sistema de Criação")

    # Verifica se as colunas necessárias existem
    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas 'SIST_CRIA' ou 'GAL_TOTAL'.")
        return

    # Remove valores nulos
    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
        return

    # Gera o gráfico de densidade
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

# Cria um DataFrame de exemplo
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
    ]
}
df = pd.DataFrame(data)

# Exibe o gráfico na página
gerar_grafico_densidade_aves_por_sistema(df)
