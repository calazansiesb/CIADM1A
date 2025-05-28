import streamlit as st
import pandas as pd
import plotly.express as px

# Substitua pela URL RAW correta do seu arquivo CSV no GitHub
GITHUB_CSV_URL = 'https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv'

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

# Carregamento dos dados
df = load_data(GITHUB_CSV_URL)

if df.empty:
    st.warning("Não foi possível carregar os dados. Verifique a URL e o conteúdo do arquivo CSV.")
    st.stop() # Interrompe a execução se os dados não puderem ser carregados

# Verifique as colunas do seu DataFrame.
# Se a coluna com os nomes das unidades federativas tiver outro nome, altere 'NOM_TERR' para o nome correto.
# Certifique-se de que 'E_CRIA_GAL' também esteja presente.
if 'NOM_TERR' not in df.columns:
    st.error("A coluna 'NOM_TERR' não foi encontrada no DataFrame. Por favor, verifique o nome da coluna no seu CSV.")
    st.stop()
if 'E_CRIA_GAL' not in df.columns:
    st.error("A coluna 'E_CRIA_GAL' não foi encontrada no DataFrame. Por favor, verifique o nome da coluna no seu CSV.")
    st.stop()

# Garantir que E_CRIA_GAL é numérica
# Se 'thousands='.' não funcionar perfeitamente, podemos fazer uma conversão manual aqui:
# df['E_CRIA_GAL'] = pd.to_numeric(df['E_CRIA_GAL'].astype(str).str.replace('.', '', regex=False), errors='coerce').fillna(0)


st.header('🌎 Distribuição por Unidade Federativa')

# Lista oficial dos 26 estados + DF
estados_brasil = [
    'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás',
    'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco',
    'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina',
    'São Paulo', 'Sergipe', 'Tocantins'
]

# Mapeamento de estados para regiões
regioes_estados = {
    'Norte': ['Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocantins'],
    'Nordeste': ['Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe'],
    'Centro-Oeste': ['Distrito Federal', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul'],
    'Sudeste': ['Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo'],
    'Sul': ['Paraná', 'Rio Grande do Sul', 'Santa Catarina']
}

# Inverter o dicionário para mapear estado -> região
estado_para_regiao = {estado: regiao for regiao, estados in regioes_estados.items() for estado in estados}

# Adicionar 'Regiao' ao DataFrame principal para uso posterior, se necessário
# Certifique-se que df['NOM_TERR'] está limpo e corresponde aos nomes de estado
df['Regiao'] = df['NOM_TERR'].map(estado_para_regiao)

# Filtrar apenas estados do Brasil
df_uf = df[df['NOM_TERR'].isin(estados_brasil)].copy() # Use .copy() para evitar SettingWithCopyWarning

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
    df_filtered_by_region = df_filtered_by_region[df_filtered_by_region['NOM_TERR'].isin(estados_da_regiao)]
    title_sufix = f' na Região {selected_region}'

# Calcular a SOMA de E_CRIA_GAL APENAS para os estados filtrados
if not df_filtered_by_region.empty:
    freq_estab_por_uf_filtered = df_filtered_by_region.groupby('NOM_TERR')['E_CRIA_GAL'].sum().sort_values(ascending=False)
    df_plot_filtered = freq_estab_por_uf_filtered.rename_axis('Unidade Federativa').reset_index(name='Quantidade de Galináceos')
else:
    df_plot_filtered = pd.DataFrame(columns=['Unidade Federativa', 'Quantidade de Galináceos']) # DataFrame vazio se não houver dados


# === Gráfico Dinâmico de Distribuição por UF ===
st.subheader(f'Quantidade de Galináceos por Estado{title_sufix}')
if not df_plot_filtered.empty:
    fig2 = px.bar(
        df_plot_filtered,
        x='Unidade Federativa',
        y='Quantidade de Galináceos', # Alterado para 'Quantidade de Galináceos'
        title=f'Quantidade de Galináceos por Unidade Federativa{title_sufix}', # Título alterado
        labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'}, # Rótulos alterados
        color='Unidade Federativa',  # Cor única para cada estado!
        color_discrete_sequence=px.colors.qualitative.Set2  # Paleta amigável
    )
    fig2.update_layout(
        xaxis_tickangle=-35,
        showlegend=False,
        bargap=0.15,
        plot_bgcolor='white',
        font=dict(size=14)
    )
    # Adicionar o valor exato no topo de cada barra
    fig2.update_traces(texttemplate='%{y:.2s}', textposition='outside') # Formato para grandes números
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info(f"Não há dados para a região '{selected_region}' com os estados filtrados.")

st.markdown('---')

# Restante do código para os gráficos dos 3 maiores, 3 do meio e 3 menores (com alterações de rótulos)
st.header('Análise Detalhada da Quantidade de Galináceos por Estado (Brasil)') # Título alterado

# Garantir que temos dados suficientes para essas análises
if len(df_plot_total) >= 3:
    # Top 3 Maiores
    top_3 = df_plot_total.head(3)
    fig_top_3 = px.bar(
        top_3,
        x='Unidade Federativa',
        y='Quantidade de Galináceos', # Alterado para 'Quantidade de Galináceos'
        title='Top 3 Maiores Estados em Quantidade de Galináceos', # Título alterado
        labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'}, # Rótulos alterados
        color='Unidade Federativa',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_top_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
    fig_top_3.update_traces(texttemplate='%{y:.2s}', textposition='outside') # Adiciona o valor
    st.plotly_chart(fig_top_3, use_container_width=True)

    # 3 do Meio
    if len(df_plot_total) >= 6: # Precisamos de pelo menos 6 estados para ter 3 do meio razoavelmente definidos
        middle_start = len(df_plot_total) // 2 - 1 # Ajuste para pegar 3 do meio
        if middle_start < 0: middle_start = 0 # Garante que não seja negativo
        middle_3 = df_plot_total.iloc[middle_start : middle_start + 3]

        fig_middle_3 = px.bar(
            middle_3,
            x='Unidade Federativa',
            y='Quantidade de Galináceos', # Alterado para 'Quantidade de Galináceos'
            title='3 Estados do Meio em Quantidade de Galináceos', # Título alterado
            labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'}, # Rótulos alterados
            color='Unidade Federativa',
            color_discrete_sequence=px.colors.qualitative.D3
        )
        fig_middle_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
        fig_middle_3.update_traces(texttemplate='%{y:.2s}', textposition='outside') # Adiciona o valor
        st.plotly_chart(fig_middle_3, use_container_width=True)
    else:
        st.info("Não há estados suficientes para exibir os '3 do meio'. São necessários pelo menos 6 estados.")


    # 3 Menores
    bottom_3 = df_plot_total.tail(3)
    fig_bottom_3 = px.bar(
        bottom_3,
        x='Unidade Federativa',
        y='Quantidade de Galináceos', # Alterado para 'Quantidade de Galináceos'
        title='Top 3 Menores Estados em Quantidade de Galináceos', # Título alterado
        labels={'Unidade Federativa': 'Estado', 'Quantidade de Galináceos': 'Quantidade de Galináceos'}, # Rótulos alterados
        color='Unidade Federativa',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    fig_bottom_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
    fig_bottom_3.update_traces(texttemplate='%{y:.2s}', textposition='outside') # Adiciona o valor
    st.plotly_chart(fig_bottom_3, use_container_width=True)

else:
    st.warning("Não há dados suficientes para gerar os gráficos dos 3 maiores, 3 do meio e 3 menores estados.")
