import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Análise de Galináceos por UF')

# Função para limpar valores numéricos
def clean_numeric_value(x):
    if isinstance(x, str):
        cleaned_value = ''.join(c for c in x if c.isdigit() or c == '.' or c == ',')
        cleaned_value = cleaned_value.replace(',', '.', 1)
        return cleaned_value
    return x

# Carregar o dataset
df = pd.read_csv("GALINACEOS.csv", sep=";")

# Limpar a coluna 'GAL_TOTAL'
df['GAL_TOTAL'] = df['GAL_TOTAL'].apply(clean_numeric_value)
df['GAL_TOTAL'] = df['GAL_TOTAL'].replace('', np.nan)
df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')

# Filtrar apenas as Unidades da Federação (UF)
df_uf = df[df['NIV_TERR'] == 'UF']

# Soma do total de aves por UF
total_aves_por_uf = df_uf.groupby('NOM_TERR')['GAL_TOTAL'].sum().sort_values(ascending=False)

# Frequência de estabelecimentos por UF (apenas para exibir o gráfico original se desejar)
freq_estab_por_uf = df_uf['NOM_TERR'].value_counts().sort_index()

# Gráfico 1: Frequência de estabelecimentos por UF
st.subheader('Frequência de Estabelecimentos por UF')
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=freq_estab_por_uf.index, y=freq_estab_por_uf.values, ax=ax1)
ax1.set_title("Frequência de Estabelecimentos por UF")
ax1.set_xlabel("UF")
ax1.set_ylabel("Número de Estabelecimentos")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)

# Gráfico 2: Total de aves por UF
st.subheader('Total de Aves por UF')
fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(x=total_aves_por_uf.index, y=total_aves_por_uf.values, ax=ax2)
ax2.set_title('Total de Aves por UF')
ax2.set_xlabel('UF')
ax2.set_ylabel('Total de Aves')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig2)

# Estatísticas
desvio_padrao_aves_uf = total_aves_por_uf.std()
media_aves_uf = total_aves_por_uf.mean()
coeficiente_variacao_aves_uf = (desvio_padrao_aves_uf / media_aves_uf) * 100

st.subheader('Estatísticas do Total de Aves por UF')
st.write(f"**Desvio padrão:** {desvio_padrao_aves_uf:,.2f}")
st.write(f"**Média:** {media_aves_uf:,.2f}")
st.write(f"**Coeficiente de variação:** {coeficiente_variacao_aves_uf:.2f}%")

# Exibe exemplo dos dados filtrados
st.subheader('Exemplo dos Dados das UF')
st.dataframe(df_uf.head())
