import pandas as pd
import plotly.express as px
import streamlit as st

# Simulando DataFrame (substitua isso pelo seu DataFrame real)
data = {
    'NOM_TERR': [
        'São Paulo', 'Minas Gerais', 'Paraná', 'Bahia', 'Santa Catarina',
        'Rio Grande do Sul', 'Goiás', 'Pernambuco', 'Ceará', 'Pará',
        'Mato Grosso', 'Espírito Santo', 'Amazonas', 'Roraima', 'Amapá'
    ]
}
df_uf = pd.DataFrame(data)

# Frequência dos estados
freq_estab_total = df_uf['NOM_TERR'].value_counts()

# Top 5, Bottom 5 e os 5 do meio
top_5 = freq_estab_total.head(5)
bottom_5 = freq_estab_total.tail(5)
middle_5 = freq_estab_total[
    ~freq_estab_total.index.isin(top_5.index.union(bottom_5.index))
].head(5)

# Monta DataFrame final
def monta_categoria(df, categoria):
    return df.rename('Quantidade').reset_index().rename(
        columns={'index': 'Unidade Federativa'}
    ).assign(Categoria=categoria)

df_top = monta_categoria(top_5, 'Top 5 Maiores')
df_middle = monta_categoria(middle_5, '5 do Meio')
df_bottom = monta_categoria(bottom_5, 'Top 5 Menores')

df_combined_ranks = pd.concat([df_top, df_middle, df_bottom])

# Ordena categorias
df_combined_ranks['Categoria'] = pd.Categorical(
    df_combined_ranks['Categoria'],
    categories=['Top 5 Maiores', '5 do Meio', 'Top 5 Menores'],
    ordered=True
)

# DEBUG VISUAL
st.write("DataFrame usado no gráfico:")
st.dataframe(df_combined_ranks)

# Cria o gráfico
fig_ranks = px.bar(
    df_combined_ranks,
    x='Unidade Federativa',
    y='Quantidade',
    color='Categoria',
    title='Ranking de Estabelecimentos por Estado',
    labels={'Unidade Federativa': 'Estado', 'Quantidade': 'Qtd de Estabelecimentos'},
    color_discrete_map={
        'Top 5 Maiores': 'green',
        '5 do Meio': 'orange',
        'Top 5 Menores': 'red'
    },
    template='plotly_white'
)

st.plotly_chart(fig_ranks)
