import streamlit as st
import pandas as pd

st.title('Exemplo de análise de CSV no Streamlit')
df = pd.read_csv('testepyntonstremlit.csv', sep=';')  # ajuste o separador se necessário

st.write('Primeiras linhas do arquivo:')
st.dataframe(df.head())

st.subheader('Resumo estatístico')
st.write(df.describe())