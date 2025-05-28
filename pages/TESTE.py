import streamlit as st
import pandas as pd
import plotly.express as px
import requests # Importar para carregar o GeoJSON de forma mais robusta
import json # Usado em load_geojson, mas requests.json() geralmente já retorna o dicionário
import unicodedata # Para normalização de texto (remover acentos)
import re # Para normalização de texto (opcional, mas bom para strip e lower)

# Substitua pela URL RAW correta do seu arquivo CSV no GitHub
GITHUB_CSV_URL = 'https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv'

# URL para o arquivo GeoJSON dos estados do Brasil (exemplo)
# ATENÇÃO: Esta URL pode não ser permanente ou pode precisar de autenticação dependendo da fonte.
# Recomenda-se baixar este arquivo e colocá-lo em seu repositório ou encontrar uma fonte mais estável.
GEOJSON_BR_STATES_URL = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'

# Função auxiliar para normalizar nomes (remover acentos e converter para minúsculas)
def normalize_state_name(name):
    if isinstance(name, str):
        # Remove acentos e caracteres especiais, depois converte para minúsculas e remove espaços extras
        normalized = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        return normalized.strip().lower()
    return name # Retorna o valor original se não for string (ex: NaN)

@st.cache_data # Usar st.cache_data para cache de dados
def load_data(url):
    try:
        # Adicionei sep=';' e encoding='latin1' pois é comum em CSVs brasileiros
        # Adicionei thousands='.' para tratar o ponto como separador de milhares na leitura de números
        df = pd.read_csv(url, sep=';', encoding='latin1', thousands='.')
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
                feature['properties']['name_original'] = feature['properties']['name'] # Mantém o nome original
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
    st.stop() # Interrompe a execução se os dados não puderem ser carregados

if geojson_data is None:
    st.warning("Não foi possível carregar os dados geográficos. O mapa não será exibido.")
    # Não st.stop() aqui, para que o restante do app ainda funcione.


# Verifique as colunas do seu DataFrame.
if 'NOM_TERR' not in df.columns:
    st.error("A coluna 'NOM_TERR' não foi encontrada no DataFrame. Por favor, verifique o nome da coluna no seu CSV.")
    st.stop()
if 'E_CRIA_GAL' not in df.columns:
    st.error("A coluna 'E_CRIA_GAL' não foi encontrada no DataFrame. Por favor, verifique o nome da coluna no seu CSV.")
    st.stop()

# --- Normalização da coluna NOM_TERR no DataFrame ---
# Isso garante que NOM_TERR e os nomes do GeoJSON estejam no mesmo formato para matching.
df['NOM_TERR_NORMALIZED'] = df['NOM_TERR'].apply(normalize_state_name)


st.header('🌎 Distribuição por Unidade Federativa')

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
# Usa a lista `estados_brasil` original para mapear as regiões e então normaliza as chaves do dicionário para uso posterior
estado_para_regiao_normalized = {normalize_state_name(estado): regiao for regiao, estados in regioes_estados.items() for estado in estados}

# Adicionar 'Regiao' ao DataFrame principal (usando o nome normalizado para o mapeamento de região)
df['Regiao'] = df['NOM_TERR_NORMALIZED'].map(estado_para_regiao_normalized)

# Filtrar apenas estados do Brasil (usando a coluna normalizada e a lista normalizada)
df_uf = df[df['NOM_TERR_NORMALIZED'].isin(normalized_estados_brasil)].copy()


# Calcular a SOMA de E_CRIA_GAL por UF (para o Brasil inteiro)
freq_estab_por_uf_total = df_uf.groupby('NOM_TERR')['E_CRIA_GAL'].sum().sort_values(ascending=False)
df_plot_total = freq_estab_por_uf_total.rename_axis('Unidade Federativa').reset_index(name='Quantidade de Galináceos')

# === Seletor de Região para o Gráfico Dinâmico ===
st.subheader('Selecione a Região para Exibir no Gráfico:')
regioes_disponiveis = ['Todas as Regiões'] + list(regioes_estados.keys())
selected_region = st.selectbox('Escolha uma região', regioes_disponiveis)

# Filtragem e cálculo da frequência com base na seleção
df_filtered_by_region = df_uf.copy() # Começa com todos os estados do Brasil

title_sufix = ''
if selected_region != 'Todas as Regiões':
    estados_da_regiao = regioes_estados[selected_region]
    # Normaliza os estados da região para a filtragem
    normalized_estados_da_regiao = [normalize_state_name(e) for e in estados_da_regiao]
    df_filtered_by_region = df_filtered_by_region[df_filtered_by_region['NOM_TERR_NORMALIZED'].isin(normalized_estados_da_regiao)]
    title_sufix = f' na Região {selected_region}'

# Calcular a SOMA de E_CRIA_GAL APENAS para os estados filtrados
if not df_filtered_by_region.empty:
    freq_estab_por_uf_filtered = df_filtered_by_region.groupby('NOM_TERR')['E_CRIA_GAL'].sum().sort_values(ascending=False)
    df_plot_filtered = freq_estab_por_uf_filtered.rename_axis('Unidade Federativa').reset_index(name='Quantidade de Galináceos')
    # Adiciona a coluna normalizada para o matching no mapa
    df_plot_filtered['Unidade Federativa_Normalized_for_map'] = df_plot_filtered['Unidade Federativa'].apply(normalize_state_name)
else:
    df_plot_filtered = pd.DataFrame(columns=['Unidade Federativa', 'Quantidade de Galináceos', 'Unidade Federativa_Normalized_for_map']) # DataFrame vazio se não houver dados


# === Gráfico Dinâmico de Distribuição por UF ===
st.subheader(f'Quantidade de Galináceos por Estado{title_sufix}')
if not df_plot_filtered.empty:
    fig2 = px.bar(
        df_plot_filtered,
        x='Unidade Federativa',
        y='Quantidade de Galináceos',
        title=f'Quantidade de Galináceos por Unidade Federativa{title_sufix}',
        labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'},
        color='Unidade Federativa',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.update_layout(
        xaxis_tickangle=-35,
        showlegend=False,
        bargap=0.15,
        plot_bgcolor='white',
        font=dict(size=14)
    )
    # Adicionar o valor exato no topo de cada barra (formatado como inteiro com separador de milhares)
    fig2.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info(f"Não há dados para a região '{selected_region}' com os estados filtrados.")

st.markdown('---')

# === Mapa do Brasil por Região/Estado ===
st.header('🗺️ Mapa da Distribuição de Galináceos por Estado')

if geojson_data is not None and not df_plot_filtered.empty:
    # Use a coluna normalizada para o matching no GeoJSON
    fig_map = px.choropleth_mapbox(
        df_plot_filtered,
        geojson=geojson_data,
        locations='Unidade Federativa_Normalized_for_map', # Coluna no DataFrame com os nomes dos estados normalizados
        featureidkey="properties.name_normalized", # Caminho para o nome do estado normalizado no GeoJSON
        color='Quantidade de Galináceos', # Coluna para colorir o mapa
        color_continuous_scale="Viridis", # Escala de cor
        range_color=(df_plot_filtered['Quantidade de Galináceos'].min(), df_plot_filtered['Quantidade de Galináceos'].max()),
        mapbox_style="carto-positron", # Estilo do mapa
        zoom=3.5, # Zoom inicial
        center={"lat": -15.78, "lon": -47.93}, # Centro do mapa (Brasília)
        opacity=0.7,
        labels={'Quantidade de Galináceos':'Total de Galináceos'},
        title=f'Quantidade de Galináceos por Estado{title_sufix}'
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("Não foi possível gerar o mapa. Verifique se o GeoJSON foi carregado e se há dados filtrados.")

st.markdown('---')

# Restante do código para os gráficos dos 3 maiores, 3 do meio e 3 menores (com alterações de rótulos)
st.header('Análise Detalhada da Quantidade de Galináceos por Estado (Brasil)')

# Garantir que temos dados suficientes para essas análises
if len(df_plot_total) >= 3:
    # Top 3 Maiores
    top_3 = df_plot_total.head(3)
    fig_top_3 = px.bar(
        top_3,
        x='Unidade Federativa',
        y='Quantidade de Galináceos',
        title='Top 3 Maiores Estados em Quantidade de Galináceos',
        labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'},
        color='Unidade Federativa',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_top_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
    fig_top_3.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig_top_3, use_container_width=True)

    # 3 do Meio
    if len(df_plot_total) >= 6:
        middle_start = len(df_plot_total) // 2 - 1
        if middle_start < 0: middle_start = 0
        middle_3 = df_plot_total.iloc[middle_start : middle_start + 3]

        fig_middle_3 = px.bar(
            middle_3,
            x='Unidade Federativa',
            y='Quantidade de Galináceos',
            title='3 Estados do Meio em Quantidade de Galináceos',
            labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'},
            color='Unidade Federativa',
            color_discrete_sequence=px.colors.qualitative.D3
        )
        fig_middle_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
        fig_middle_3.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig_middle_3, use_container_width=True)
    else:
        st.info("Não há estados suficientes para exibir os '3 do meio'. São necessários pelo menos 6 estados.")


    # 3 Menores
    bottom_3 = df_plot_total.tail(3)
    fig_bottom_3 = px.bar(
        bottom_3,
        x='Unidade Federativa',
        y='Quantidade de Galináceos',
        title='Top 3 Menores Estados em Quantidade de Galináceos',
        labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'},
        color='Unidade Federativa',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    fig_bottom_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
    fig_bottom_3.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig_bottom_3, use_container_width=True)

else:
    st.warning("Não há dados suficientes para gerar os gráficos dos 3 maiores, 3 do meio e 3 menores estados.")
