import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Frequência de Estabelecimentos por UF')

# Carregar o dataset
df = pd.read_csv("GALINACEOS.csv", sep=";")

# Filtra apenas linhas onde o nível territorial é UF
df_uf = df[df["NIV_TERR"] == "UF"]
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Exploração dos Galináceos por UF')

# Carregar o dataset
df = pd.read_csv("GALINACEOS.csv", sep=";")

# Filtra apenas linhas onde o nível territorial é UF
df_uf = df[df["NIV_TERR"] == "UF"]

if "NOM_TERR" in df_uf.columns:
    # Gráfico 1: Frequência de estabelecimentos por UF
    freq_estab_por_uf = df_uf["NOM_TERR"].value_counts().sort_index()
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=freq_estab_por_uf.index, y=freq_estab_por_uf.values, ax=ax1)
    ax1.set_title("Frequência de Estabelecimentos por UF")
    ax1.set_xlabel("UF")
    ax1.set_ylabel("Número de Estabelecimentos")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig1)

    # Gráfico 2: Total de aves por UF
    # Ajuste "E_TEM_GAL" para a coluna correta caso seu total de aves esteja em outro campo
    total_aves_por_uf = df_uf.groupby("NOM_TERR")["E_TEM_GAL"].sum().sort_index()
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=total_aves_por_uf.index, y=total_aves_por_uf.values, ax=ax2)
    ax2.set_title("Total de Aves por UF")
    ax2.set_xlabel("UF")
    ax2.set_ylabel("Total de Aves")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig2)
else:
    st.error("Coluna 'NOM_TERR' não encontrada no arquivo GALINACEOS.csv. Verifique o nome das colunas.")

st.subheader('Exemplo dos Dados')
st.dataframe(df_uf.head())
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

