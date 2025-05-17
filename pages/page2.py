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
regioes
