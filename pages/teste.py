import pandas as pd
import plotly.express as px

# Dados simulados
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

# Top 5, 5 do meio, Bottom 5
top_5 = freq_estab_total.head(5)
bottom_5 = freq_estab_total.tail(5)
middle_5 = freq_estab_total[~freq_estab_total.index.isin(top_5.index.union(bottom_5.index))].head(5)

# Combinação dos dados
df_combined_ranks = pd.concat([
    top_5.rename('Quantidade').reset_index().assign(Categoria='Top 5 Maiores'),
    middle_5.rename('Quantidade').reset_index().assign(Categoria='5 do Meio'),
    bottom_5.rename('Quantidade').reset_index().assign(Categoria='Top 5 Menores')
]).rename(columns={'index': 'Unidade Federativa'})

df_combined_ranks['Categoria'] = pd.Categorical(df_combined_ranks['Categoria'], 
                                                categories=['Top 5 Maiores', '5 do Meio', 'Top 5 Menores'],
                                                ordered=True)

# Gráfico
fig_ranks = px.bar(
    df_combined_ranks,
    x='Unidade Federativa',
    y='Quantidade',
    color='Categoria',
    title='Ranking de Estabelecimentos Avícolas por Estado (Top 5, Meio 5, Bottom 5)',
    labels={'Unidade Federativa': 'Estado', 'Quantidade': 'Quantidade de Estabelecimentos'},
    color_discrete_map={
        'Top 5 Maiores': 'green',
        '5 do Meio': 'orange',
        'Top 5 Menores': 'red'
    },
    template='plotly_white'
)

fig_ranks.show()
