import streamlit as st
import plotly.express as px
import pandas as pd

# Carregar os dados corretamente
df = pd.read_csv("seu_arquivo.csv", sep=";", encoding="utf-8")

# Configurar a interface do Streamlit
st.title("Gráfico de Dispersão - Correlação entre Métricas")

# Exibir os nomes das colunas para depuração
st.write("Colunas disponíveis:", df.columns)

# Seletores para métricas
col_x = st.selectbox("Selecione a métrica para o eixo X:", df.columns)
col_y = st.selectbox("Selecione a métrica para o eixo Y:", df.columns)

# Seletores para região e ano (validando existência das colunas)
if "NIV_TERR" in df.columns:
    regiao = st.selectbox("Selecione a Região:", df["NIV_TERR"].unique())
else:
    st.error("Coluna 'NIV_TERR' não encontrada no arquivo. Verifique a estrutura dos dados.")

if "ANO" in df.columns:
    ano = st.selectbox("Selecione o Ano:", df["ANO"].unique())
else:
    st.error("Coluna 'ANO' não encontrada no arquivo. Verifique a estrutura dos dados.")

# Filtrar os dados com base na seleção do usuário
df_filtrado = df[(df["NIV_TERR"] == regiao) & (df["ANO"] == ano)] if "ANO" in df.columns else df[df["NIV_TERR"] == regiao]

# Criar o gráfico de dispersão
fig = px.scatter(
    df_filtrado, 
    x=col_x, 
    y=col_y, 
    color="NOM_TERR" if "NOM_TERR" in df.columns else None,
    title=f"Correlação entre {col_x} e {col_y} para {regiao} no ano {ano}" if "ANO" in df.columns else f"Correlação entre {col_x} e {col_y} para {regiao}",
    labels={col_x: col_x, col_y: col_y}
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)
