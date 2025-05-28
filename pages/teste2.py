import streamlit as st
import plotly.express as px
import pandas as pd

# URL do arquivo CSV no GitHub (versão raw)
url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

# Carregar os dados corretamente
df = pd.read_csv(url, sep=";", encoding="utf-8")

# Exibir as primeiras linhas para depuração
st.write("Prévia dos dados:", df.head())

# Configurar a interface do Streamlit
st.title("Gráfico de Dispersão - Correlação entre Métricas")

# Exibir os nomes das colunas disponíveis
st.write("Colunas disponíveis:", df.columns)

# Seletores para métricas
col_x = st.selectbox("Selecione a métrica para o eixo X:", df.columns)
col_y = st.selectbox("Selecione a métrica para o eixo Y:", df.columns)

# Seletores para região e ano (verificando existência das colunas)
if "NIV_TERR" in df.columns:
    regiao = st.selectbox("Selecione a Região:", df["NIV_TERR"].unique())
else:
    regiao = None
    st.error("Coluna 'NIV_TERR' não encontrada no arquivo.")

if "ANO" in df.columns:
    ano = st.selectbox("Selecione o Ano:", df["ANO"].unique())
else:
    ano = None
    st.error("Coluna 'ANO' não encontrada no arquivo.")

# Filtrar os dados com base na seleção do usuário
if regiao and ano:
    df_filtrado = df[(df["NIV_TERR"] == regiao) & (df["ANO"] == ano)]
elif regiao:
    df_filtrado = df[df["NIV_TERR"] == regiao]
else:
    df_filtrado = df

# Criar o gráfico de dispersão
fig = px.scatter(
    df_filtrado, 
    x=col_x, 
    y=col_y, 
    color="NOM_TERR" if "NOM_TERR" in df.columns else None,
    title=f"Correlação entre {col_x} e {col_y} para {regiao} no ano {ano}" if ano else f"Correlação entre {col_x} e {col_y} para {regiao}",
    labels={col_x: col_x, col_y: col_y}
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

