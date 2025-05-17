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

# Normalizar nomes e converter valores numéricos
df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()
df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce')
df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')

# Remover valores NaN
df = df.dropna(subset=['GAL_TOTAL'])

# --------- GRÁFICO DE DENSIDADE: Aves por Sistema de Criação ---------
st.subheader("Gráfico de Densidade: Aves por Sistema de Criação")

if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
    st.warning("O DataFrame não contém as colunas 'SIST_CRIA' ou 'GAL_TOTAL'.")
else:
    if df[['SIST_CRIA', 'GAL_TOTAL']].dropna().empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Criando o gráfico de densidade com melhorias visuais
        sns.kdeplot(data=df, x='GAL_TOTAL', hue='SIST_CRIA', fill=True, 
                    linewidth=2, common_norm=False, palette="Set2", ax=ax)
        
        ax.set_title('Densidade de Aves por Sistema de Criação', fontsize=16, fontweight='bold')
        ax.set_xlabel('Total de Aves (Cabeça)', fontsize=14)
        ax.set_ylabel('Densidade', fontsize=14)
        ax.legend(title="Sistema de Criação", fontsize=12, title_fontsize='13')
        
        # Ajustando limites e escala do gráfico
        ax.set_xlim(df['GAL_TOTAL'].min() * 0.9, df['GAL_TOTAL'].max() * 1.1)
        ax.set_ylim(0, None)
        
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        
        st.pyplot(fig)
