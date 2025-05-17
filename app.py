import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Análise de Galináceos no Brasil')

# Função para limpar valores numéricos
def clean_numeric_value(x):
    if isinstance(x, str):
        cleaned_value = ''.join(c for c in x if c.isdigit() or c == '.' or c == ',')
        cleaned_value = cleaned_value.replace(',', '.', 1)
        return cleaned_value
    return x

# Carregar o DataFrame
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

# Limpar a coluna 'GAL_TOTAL'
if 'GAL_TOTAL' in df.columns:
    df['GAL_TOTAL'] = df['GAL_TOTAL'].apply(clean_numeric_value)
    df['GAL_TOTAL'] = df['GAL_TOTAL'].replace('', np.nan)
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')

# Filtrar apenas as Unidades da Federação (UF)
df_uf = df[df['NIV_TERR'] == 'UF']

# =======================
# 1. Frequência/proporção por SIST_CRIA (Sistema de Criação)
# =======================

st.header('Sistemas de Criação de Galináceos')
freq_sistema_cria = df['SIST_CRIA'].value_counts()
prop_sistema_cria = df['SIST_CRIA'].value_counts(normalize=True) * 100

st.subheader('Frequência dos Sistemas de Criação')
st.write(freq_sistema_cria)
st.subheader('Proporção dos Sistemas de Criação (%)')
st.write(prop_sistema_cria.round(1))

# Gráfico de Barras - Proporção dos Sistemas de Criação
fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
sns.barplot(x=prop_sistema_cria.index, y=prop_sistema_cria.values, ax=ax_bar)
ax_bar.set_title('Proporção de Estabelecimentos por Sistema de Criação')
ax_bar.set_xlabel('Sistema de Criação')
ax_bar.set_ylabel('Proporção (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig_bar)

# Gráfico de Pizza - Proporção dos Sistemas de Criação
fig_pie, ax_pie = plt.subplots(figsize=(8, 8))

descricao_dict = {
    "1-SIST_POC": "Produtores de ovos para consumo",
    "2-SIST_POI": "Produtores de ovos para incubação",
    "3-SIST_PFC": "Produtores de frangos de corte",
    "4-Outro": "Outros produtores"
}
descricao_labels = [descricao_dict.get(s, s) for s in prop_sistema_cria.index]

wedges, texts, autotexts = ax_pie.pie(
    prop_sistema_cria,
    autopct='%1.1f%%',
    startangle=140,
    pctdistance=0.85
)
legend_labels = [
    f"{sistema}: {desc} ({prop:0.1f}%)"
    for sistema, prop, desc in zip(
        prop_sistema_cria.index,
        prop_sistema_cria,
        descricao_labels
    )
]
ax_pie.legend(labels=legend_labels, loc="best", bbox_to_anchor=(1, 0.5))
ax_pie.set_title('Proporção de Estabelecimentos por Sistema de Criação')
ax_pie.axis('equal')
plt.tight_layout()
st.pyplot(fig_pie)

# =======================
# 2. Barras empilhadas: Distribuição dos tipos de exploração por UF
# =======================

st.header('Distribuição dos Sistemas de Criação por UF')
dist_sistema_cria_por_uf = df_uf.groupby('NOM_TERR')['SIST_CRIA'].value_counts(normalize=True).unstack(fill_value=0) * 100

st.dataframe(dist_sistema_cria_por_uf.round(1))

fig_stack, ax_stack = plt.subplots(figsize=(13, 8))
dist_sistema_cria_por_uf.plot(kind='bar', stacked=True, ax=ax_stack)
ax_stack.set_title('Distribuição de Sistemas de Criação por UF')
ax_stack.set_xlabel('UF')
ax_stack.set_ylabel('Proporção (%)')
plt.xticks(rotation=45, ha='right')
ax_stack.legend(title='Sistema de Criação', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(fig_stack)

# =======================
# 3. Gráficos e análises anteriores
# =======================

st.header('Análises Gerais por UF')

# Frequência de estabelecimentos por UF
freq_estab_por_uf = df_uf['NOM_TERR'].value_counts().sort_index()
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=freq_estab_por_uf.index, y=freq_estab_por_uf.values, ax=ax1)
ax1.set_title("Frequência de Estabelecimentos por UF")
ax1.set_xlabel("UF")
ax1.set_ylabel("Número de Estabelecimentos")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig1)

# Total de aves por UF
if 'GAL_TOTAL' in df_uf.columns:
    total_aves_por_uf = df_uf.groupby('NOM_TERR')['GAL_TOTAL'].sum().sort_values(ascending=False)
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
else:
    st.info("A coluna 'GAL_TOTAL' não está presente para análise de total de aves.")

# Exemplo dos dados filtrados
st.header('Exemplo dos Dados das UF')
st.dataframe(df_uf.head())
# --- Gráfico: Média de GAL_TOTAL por grupo de tamanho de Q_DZ_PROD ---
st.header('Média de GAL_TOTAL por Grupo de Tamanho de Q_DZ_PROD')

if 'Q_DZ_PROD' in df.columns and 'GAL_TOTAL' in df.columns:
    # Classificar os estabelecimentos em grupos (tercis)
    df['TAMANHO_GRUPO'] = pd.qcut(df['Q_DZ_PROD'].dropna(), q=3, labels=['Pequeno', 'Médio', 'Grande'])
    # Calcular média de GAL_TOTAL por grupo
    variavel_por_grupo = df.groupby('TAMANHO_GRUPO')['GAL_TOTAL'].mean()
    
    st.write("Média de GAL_TOTAL por grupo de tamanho (baseado em Q_DZ_PROD):")
    st.dataframe(variavel_por_grupo)

    # Gráfico
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=variavel_por_grupo.index, y=variavel_por_grupo.values, ax=ax)
    ax.set_title('Média de GAL_TOTAL por Grupo de Tamanho (Q_DZ_PROD)')
    ax.set_xlabel('Grupo de Tamanho')
    ax.set_ylabel('Média de GAL_TOTAL')
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("Coluna 'Q_DZ_PROD' ou 'GAL_TOTAL' não encontrada no DataFrame.")
