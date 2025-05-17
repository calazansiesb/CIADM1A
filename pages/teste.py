import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Matrizes por Unidade Territorial: Estados e Regiões")

# Carregar o DataFrame real do arquivo CSV
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

# Verificar se todas as colunas necessárias estão presentes
colunas_necessarias = ['NOM_TERR', 'GAL_MATR', 'SIST_CRIA', 'GAL_TOTAL']
if not all(col in df.columns for col in colunas_necessarias):
    st.error(f"O arquivo deve conter as colunas {colunas_necessarias}.")
    st.write("Colunas disponíveis:", df.columns.tolist())
    st.stop()

# Normalizar nomes e converter valores numéricos
df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()
df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce')
df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')

# Remover valores NaN
df = df.dropna(subset=['GAL_TOTAL'])

# Listas de regiões e Brasil
regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
brasil = ['Brasil']

# --------- GRÁFICO 1: BARRAS INTERATIVO - Apenas Estados ---------
st.subheader("Gráfico de Barras: Total de Matrizes por Estado (Interativo)")

df_estados = df[~df['NOM_TERR'].isin(regioes + brasil)].copy()

if df_estados.empty or df_estados['GAL_MATR'].sum() == 0:
    st.warning("Não há dados de matrizes para os estados no arquivo.")
else:
    total_matrizes_por_estado = df_estados.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum().sort_values('GAL_MATR', ascending=False)
    st.dataframe(total_matrizes_por_estado)

    fig_estado = px.bar(
        total_matrizes_por_estado, x="NOM_TERR", y="GAL_MATR", 
        title="Total de Matrizes por Estado", labels={"NOM_TERR": "Estado", "GAL_MATR": "Total de Matrizes"},
        color="GAL_MATR", hover_data=["GAL_MATR"]
    )

    st.plotly_chart(fig_estado)

# --------- GRÁFICO 2: PIZZA INTERATIVO - Apenas Regiões ---------
st.subheader("Gráfico de Pizza: Distribuição de Matrizes por Região (Interativo)")

df_regioes = df[df['NOM_TERR'].isin(regioes)].copy()
total_matrizes_por_regiao = df_regioes.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum()

if total_matrizes_por_regiao.empty or total_matrizes_por_regiao['GAL_MATR'].sum() == 0:
    st.warning("Não há dados de matrizes para as regiões no arquivo.")
else:
    total = total_matrizes_por_regiao['GAL_MATR'].sum()
    total_matrizes_por_regiao['Proporcao'] = total_matrizes_por_regiao['GAL_MATR'] / total
    st.dataframe(total_matrizes_por_regiao)

    fig_pie = px.pie(
        total_matrizes_por_regiao, values="GAL_MATR", names="NOM_TERR", 
        title="Distribuição de Matrizes por Região", hover_data=["GAL_MATR"],
        color="NOM_TERR"
    )

    st.plotly_chart(fig_pie)

# --------- GRÁFICO 3: DENSIDADE INTERATIVO - Aves por Sistema de Criação ---------
st.subheader("Gráfico de Densidade: Aves por Sistema de Criação (Interativo)")

if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
    st.warning("O DataFrame não contém as colunas 'SIST_CRIA' ou 'GAL_TOTAL'.")
else:
    if df[['SIST_CRIA', 'GAL_TOTAL']].dropna().empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
    else:
        fig_densidade = px.histogram(
            df, x="GAL_TOTAL", color="SIST_CRIA", marginal="box",
            title="Densidade de Aves por Sistema de Criação",
            labels={"GAL_TOTAL": "Total de Aves", "SIST_CRIA": "Sistema de Criação"},
            hover_data=["GAL_TOTAL", "SIST_CRIA"]
        )

        st.plotly_chart(fig_densidade)
