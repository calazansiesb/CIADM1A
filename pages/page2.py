import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Matrizes por Unidade Territorial: Estados e Regiões")

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

# --------- GRÁFICO 1: BARRAS - Apenas Estados (UFs) ---------
st.subheader("Gráfico de Barras: Total de Matrizes por Estado (apenas UFs)")

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

# --------- GRÁFICO 2: PIZZA - Apenas Regiões ---------
st.subheader("Gráfico de Pizza: Distribuição de Matrizes por Região")

df_regioes = df[df['NOM_TERR'].isin(regioes)].copy()
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
    #---------------------------------------

st.subheader("Gráfico de Densidade: Distribuição das Matrizes")

if df['GAL_MATR'].dropna().empty:
    st.warning("Não há dados numéricos suficientes para gerar o gráfico de densidade.")
else:
    fig_dens, ax_dens = plt.subplots(figsize=(10, 5))
    try:
        # Para Seaborn >= 0.11
        sns.kdeplot(df['GAL_MATR'].dropna(), ax=ax_dens, fill=True, color="purple")
    except TypeError:
        # Para Seaborn < 0.11 (sem fill)
        sns.kdeplot(df['GAL_MATR'].dropna(), ax=ax_dens, color="purple")
    ax_dens.set_title("Densidade da Distribuição do Total de Matrizes")
    ax_dens.set_xlabel("Total de Matrizes (Cabeça)")
    ax_dens.set_ylabel("Densidade")
    plt.tight_layout()
    st.pyplot(fig_dens)
    #--------------------------------------------------
