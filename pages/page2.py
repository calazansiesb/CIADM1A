import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Total de Matrizes por Unidade Territorial")

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

# Agrupar os dados por 'NOM_TERR' e somar o total de 'GAL_MATR'
total_matrizes_por_territorio = df.groupby('NOM_TERR')['GAL_MATR'].sum().reset_index()

st.subheader("Tabela: Total de Matrizes por Unidade Territorial")
st.dataframe(total_matrizes_por_territorio)

# --- Gráfico de Barras ---
st.subheader("Gráfico de Barras: Total de Matrizes por Unidade Territorial")
fig_bar, ax_bar = plt.subplots(figsize=(12, 6))
ax_bar.bar(total_matrizes_por_territorio['NOM_TERR'], total_matrizes_por_territorio['GAL_MATR'])
ax_bar.set_title('Total de Matrizes por Unidade Territorial')
ax_bar.set_xlabel('Unidade Territorial')
ax_bar.set_ylabel('Total de Matrizes (Cabeça)')
plt.xticks(rotation=45, ha="right", fontsize=8)
plt.tight_layout()
st.pyplot(fig_bar)

# --- Gráfico de Pizza ---
st.subheader("Gráfico de Pizza: Distribuição de Matrizes por Unidade Territorial")
# Calcular a proporção de matrizes para cada território
total_matrizes = total_matrizes_por_territorio['GAL_MATR'].sum()
total_matrizes_por_territorio['Proporcao'] = total_matrizes_por_territorio['GAL_MATR'] / total_matrizes

fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
ax_pie.pie(
    total_matrizes_por_territorio['Proporcao'],
    labels=total_matrizes_por_territorio['NOM_TERR'],
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Paired.colors
)
ax_pie.set_title('Distribuição de Matrizes por Unidade Territorial')
ax_pie.axis('equal')
plt.tight_layout()
st.pyplot(fig_pie)
