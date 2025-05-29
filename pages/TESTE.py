import streamlit as st
import pandas as pd
import plotly.express as px

# URL do arquivo CSV
CSV_URL = 'https://github.com/calazansiesb/CIADM1A/GALINACEOS.csv'

st.set_page_config(layout="wide")

st.title('Dashboard de Análise de Estabelecimentos de Galináceos')

# Carregar os dados
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url, encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        return pd.DataFrame()

df = load_data(CSV_URL)

# =============================================
# 5. Distribuição por Porte dos Estabelecimentos
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

if not df.empty and 'NOM_CL_GAL' in df.columns:
    freq_portes = df['NOM_CL_GAL'].value_counts().sort_index()
    fig4 = px.bar(
        x=freq_portes.index,
        y=freq_portes.values,
        title='Distribuição de Estabelecimentos por Porte (Faixas IBGE)',
        labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
        color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    st.plotly_chart(fig4, use_container_width=True)

    with st.expander("💡 Interpretação do Gráfico de Distribuição por Porte dos Estabelecimentos"):
        st.info("""
        **🏭 Análise da Distribuição por Porte dos Estabelecimentos**

        O gráfico mostra a quantidade de estabelecimentos distribuídos por diferentes faixas de porte (definidas pelo IBGE):

        - As faixas intermediárias, especialmente entre **201 e 5.000 aves**, concentram os maiores números de estabelecimentos, sugerindo predominância de produtores de médio porte no setor.
        - Pequenos produtores ("De 1 a 100" e "De 101 a 200") também são numerosos, mas em menor quantidade que as faixas intermediárias.
        - Faixas extremas ("De 100.001 e mais" e "Sem galináceos em 30.09.2017") apresentam participação reduzida, indicando que grandes produtores e estabelecimentos temporariamente inativos são minoria.
        - A categoria "Total" pode representar registros agregados ou casos não classificados nas demais faixas, devendo ser analisada com cautela.
        - A presença de estabelecimentos "Sem galináceos" reforça a importância de considerar sazonalidade ou inatividade temporária.

        **Conclusão:**
        - O perfil da produção avícola brasileira é fortemente marcado pela presença de estabelecimentos de porte intermediário, com pequena participação de grandes produtores e um contingente relevante de pequenos estabelecimentos. Isso tem implicações para políticas públicas, estratégias de mercado e apoio ao setor.
        """)
else:
    st.warning("A coluna 'NOM_CL_GAL' não foi encontrada no dataset ou o dataset está vazio. Verifique a URL e o conteúdo do arquivo CSV.")
