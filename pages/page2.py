import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Total de Matrizes por Unidade Territorial (Sem o Brasil)")

# Carregar o DataFrame real do arquivo CSV
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

# Garantir que a coluna está numérica
if 'GAL_MATR' in df.columns:
    df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce')

# Remover o total do Brasil, se existir
if 'NOM_TERR' in df.columns:
    df = df[df['NOM_TERR'].str.upper() != 'BRASIL']

# Verificar se as colunas necessárias existem
if 'NOM_TERR' not in df.columns or 'GAL_MATR' not in df.columns:
    st.error("O arquivo deve conter as colunas 'NOM_TERR' e 'GAL_MATR'.")
    st.write("Colunas disponíveis:", df.columns.tolist())
    st.stop()

# 1. Agrupar os dados por 'NOM_TERR' e somar o total de 'GAL_MATR'
total_matrizes_por_territorio = df.groupby('NOM_TERR')['GAL_MATR'].sum().reset_index()

st.subheader("Tabela: Total de Matrizes por Unidade Territorial")
st.dataframe(total_matrizes_por_territorio)

# 2. Criar o gráfico de barras usando matplotlib e exibir no Streamlit
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(total_matrizes_por_territorio['NOM_TERR'], total_matrizes_por_territorio['GAL_MATR'])
ax.set_title('Total de Matrizes por Unidade Territorial (Sem o Brasil)')
ax.set_xlabel('Unidade Territorial')
ax.set_ylabel('Total de Matrizes (Cabeça)')
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.tight_layout()
st.pyplot(fig)
