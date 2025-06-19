import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import unicodedata
import re

# Substitua pela URL RAW correta do seu arquivo CSV no GitHub
GITHUB_CSV_URL = 'https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv'

# URL para o arquivo GeoJSON dos estados do Brasil (exemplo)
GEOJSON_BR_STATES_URL = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'

# --- Definição das variáveis e seus nomes de exibição ---
DATA_VARS = {
    'E_CRIA_GAL': {
        'column_name': 'E_CRIA_GAL',
        'display_title': 'Estabelecimentos de Criação de Galináceos',
        'y_axis_label': 'Número de Estabelecimentos'
    },
    'E_OVOS_PROD': {
        'column_name': 'E_OVOS_PROD',
        'display_title': 'Estabelecimentos de Produção de Ovos',
        'y_axis_label': 'Número de Estabelecimentos'
    },
    'GAL_TOTAL': {
        'column_name': 'GAL_TOTAL',
        'display_title': 'Total de Galináceos (Cabeças)',
        'y_axis_label': 'Total de Cabeças'
    }
}

# Função auxiliar para normalizar nomes (remover acentos e converter para minúsculas)
def normalize_state_name(name):
    if isinstance(name, str):
        normalized = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        return normalized.strip().lower()
    return name

@st.cache_data # Usar st.cache_data para cache de dados
def load_data(url):
    try:
        # Tentar ler com delimitador ';' e ponto como separador de milhares
        df = pd.read_csv(url, sep=';', encoding='latin1', thousands='.')

        # --- CONVERSÃO NUMÉRICA ROBUSTA PARA AS COLUNAS DE DADOS ---
        for col_key, info in DATA_VARS.items():
            col_name = info['column_name']
            if col_name in df.columns:
                # Converte para string para garantir manipulação de texto
                # Remove pontos (separadores de milhares)
                # Substitui vírgulas (se usadas como decimal) por pontos (para pd.to_numeric)
                df[col_name] = df[col_name].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                # Converte para numérico, valores inválidos viram NaN
                df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                # Preenche NaN com 0 (ou outro valor apropriado, dependendo do contexto)
                df[col_name] = df[col_name].fillna(0)
                # Converte para inteiro, pois são contagens/totais
                df[col_name] = df[col_name].astype(int)

        return df
    except FileNotFoundError:
        st.error("Erro: O arquivo não foi encontrado na URL especificada. Verifique se a URL está correta e o arquivo existe.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.error("Erro: O arquivo está vazio. Não há dados para processar.")
        return pd.DataFrame()
    except pd.errors.ParserError as e:
        st.error(f"Erro: O arquivo CSV não pôde ser analisado. Verifique o delimitador (sep=';'), a codificação (encoding='latin1') ou os separadores de números (thousands='.'). Detalhes: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar dados do GitHub. Verifique a URL ou o formato do arquivo. Detalhes: {e}")
        return pd.DataFrame()

@st.cache_data # Cache para o GeoJSON
def load_geojson(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Lança um erro para status HTTP ruins (4xx ou 5xx)
        geojson_data = response.json()

        # Normaliza os nomes dos estados dentro do GeoJSON para facilitar o matching
        for feature in geojson_data['features']:
            if 'name' in feature['properties']:
                feature['properties']['name_original'] = feature['properties']['name']
                feature['properties']['name_normalized'] = normalize_state_name(feature['properties']['name'])
        return geojson_data
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo GeoJSON: {e}. Verifique a URL ou o formato do arquivo.")
        return None

# Carregamento dos dados
df = load_data(GITHUB_CSV_URL)
geojson_data = load_geojson(GEOJSON_BR_STATES_URL)

if df.empty:
    st.warning("Não foi possível carregar os dados. Verifique a URL e o conteúdo do arquivo CSV.")
    st.stop()

if geojson_data is None:
    st.warning("Não foi possível carregar os dados geográficos. O mapa não será exibido.")


# Verifique as colunas essenciais
required_columns = ['NOM_TERR'] + [v['column_name'] for k, v in DATA_VARS.items()]
for col in required_columns:
    if col not in df.columns:
        st.error(f"A coluna '{col}' não foi encontrada no DataFrame. Por favor, verifique o nome da coluna no seu CSV.")
        st.stop()

# --- Normalização da coluna NOM_TERR no DataFrame ---
df['NOM_TERR_NORMALIZED'] = df['NOM_TERR'].apply(normalize_state_name)


st.header('🌎 Análise de Galináceos — Explore 3 Métricas por Região ou Nacional')

# Lista oficial dos 26 estados + DF
estados_brasil = [
    'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás',
    'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco',
    'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina',
    'São Paulo', 'Sergipe', 'Tocantins'
]

# Normaliza a lista de estados para a filtragem consistente
normalized_estados_brasil = [normalize_state_name(estado) for estado in estados_brasil]

# Mapeamento de estados para regiões
regioes_estados = {
    'Norte': ['Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocantins'],
    'Nordeste': ['Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe'],
    'Centro-Oeste': ['Distrito Federal', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul'],
    'Sudeste': ['Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo'],
    'Sul': ['Paraná', 'Rio Grande do Sul', 'Santa Catarina']
}

# Inverter o dicionário para mapear estado normalizado -> região
estado_para_regiao_normalized = {normalize_state_name(estado): regiao for regiao, estados in regioes_estados.items() for estado in estados}

# Adicionar 'Regiao' ao DataFrame principal (usando o nome normalizado para o mapeamento de região)
df['Regiao'] = df['NOM_TERR_NORMALIZED'].map(estado_para_regiao_normalized)

# Filtrar apenas estados do Brasil (usando a coluna normalizada e a lista normalizada)
df_uf = df[df['NOM_TERR_NORMALIZED'].isin(normalized_estados_brasil)].copy()

# --- Seletor de Variável ---
st.subheader('Selecione a Métrica para Análise:')
selected_metric_key = st.selectbox(
    'Escolha a métrica',
    options=list(DATA_VARS.keys()),
    format_func=lambda x: DATA_VARS[x]['display_title']
)
selected_metric_info = DATA_VARS[selected_metric_key]
selected_column = selected_metric_info['column_name']
selected_display_title = selected_metric_info['display_title']
selected_y_label = selected_metric_info['y_axis_label']


# Calcular a SOMA da métrica selecionada por UF (para o Brasil inteiro)
freq_data_por_uf_total = df_uf.groupby('NOM_TERR')[selected_column].sum().sort_values(ascending=False)
df_plot_total = freq_data_por_uf_total.rename_axis('Unidade Federativa').reset_index(name=selected_y_label)


# === Seletor de Região para os Gráficos Dinâmicos ===
st.subheader('Selecione a Região para Exibir nos Gráficos:')
regioes_disponiveis = ['Todas as Regiões'] + list(regioes_estados.keys())
selected_region = st.selectbox('Escolha uma região', regioes_disponiveis)

# Filtragem e cálculo da métrica com base na seleção
df_filtered_by_region = df_uf.copy()

title_sufix = ''
if selected_region != 'Todas as Regiões':
    estados_da_regiao = regioes_estados[selected_region]
    normalized_estados_da_regiao = [normalize_state_name(e) for e in estados_da_regiao]
    df_filtered_by_region = df_filtered_by_region[df_filtered_by_region['NOM_TERR_NORMALIZED'].isin(normalized_estados_da_regiao)]
    title_sufix = f' na Região {selected_region}'

# Calcular a SOMA da métrica selecionada APENAS para os estados filtrados
if not df_filtered_by_region.empty:
    freq_data_por_uf_filtered = df_filtered_by_region.groupby('NOM_TERR')[selected_column].sum().sort_values(ascending=False)
    df_plot_filtered = freq_data_por_uf_filtered.rename_axis('Unidade Federativa').reset_index(name=selected_y_label)
    # Adiciona a coluna normalizada para o matching no mapa
    df_plot_filtered['Unidade Federativa_Normalized_for_map'] = df_plot_filtered['Unidade Federativa'].apply(normalize_state_name)
else:
    df_plot_filtered = pd.DataFrame(columns=['Unidade Federativa', selected_y_label, 'Unidade Federativa_Normalized_for_map'])


# === Gráfico Dinâmico de Distribuição por UF (Barras) ===
st.subheader(f'{selected_display_title} por Estado{title_sufix}')
if not df_plot_filtered.empty:
    fig_bar_dynamic = px.bar(
        df_plot_filtered,
        x='Unidade Federativa',
        y=selected_y_label,
        title=f'{selected_display_title} por Unidade Federativa{title_sufix}',
        labels={'Unidade Federativa': 'Estado', selected_y_label: selected_y_label},
        color='Unidade Federativa',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_bar_dynamic.update_layout(
        xaxis_tickangle=-35,
        showlegend=False,
        bargap=0.15,
        plot_bgcolor='white',
        font=dict(size=14)
    )
    # Formatação para números inteiros com separadores de milhares
    fig_bar_dynamic.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig_bar_dynamic, use_container_width=True)
else:
    st.info(f"Não há dados para a região '{selected_region}' com os estados filtrados para a métrica '{selected_display_title}'.")

st.markdown('---')

# === Mapa Dinâmico do Brasil por Estado ===
st.header(f'🗺️ Mapa da Distribuição de {selected_display_title} por Estado')

if geojson_data is not None and not df_plot_filtered.empty:
    fig_map_dynamic = px.choropleth_mapbox(
        df_plot_filtered,
        geojson=geojson_data,
        locations='Unidade Federativa_Normalized_for_map',
        featureidkey="properties.name_normalized",
        color=selected_y_label,
        color_continuous_scale="Viridis",
        range_color=(df_plot_filtered[selected_y_label].min(), df_plot_filtered[selected_y_label].max()),
        mapbox_style="carto-positron",
        zoom=3.5,
        center={"lat": -15.78, "lon": -47.93},
        opacity=0.7,
        labels={selected_y_label: selected_y_label},
        title=f'{selected_display_title} por Estado{title_sufix}'
    )
    fig_map_dynamic.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map_dynamic, use_container_width=True)
else:
    st.info(f"Não foi possível gerar o mapa para '{selected_display_title}'. Verifique se o GeoJSON foi carregado e se há dados filtrados.")

st.markdown('---')
# Os gráficos dos 3 maiores, 3 do meio e 3 menores foram removidos a partir daqui.
