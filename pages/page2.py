import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Análises de Matrizes por Unidade Territorial")

# Carregar o DataFrame real do arquivo CSV
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

if 'NOM_TERR' not in df.columns or 'GAL_MATR' not in df.columns:
    st.error("O arquivo deve conter as colunas 'NOM_TERR' e 'GAL_MATR'.")
    st.write("Colunas disponíveis:", df.columns.tolist())
    st.stop()

# Normalizar nomes
df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()
df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce')

# Listas de regiões e Brasil
regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
brasil = ['Brasil']

# Gráfico 3: Barras por Estado (apenas UFs)
st.subheader("Gráfico de Barras: Total de Matrizes por Estado (apenas UFs, sem regiões e sem Brasil)")

# Filtrar apenas estados: não estão nas regiões nem em "Brasil"
df_estados = df[~df['NOM_TERR'].isin(regioes + brasil)].copy()

if df_estados.empty or df_estados['GAL_MATR'].sum() == 0:
    st.warning("Não há dados de matrizes para os estados no arquivo.")
else:
    total_matrizes_por_estado = df_estados.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum().sort_values('GAL_MATR', ascending=False)
    st.dataframe(total_matrizes_por_estado)
    fig_estado, ax_estado = plt.subplots(figsize=(16, 6))
    ax_estado.bar(total_matrizes_por_estado['NOM_TERR'], total_matrizes_por_estado['GAL_MATR'], color='orange')
    ax_estado.set_title('Total de Matrizes por Estado (apenas UFs)')
    ax_estado.set_xlabel('Estado')
    ax_estado.set_ylabel('Total de Matrizes (Cabeça)')
    plt.xticks(rotation=90, ha="center", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig_estado)
