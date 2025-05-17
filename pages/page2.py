import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Distribuição de Matrizes por Região")

# Carregar o DataFrame real do arquivo CSV
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

# Garantir que as colunas necessárias existem
if 'NOM_TERR' not in df.columns or 'GAL_MATR' not in df.columns:
    st.error("O arquivo deve conter as colunas 'NOM_TERR' e 'GAL_MATR'.")
    st.write("Colunas disponíveis:", df.columns.tolist())
    st.stop()

# Converter nomes para formato consistente (strip e title)
df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()
regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']

# Filtrar apenas linhas das regiões
df_regioes = df[df['NOM_TERR'].isin(regioes)].copy()

# Garantir que a coluna está numérica
df_regioes['GAL_MATR'] = pd.to_numeric(df_regioes['GAL_MATR'], errors='coerce')

# Agrupar os dados por 'NOM_TERR' e somar o total de 'GAL_MATR'
total_matrizes_por_regiao = df_regioes.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum()

# Só continua se houver dados
if total_matrizes_por_regiao.empty or total_matrizes_por_regiao['GAL_MATR'].sum() == 0:
    st.warning("Não há dados de matrizes para as regiões no arquivo.")
else:
    st.subheader("Tabela: Total de Matrizes por Região")
    st.dataframe(total_matrizes_por_regiao)

    # Calcular proporção
    total = total_matrizes_por_regiao['GAL_MATR'].sum()
    total_matrizes_por_regiao['Proporcao'] = total_matrizes_por_regiao['GAL_MATR'] / total

    # Gráfico de pizza
    st.subheader("Gráfico de Pizza: Distribuição de Matrizes por Região")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        total_matrizes_por_regiao['Proporcao'],
        labels=total_matrizes_por_regiao['NOM_TERR'],
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    ax.set_title('Distribuição de Matrizes por Região')
    ax.axis('equal')
    plt.tight_layout()
    st.pyplot(fig)
