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

# Converter nomes para formato consistente (strip)
df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip()

# Garantir que a coluna está numérica
df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce')

# Definir listas de regiões e remover "Brasil"
regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
df = df[~df['NOM_TERR'].str.upper().eq('BRASIL')]

# --- Gráfico 1: Barras por Unidade Territorial (Estados e Regiões, exceto Brasil) ---
st.subheader("Gráfico de Barras: Total de Matrizes por Unidade Territorial (Estados e Regiões)")
total_matrizes_por_territorio = df.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum().sort_values('GAL_MATR', ascending=False)
st.dataframe(total_matrizes_por_territorio)

fig_bar, ax_bar = plt.subplots(figsize=(14, 6))
ax_bar.bar(total_matrizes_por_territorio['NOM_TERR'], total_matrizes_por_territorio['GAL_MATR'], color='skyblue')
ax_bar.set_title('Total de Matrizes por Unidade Territorial')
ax_bar.set_xlabel('Unidade Territorial')
ax_bar.set_ylabel('Total de Matrizes (Cabeça)')
plt.xticks(rotation=90, ha="center", fontsize=8)
plt.tight_layout()
st.pyplot(fig_bar)

# --- Gráfico 2: Pizza por Região ---
st.subheader("Gráfico de Pizza: Distribuição de Matrizes por Região")
df_regioes = df[df['NOM_TERR'].str.title().isin(regioes)].copy()
total_matrizes_por_regiao = df_regioes.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum()

if total_matrizes_por_regiao.empty or total_matrizes_por_regiao['GAL_MATR'].sum() == 0:
    st.warning("Não há dados de matrizes para as regiões no arquivo.")
else:
    total = total_matrizes_por_regiao['GAL_MATR'].sum()
    total_matrizes_por_regiao['Proporcao'] = total_matrizes_por_regiao['GAL_MATR'] / total
    st.dataframe(total_matrizes_por_regiao)
    fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
    ax_pie.pie(
        total_matrizes_por_regiao['Proporcao'],
        labels=total_matrizes_por_regiao['NOM_TERR'],
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    ax_pie.set_title('Distribuição de Matrizes por Região')
    ax_pie.axis('equal')
    plt.tight_layout()
    st.pyplot(fig_pie)

# --- Gráfico 3: Barras por Estado (apenas estados, sem regiões e sem Brasil) ---
st.subheader("Gráfico de Barras: Total de Matrizes por Estado (apenas UF, sem regiões e sem Brasil)")

# Estados: tudo que não está em regiões e não é Brasil
estados = df[~df['NOM_TERR'].str.title().isin(regioes)].copy()

if estados.empty or estados['GAL_MATR'].sum() == 0:
    st.warning("Não há dados de matrizes para os estados no arquivo.")
else:
    total_matrizes_por_estado = estados.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum().sort_values('GAL_MATR', ascending=False)
    st.dataframe(total_matrizes_por_estado)
    fig_estado, ax_estado = plt.subplots(figsize=(16, 6))
    ax_estado.bar(total_matrizes_por_estado['NOM_TERR'], total_matrizes_por_estado['GAL_MATR'], color='orange')
    ax_estado.set_title('Total de Matrizes por Estado (apenas UF)')
    ax_estado.set_xlabel('Estado')
    ax_estado.set_ylabel('Total de Matrizes (Cabeça)')
    plt.xticks(rotation=90, ha="center", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig_estado)
