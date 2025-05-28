import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import unicodedata

st.title('Análise de Galináceos no Brasil (IBGE 2017)')
st.markdown("---")

# =============================================
# 1. Carregar Dados Reais do GitHub
# =============================================
st.header("📂 Carregando Dados Reais")

csv_url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

try:
    df = pd.read_csv(csv_url, sep=';')
    df.columns = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8').strip().upper() for col in df.columns]
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# =============================================
# Limpeza da coluna SIST_CRIA (se existir)
# =============================================
if 'SIST_CRIA' in df.columns:
    df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()
    mapeamento_sistemas = {
        '1-SIST_POC': 'Produtores de ovos para consumo',
        '2-SIST_POI': 'Produtores de ovos para incubação',
        '3-SIST_PFC': 'Produtores de frangos de corte',
        '4-Outro': 'Outros produtores'
    }
    df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)

# Mostrar registros aleatórios
st.subheader("Visualização dos Dados")
with st.expander("🔎 Ver registros aleatórios do conjunto de dados"):
    st.dataframe(df.sample(10))

# =============================================
# Distribuição por Unidade Federativa
# =============================================
st.header('🌎 Distribuição de Estabelecimentos por Unidade Federativa')

if 'NOM_TERR' in df.columns:
    regioes = {
        'Norte': ['Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocantins'],
        'Nordeste': ['Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe'],
        'Sudeste': ['Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo'],
        'Sul': ['Paraná', 'Rio Grande do Sul', 'Santa Catarina'],
        'Centro-Oeste': ['Distrito Federal', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul']
    }

    estado_para_regiao = {estado: regiao for regiao, estados in regioes.items() for estado in estados}
    df['REGIAO'] = df['NOM_TERR'].map(estado_para_regiao)
    df_uf = df[df['NOM_TERR'].isin(sum(regioes.values(), []))].copy()

    todas_regioes = ['Todas as Regiões'] + list(regioes.keys())
    selected_region = st.selectbox("Selecione uma Região:", todas_regioes)

    if selected_region != 'Todas as Regiões':
        df_filtered_by_region = df_uf[df_uf['REGIAO'] == selected_region]
        region_title = f'Número de Estabelecimentos por Estado na Região {selected_region}'
    else:
        df_filtered_by_region = df_uf
        region_title = 'Número de Estabelecimentos por Estado em Todas as Regiões'

    freq_estab_por_uf = df_filtered_by_region['NOM_TERR'].value_counts().sort_values(ascending=False)
    df_plot_uf = freq_estab_por_uf.rename_axis('Unidade Federativa').reset_index(name='Quantidade')

    fig_uf_geral = px.bar(
        df_plot_uf,
        x='Unidade Federativa',
        y='Quantidade',
        title=region_title,
        labels={'Unidade Federativa': 'Estado', 'Quantidade': 'Quantidade de Estabelecimentos'},
        color='Unidade Federativa',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_uf_geral.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        bargap=0.15,
        plot_bgcolor='white',
        font=dict(size=14),
        hovermode="x unified"
    )
    st.plotly_chart(fig_uf_geral, use_container_width=True)

    # =============================================
    # Ranking: Top 5, Meio 5, Bottom 5
    # =============================================
    st.header('📈 Desempenho dos Estados: Top, Médios e Menores Produtores')

    freq_estab_total = df_uf['NOM_TERR'].value_counts().sort_values(ascending=False)
    top_5 = freq_estab_total.head(5)
    bottom_5 = freq_estab_total[~freq_estab_total.index.isin(top_5.index)].tail(5)
    remaining = freq_estab_total.drop(top_5.index.union(bottom_5.index))
    middle_5 = remaining.head(5)

    df_combined_ranks = pd.concat([
        top_5.rename('Quantidade').reset_index().assign(Categoria='Top 5 Maiores'),
        middle_5.rename('Quantidade').reset_index().assign(Categoria='5 do Meio'),
        bottom_5.rename('Quantidade').reset_index().assign(Categoria='Top 5 Menores')
    ]).rename(columns={'index': 'Unidade Federativa'})

    df_combined_ranks['Categoria'] = pd.Categorical(
        df_combined_ranks['Categoria'],
        categories=['Top 5 Maiores', '5 do Meio', 'Top 5 Menores'],
        ordered=True
    )

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
    fig_ranks.update_layout(
        xaxis_tickangle=-45,
        bargap=0.15,
        plot_bgcolor='white',
        font=dict(size=14),
        hovermode="x unified",
        legend_title_text='Categorias de Estados'
    )
    st.plotly_chart(fig_ranks, use_container_width=True)

else:
    st.warning("A coluna 'NOM_TERR' não foi encontrada no dataset para a análise de Unidade Federativa.")

# =============================================
# Rodapé
# =============================================
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base nos dados reais do IBGE 2017*  
📅 *Atualizado em Maio 2025*
""")
