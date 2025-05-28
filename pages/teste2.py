import streamlit as st
import plotly.express as px
import pandas as pd

# Carregar os dados (substituir 'seu_arquivo.csv' pelo nome do seu arquivo de dados)
df = pd.read_csv("GALINACEOS.csv")

# Configurar a interface do Streamlit
st.title("Gráfico de Dispersão - Correlação entre Métricas")

# Seletores
col_x = st.selectbox("Selecione a métrica para o eixo X:", df.columns)
col_y = st.selectbox("Selecione a métrica para o eixo Y:", df.columns)
regiao = st.selectbox("Selecione a Região:", df["Regiao"].unique())
ano = st.selectbox("Selecione o Ano:", df["ANO"].unique())

# Filtrar os dados com base na seleção do usuário
df_filtrado = df[(df["Regiao"] == regiao) & (df["ANO"] == ano)]

# Criar o gráfico de dispersão
fig = px.scatter(
    df_filtrado, 
    x=col_x, 
    y=col_y, 
    color="NOM_TERR",
    title=f"Correlação entre {col_x} e {col_y} para {regiao} no ano {ano}",
    labels={col_x: col_x, col_y: col_y}
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)
