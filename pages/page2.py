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

if 'NOM_TERR' not in df.columns or 'GAL_MATR' not in df.columns or 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
    st.error("O arquivo deve conter as colunas 'NOM_TERR', 'GAL_MATR', 'SIST_CRIA' e 'GAL_TOTAL'.")
    st.write("Colunas disponíveis:", df.columns.tolist())
    st.stop()

# Normalizar nomes
df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()
df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce')
df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')  # Garantindo que seja numérico

# Remover valores NaN na coluna GAL_TOTAL
df = df.dropna(subset=['GAL_TOTAL'])

# --------- GRÁFICO DE DENSIDADE: Aves por Sistema de Criação ---------
st.subheader("Gráfico de Densidade: Aves por Sistema de Criação")

if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
    st.warning("O DataFrame não contém as colunas 'SIST_CRIA' ou 'GAL_TOTAL'.")
else:
    if df[['SIST_CRIA', 'GAL_TOTAL']].dropna().empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Criando o gráfico de densidade com ajustes para ficarem visíveis
        sns.kdeplot(data=df, x='GAL_TOTAL', hue='SIST_CRIA', fill=True, linewidth=2, common_norm=False, palette="Set2", ax=ax)
        
        ax.set_title('Densidade de Aves por Sistema de Criação', fontsize=14)
        ax.set_xlabel('Total de Aves (Cabeça)', fontsize=12)
        ax.set_ylabel('Densidade', fontsize=12)
        ax.legend(title="Sistema de Criação", fontsize=10)
        plt.tight_layout()
        
        st.pyplot(fig)
