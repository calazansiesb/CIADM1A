import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset
df = pd.read_csv('GALINACEOS.csv', sep=';')  # ajuste o separador se necessário

# Calcular a frequência de estabelecimentos por UF (ajuste o nome da coluna conforme seu CSV)
freq_estab_por_uf = df['UF'].value_counts().sort_index()

st.title('Frequência de Estabelecimentos por UF')

# Visualização (Gráfico de Barras)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=freq_estab_por_uf.index, y=freq_estab_por_uf.values, ax=ax)
ax.set_title('Frequência de Estabelecimentos por UF')
ax.set_xlabel('UF')
ax.set_ylabel('Número de Estabelecimentos')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(fig)
