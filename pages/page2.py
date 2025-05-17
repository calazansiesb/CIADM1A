import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Variação Temporal da Produção Avícola")

# Carregar o DataFrame (espera-se que o arquivo GALINACEOS.csv esteja na raiz do projeto)
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

# --- Análise da Variação Temporal da Produção Avícola ---

if 'ANO' not in df.columns:
    st.error("Erro: A coluna 'ANO' não está presente no DataFrame.")
    st.stop()

anos = sorted(df['ANO'].unique())
st.write(f"**Anos disponíveis:** {anos}")

# Etapa 1: Preparar os Dados para Análise Temporal
dados_por_ano = {}
for ano in anos:
    df_ano = df[df['ANO'] == ano]
    total_estabelecimentos = df_ano['E_TEM_GAL'].sum() if 'E_TEM_GAL' in df_ano.columns else None
    total_aves = df_ano['GAL_TOTAL'].sum() if 'GAL_TOTAL' in df_ano.columns else None
    proporcoes_sist_cria = df_ano['SIST_CRIA'].value_counts(normalize=True) * 100 if 'SIST_CRIA' in df_ano.columns else None

    dados_por_ano[ano] = {
        'Total Estabelecimentos': total_estabelecimentos,
        'Total Aves': total_aves,
        'Proporcoes SIST_CRIA': proporcoes_sist_cria
    }

df_temporal = pd.DataFrame(dados_por_ano).T
df_temporal['ANO'] = df_temporal.index
df_temporal = df_temporal.reset_index(drop=True)
df_temporal[['Total Aves', 'Total Estabelecimentos']] = df_temporal[['Total Aves', 'Total Estabelecimentos']].apply(pd.to_numeric)

st.subheader("Dados Agregados por Ano")
st.dataframe(df_temporal[['ANO', 'Total Estabelecimentos', 'Total Aves']])

# Etapa 2: Visualizar a Variação Temporal do Número de Estabelecimentos e Aves
st.subheader("Evolução do Número de Estabelecimentos ao Longo do Tempo")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='ANO', y='Total Estabelecimentos', data=df_temporal, marker="o", ax=ax)
ax.set_title('Evolução do Número de Estabelecimentos')
ax.set_xlabel('Ano')
ax.set_ylabel('Total de Estabelecimentos')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Evolução do Número de Aves ao Longo do Tempo")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.lineplot(x='ANO', y='Total Aves', data=df_temporal, marker="o", ax=ax2)
ax2.set_title('Evolução do Número de Aves')
ax2.set_xlabel('Ano')
ax2.set_ylabel('Total de Aves')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)

# Etapa 3: Visualizar a Variação Temporal dos Tipos de Exploração
if 'SIST_CRIA' in df.columns:
    st.subheader("Proporção dos Tipos de Exploração ao Longo do Tempo")
    df_sist_cria = df.groupby(['ANO', 'SIST_CRIA']).size().unstack(fill_value=0)
    df_sist_cria_prop = df_sist_cria.div(df_sist_cria.sum(axis=1), axis=0) * 100

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    df_sist_cria_prop.plot(kind='bar', stacked=True, ax=ax3)
    ax3.set_title('Proporção dos Tipos de Exploração ao Longo do Tempo')
    ax3.set_xlabel('Ano')
    ax3.set_ylabel('Proporção (%)')
    plt.xticks(rotation=45)
    ax3.legend(title='Tipo de Exploração', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(fig3)
else:
    st.info("Coluna 'SIST_CRIA' não encontrada para análise temporal dos tipos de exploração.")
