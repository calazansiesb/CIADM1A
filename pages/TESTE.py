import pandas as pd
import streamlit as st # Se você estiver usando no Streamlit

# URL do arquivo CSV
CSV_URL = 'https://github.com/calazansiesb/CIADM1A/GALINACEOS.csv'

# Carregar os dados, especificando o separador como ponto e vírgula
@st.cache_data # Mantenha o cache se estiver usando Streamlit
def load_data(url):
    try:
        # AQUI ESTÁ A MUDANÇA PRINCIPAL: adicione sep=';'
        df = pd.read_csv(url, sep=';', encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        return pd.DataFrame()

df = load_data(CSV_URL)

# Agora, para verificar se funcionou, você pode imprimir as colunas novamente
if not df.empty:
    st.write("Colunas após correção:", df.columns.tolist())
    st.dataframe(df.head()) # Exibir as primeiras linhas para verificar
else:
    st.warning("O DataFrame está vazio, o carregamento falhou.")

# O restante do seu código para gerar gráficos viria aqui
# Por exemplo:
# if 'NOM_CL_GAL' in df.columns:
#     # ... seu código para gerar o gráfico de barras
