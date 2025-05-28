import pandas as pd
import plotly.express as px
import streamlit as st

# Simulando dados
data = {
    'NOM_TERR': [
        'SP', 'MG', 'RJ', 'BA', 'RS',
        'PR', 'SC', 'PE', 'CE', 'PA',
        'MT', 'ES', 'AM', 'RR', 'AP'
    ]
}
df = pd.DataFrame(data)

# Contagem por estado
frequencias = df['NOM_TERR'].value_counts()

# Top 5
top5 = frequencias.head(5)
bottom5 = frequencias.tail(5)
meio = frequencias[~frequencias.index.isin(top5.index.union(bottom5.index))].head(5)

def to_df(freq, categoria):
    return freq.rename("Quantidade").reset_index().rename(columns={"index": "Unidade Federativa"}).assign(Categoria=categoria)

df_top = to_df(top5, "Top 5 Maiores")
df_meio = to_df(meio, "5 do Meio")
df_bottom = to_df(bottom5, "Top 5 Menores")

df_combined_ranks = pd.concat([df_top, df_meio, df_bottom])

df_combined_ranks["Categoria"] = pd.Categorical(
    df_combined_ranks["Categoria"],
    categories=["Top 5 Maiores", "5 do Meio", "Top 5 Menores"],
    ordered=True
)

# Debug visual
st.subheader("🔍 Dados enviados ao gráfico")
st.dataframe(df_combined_ranks)
st.write(df_combined_ranks.dtypes)
st.write(df_combined_ranks.isnull().sum())

# Gráfico
fig_ranks = px.bar(
    df_combined_ranks,
    x="Unidade Federativa",
    y="Quantidade",
    color="Categoria",
    title="Ranking por Estado",
    color_discrete_map={
        "Top 5 Maiores": "green",
        "5 do Meio": "orange",
        "Top 5 Menores": "red"
    },
    template="plotly_white"
)

st.plotly_chart(fig_ranks)
