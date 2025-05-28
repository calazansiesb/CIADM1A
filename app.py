import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da página
st.set_page_config(page_title="Análise de Galináceos", layout="wide")

# 2. Título
st.title("Análise de Galináceos no Brasil - IBGE 2017")

# 3. Carregar dados
csv_url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"
try:
    df = pd.read_csv(csv_url, sep=';')
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# 4. Mostrar amostra dos dados
st.subheader("Visualização dos dados")
st.dataframe(df.sample(10))

# 5. Gráfico simples de barras - Exemplo: Quantidade por Unidade Federativa
st.subheader("Número de Estabelecimentos por Estado")

# Filtrar só os estados (exemplo)
estados_brasil = [
    'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás',
    'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco',
    'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina',
    'São Paulo', 'Sergipe', 'Tocantins'
]

df_uf = df[df['NOM_TERR'].isin(estados_brasil)]

# Contar quantidade por estado
contagem = df_uf['NOM_TERR'].value_counts().sort_values(ascending=False)
df_contagem = contagem.rename_axis('Estado').reset_index(name='Quantidade')

# Plot
fig = px.bar(
    df_contagem,
    x='Estado',
    y='Quantidade',
    title='Quantidade de Estabelecimentos por Estado',
    labels={'Quantidade': 'Quantidade', 'Estado': 'Estado'},
    color='Estado',
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig, use_container_width=True)
