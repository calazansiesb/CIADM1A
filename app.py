import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Frequência de Estabelecimentos por UF')

# Carregar o dataset
df = pd.read_csv('GALINACEOS.csv', sep=';')  # ajuste o separador se necessário

# Verifica se a coluna 'UF' existe
if 'UF' in df.columns:
    # Calcular a frequência de estabelecimentos por UF
    freq_estab_por_uf = df['UF'].value_counts().sort_index()

    # Gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=freq_estab_por_uf.index, y=freq_estab_por_uf.values, ax=ax)
    ax.set_title('Frequência de Estabelecimentos por UF')
    ax.set_xlabel('UF')
    ax.set_ylabel('Número de Estabelecimentos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.error("A coluna 'UF' não foi encontrada no arquivo GALINACEOS.csv. Verifique o nome das colunas.")

# Exibe uma amostra dos dados
st.subheader('Exemplo dos Dados')
st.dataframe(df.head())
