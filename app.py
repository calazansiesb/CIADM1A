import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Frequência de Estabelecimentos por UF')

# Carregar o dataset
df = pd.read_csv("GALINACEOS.csv", sep=";")

# Filtra apenas linhas onde o nível territorial é UF
df_uf = df[df["NIV_TERR"] == "UF"]

# Checa se as colunas existem
if "NOM_TERR" in df_uf.columns:
    freq_estab_por_uf = df_uf["NOM_TERR"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=freq_estab_por_uf.index, y=freq_estab_por_uf.values, ax=ax)
    ax.set_title("Frequência de Estabelecimentos por UF")
    ax.set_xlabel("UF")
    ax.set_ylabel("Número de Estabelecimentos")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.error("Coluna 'NOM_TERR' não encontrada no arquivo GALINACEOS.csv. Verifique o nome das colunas.")

st.subheader('Exemplo dos Dados')
st.dataframe(df_uf.head())
