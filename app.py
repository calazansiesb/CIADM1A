import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="1. Distribuição Geográfica da Produção Avícola:",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('Análise de Galináceos no Brasil')
st.info("Use o menu lateral à esquerda para acessar as outras páginas.")

# Função para limpar valores numéricos
def clean_numeric_value(x):
    if isinstance(x, str):
        cleaned_value = ''.join(c for c in x if c.isdigit() or c == '.' or c == ',')
        cleaned_value = cleaned_value.replace(',', '.', 1)
        return cleaned_value
    return x

# Carregar o DataFrame
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado.")
    st.stop()

# Garantir que E_SUBS e E_COMERC são numéricos
for col in ['E_SUBS', 'E_COMERC']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Limpar a coluna 'GAL_TOTAL'
if 'GAL_TOTAL' in df.columns:
    df['GAL_TOTAL'] = df['GAL_TOTAL'].apply(clean_numeric_value)
    df['GAL_TOTAL'] = df['GAL_TOTAL'].replace('', np.nan)
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')

# =======================
# 1. Gráfico Interativo - Proporção dos Sistemas de Criação
# =======================

st.header('Proporção dos Sistemas de Criação')
st.info(
    'Pergunta: Qual é a proporção de estabelecimentos dedicados a cada tipo de exploração\n'
    '(corte, postura, reprodução, misto)? Existe algum tipo de exploração predominante em certas regiões?'
)

if 'SIST_CRIA' in df.columns:
    freq_sistema_cria = df['SIST_CRIA'].value_counts()
    prop_sistema_cria = df['SIST_CRIA'].value_counts(normalize=True) * 100

    st.subheader('Frequência dos Sistemas de Criação')
    st.dataframe(freq_sistema_cria)

    fig_pie = px.pie(df, names="SIST_CRIA", title="Proporção dos Sistemas de Criação", hover_data=["SIST_CRIA"])
    st.plotly_chart(fig_pie)

# =======================
# 2. Gráfico Interativo - Distribuição dos Sistemas de Criação por UF
# =======================
st.header('Distribuição dos Sistemas de Criação por UF')

if 'NOM_TERR' in df.columns and 'SIST_CRIA' in df.columns:
    dist_sistema_cria_por_uf = df.groupby('NOM_TERR')['SIST_CRIA'].value_counts(normalize=True).reset_index()
    dist_sistema_cria_por_uf.columns = ['UF', 'SIST_CRIA', 'Proporção']

    fig_bar = px.bar(
        dist_sistema_cria_por_uf, x="UF", y="Proporção", color="SIST_CRIA", 
        title="Distribuição dos Sistemas de Criação por UF", 
        labels={"UF": "Unidade Federativa", "Proporção": "Percentual"},
        hover_data=["SIST_CRIA", "Proporção"]
    )

    st.plotly_chart(fig_bar)

# =======================
# 3. Gráfico Interativo - Análise da Mão de Obra no Setor Avícola
# =======================
st.header('Análise da Mão de Obra no Setor Avícola')
st.header('Estatísticas Descritivas dos Trabalhadores')
if 'N_TRAB_PERM' in df.columns and 'N_TRAB_TEMP' in df.columns:
    st.subheader('Trabalhadores Permanentes')
    st.write(df['N_TRAB_PERM'].describe())
    st.subheader('Trabalhadores Temporários')
    st.write(df['N_TRAB_TEMP'].describe())
    if 'N_TRAB_TOTAL' in df.columns:
        st.subheader('Total de Trabalhadores')
        st.write(df['N_TRAB_TOTAL'].describe())

st.header('Correlação entre Tamanho do Estabelecimento e Número de Trabalhadores')
if 'GAL_TOTAL' in df.columns and 'N_TRAB_TOTAL' in df.columns:
    # Garantir que as colunas são numéricas
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')
    cor = df[['GAL_TOTAL', 'N_TRAB_TOTAL']].corr().loc['GAL_TOTAL', 'N_TRAB_TOTAL']
    st.write(f'A correlação entre número total de aves e número de trabalhadores é: **{cor:.2f}**')

    # Visualização
    fig = px.scatter(
        df, x='GAL_TOTAL', y='N_TRAB_TOTAL',
        labels={'GAL_TOTAL': 'Total de Aves', 'N_TRAB_TOTAL': 'Total de Trabalhadores'},
        title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
        trendline="ols"  # Adiciona linha de tendência
    )
    st.plotly_chart(fig)

if 'N_TRAB_TOTAL' in df.columns and 'GAL_TOTAL' in df.columns:
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')

    fig_scatter = px.scatter(
        df, x="GAL_TOTAL", y="N_TRAB_TOTAL", title="Tamanho do Estabelecimento vs. Número de Trabalhadores", 
        labels={"GAL_TOTAL": "Total de Galináceos", "N_TRAB_TOTAL": "Número de Trabalhadores"},
        hover_data=["GAL_TOTAL", "N_TRAB_TOTAL"]
    )
    
    st.plotly_chart(fig_scatter)

# =======================
# 4. Gráfico Interativo - Média de GAL_TOTAL por Grupo de Tamanho
# =======================
st.header('Média de GAL_TOTAL por Grupo de Tamanho')
st.info(
    '''Exploração: Analisar a frequência dos tipos de instalações. Agrupar os estabelecimentos por 
    faixas de número de aves e verificar a proporção de cada tipo de instalação em cada faixa. '''
)
if 'Q_DZ_PROD' in df.columns and 'GAL_TOTAL' in df.columns:
    df['Q_DZ_PROD'] = pd.to_numeric(df['Q_DZ_PROD'], errors='coerce')
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')

    df.loc[df['Q_DZ_PROD'].notna(), 'TAMANHO_GRUPO'] = pd.qcut(df.loc[df['Q_DZ_PROD'].notna(), 'Q_DZ_PROD'], q=3, labels=['Pequeno', 'Médio', 'Grande'])

    variavel_por_grupo = df.groupby('TAMANHO_GRUPO')['GAL_TOTAL'].mean().reset_index()
    
    fig_bar_size = px.bar(
        variavel_por_grupo, x="TAMANHO_GRUPO", y="GAL_TOTAL", title="Média de GAL_TOTAL por Grupo de Tamanho",
        labels={"TAMANHO_GRUPO": "Grupo de Tamanho", "GAL_TOTAL": "Média de Galináceos"},
        hover_data=["GAL_TOTAL"]
    )
    
    st.plotly_chart(fig_bar_size)
