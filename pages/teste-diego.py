import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- 0. CONFIGURAÇÃO DA PÁGINA STREAMLIT (DEVE SER A PRIMEIRA COISA) ---
st.set_page_config(layout="wide", page_title="Análise de Galináceos")

# --- Inicializar st.session_state para os seletores ---
# Isso garante que as chaves existam antes de serem lidas ou modificadas
if 'scatter_x' not in st.session_state:
    st.session_state.scatter_x = None # Valor inicial padrão
if 'scatter_y' not in st.session_state:
    st.session_state.scatter_y = None # Valor inicial padrão
if 'scatter_color' not in st.session_state:
    st.session_state.scatter_color = "Nenhuma" # Valor inicial padrão
if 'scatter_filter_col' not in st.session_state:
    st.session_state.scatter_filter_col = "Nenhuma" # Valor inicial padrão
# Para o multiselect, o padrão é todos selecionados, então não precisamos setar um default aqui

# URL do arquivo CSV no GitHub (versão raw)
url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url, sep=";", encoding="latin1")
    except UnicodeDecodeError:
        df = pd.read_csv(url, sep=";", encoding="utf-8")
    
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except ValueError:
                pass
    return df

df = load_data(url)

# Dicionário de descrições das variáveis (mantido como está)
descricao_variaveis = {
    # ... seu dicionário ...
    "SIST_CRIA": "Sistema de criação",
    "NIV_TERR": "Nível das unidades territoriais",
    "COD_TERR": "Código das unidades territoriais",
    "NOM_TERR": "Nome das unidades territoriais",
    "GAL_TOTAL": "Total efetivo de galináceos",
    "V_GAL_VEND": "Valor dos galináceos vendidos",
    "E_RECEBE_ORI": "Estabelecimentos com orientação técnica",
    "VTP_AGRO": "Valor total da produção agropecuária",
    "E_ORI_GOV": "Orientação do governo",
    "A_PAST_PLANT": "Área de pastagem plantada",
    "GAL_ENG": "Galináceos para engorda",
    "E_ASSOC_COOP": "Associação a cooperativas",
    "CL_GAL": "Classe de cabeças de galináceos",
    "GAL_POED": "Total de poedeiras",
    "Q_DZ_VEND": "Ovos vendidos em dúzias",
    "E_COMERC": "Estabelecimentos comerciais",
    "E_AGRIFAM": "Agricultura familiar",
    "E_FINANC": "Estabelecimentos com investimento",
    "RECT_AGRO": "Receita total agropecuária",
    "E_FINANC_COOP": "Investimento de cooperativas",
    "E_CNPJ": "Estabelecimentos com CNPJ",
    "E_SUBS": "Produção para consumo próprio",
    "E_DAP": "Possui DAP/PRONAF",
    "N_TRAB_TOTAL": "Total de trabalhadores",
    "E_PRODUTOR": "Produtor individual",
    "GAL_MATR": "Total de matrizes",
    "GAL_VEND": "Galináceos vendidos",
    "E_ORI_INTEG": "Orientação de integradoras",
    "E_GAL_MATR": "Estabelecimentos com matrizes"
}

# Filtro de Colunas Numéricas e Categóricas (mantido como está)
df_numerico = df.select_dtypes(include=[np.number])
colunas_numericas = df_numerico.columns.tolist()

colunas_para_cor = [col for col in df.columns if col not in colunas_numericas and df[col].nunique() < 20] + \
                   [col for col in colunas_numericas if df[col].nunique() < 20 and df[col].isin([0, 1]).all()]
colunas_para_cor_map = {col: descricao_variaveis.get(col, col) for col in colunas_para_cor}
colunas_para_cor_map["Nenhuma"] = "Nenhuma"

st.title("🐔 Análise de Dados de Galináceos")
st.markdown("Explore as relações entre diferentes métricas usando gráficos de dispersão e mapas de calor.")

tab1, tab2, tab3 = st.tabs(["Gráfico de Dispersão Personalizado", "Sugestões de Análise", "Matriz de Correlação"])

# --- Função para setar as variáveis no estado da sessão (agora sem rerun direto aqui) ---
def set_scatter_vars(x, y, color, filter_col_name=None):
    st.session_state.scatter_x = x
    st.session_state.scatter_y = y
    st.session_state.scatter_color = color
    st.session_state.scatter_filter_col = filter_col_name if filter_col_name else "Nenhuma"
    # Se você quiser que o filtro seja pré-selecionado, isso é mais complexo
    # e pode envolver st.session_state.scatter_filter_val, mas requer que
    # o default do multiselect leia de session_state.
    # Por enquanto, apenas setamos a coluna de filtro.


with tab1:
    st.header("Gráfico de Dispersão Personalizado")

    col1, col2 = st.columns(2)
    with col1:
        # Usar value=st.session_state.scatter_x para ler do estado
        col_x = st.selectbox(
            "Selecione a métrica para o eixo X:", 
            options=colunas_numericas, 
            index=colunas_numericas.index(st.session_state.scatter_x) if st.session_state.scatter_x in colunas_numericas else 0, # Definir índice
            format_func=lambda x: descricao_variaveis.get(x, x),
            key='scatter_x'
        )
    with col2:
        # Usar value=st.session_state.scatter_y para ler do estado
        col_y = st.selectbox(
            "Selecione a métrica para o eixo Y:", 
            options=colunas_numericas, 
            index=colunas_numericas.index(st.session_state.scatter_y) if st.session_state.scatter_y in colunas_numericas else 0, # Definir índice
            format_func=lambda y: descricao_variaveis.get(y, y),
            key='scatter_y'
        )

    # Seletor para cor
    # Precisa encontrar o índice da cor selecionada no mapeamento
    default_color_index = 0
    if st.session_state.scatter_color in colunas_para_cor_map:
        default_color_index = list(colunas_para_cor_map.keys()).index(st.session_state.scatter_color)

    cor_selecionada = st.selectbox(
        "Colorir pontos por:", 
        options=list(colunas_para_cor_map.keys()),
        index=default_color_index, # Ler do estado da sessão
        format_func=lambda x: colunas_para_cor_map.get(x, x),
        key='scatter_color'
    )
    plot_color = colunas_para_cor_map[cor_selecionada] if cor_selecionada != "Nenhuma" else None

    # Seletor para filtro
    colunas_para_filtro_opcoes = ["Nenhuma"] + [
        col for col in df.columns 
        if df[col].dtype == 'object' or (df[col].nunique() < 50 and df[col].nunique() > 1)
    ]
    # Definir o índice padrão para o seletor de filtro
    default_filter_index = 0
    if st.session_state.scatter_filter_col in colunas_para_filtro_opcoes:
        default_filter_index = colunas_para_filtro_opcoes.index(st.session_state.scatter_filter_col)

    filtro_col = st.selectbox(
        "Filtrar por:",
        options=colunas_para_filtro_opcoes,
        index=default_filter_index, # Ler do estado da sessão
        format_func=lambda x: descricao_variaveis.get(x, x) if x != "Nenhuma" else "Nenhum Filtro",
        key='scatter_filter_col'
    )

    df_filtrado_scatter = df.copy()
    if filtro_col != "Nenhuma":
        opcoes_filtro = df[filtro_col].unique().tolist()
        # Aqui, o default do multiselect ainda é todos, você teria que gerenciar
        # st.session_state.scatter_filter_val para que os valores selecionados mudassem
        valor_filtro = st.multiselect(
            f"Selecione valores para {descricao_variaveis.get(filtro_col, filtro_col)}:",
            options=opcoes_filtro,
            default=opcoes_filtro, # Manter todos selecionados por padrão, ou ajustar com session_state
            key='scatter_filter_val'
        )
        if valor_filtro:
            df_filtrado_scatter = df_filtrado_scatter[df_filtrado_scatter[filtro_col].isin(valor_filtro)]

    if col_x and col_y:
        df_plot = df_filtrado_scatter.dropna(subset=[col_x, col_y])

        fig_scatter = px.scatter(
            df_plot,
            x=col_x,
            y=col_y,
            color=plot_color,
            title=f"Correlação entre {descricao_variaveis.get(col_x, col_x)} e {descricao_variaveis.get(col_y, col_y)}",
            labels={col_x: descricao_variaveis.get(col_x, col_x), col_y: descricao_variaveis.get(col_y, col_y)},
            hover_name="NOM_TERR" if "NOM_TERR" in df.columns else None,
            height=500
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Selecione as métricas para os eixos X e Y para gerar o gráfico.")

with tab2:
    st.header("Sugestões de Análise Pré-definidas")
    st.markdown("Clique em uma sugestão para carregar automaticamente as variáveis no gráfico de dispersão na aba **'Gráfico de Dispersão Personalizado'**.")

    # A função set_scatter_vars agora apenas define o estado
    # O rerun é para que o Streamlit re-execute e os seletores leiam o novo estado.

    st.subheader("1. Produção vs. Comercialização")
    st.write(f"**Eixo X:** {descricao_variaveis.get('GAL_TOTAL', 'GAL_TOTAL')}  \n**Eixo Y:** {descricao_variaveis.get('V_GAL_VEND', 'V_GAL_VEND')}  \n**Cores:** {descricao_variaveis.get('NIV_TERR', 'NIV_TERR')}  \n**Filtro:** {descricao_variaveis.get('NOM_TERR', 'NOM_TERR')}")
    if st.button("Ver Sugestão 1", key="sugestao1"):
        set_scatter_vars('GAL_TOTAL', 'V_GAL_VEND', 'NIV_TERR', 'NOM_TERR')
        st.rerun() # Dispara rerun após a alteração do session_state
    st.markdown("---")

    st.subheader("2. Orientação Técnica vs. Produtividade")
    st.write(f"**Eixo X:** {descricao_variaveis.get('E_RECEBE_ORI', 'E_RECEBE_ORI')}  \n**Eixo Y:** {descricao_variaveis.get('VTP_AGRO', 'VTP_AGRO')}  \n**Cores:** {descricao_variaveis.get('E_ORI_GOV', 'E_ORI_GOV')}  \n**Filtro:** {descricao_variaveis.get('SIST_CRIA', 'SIST_CRIA')}")
    if st.button("Ver Sugestão 2", key="sugestao2"):
        set_scatter_vars('E_RECEBE_ORI', 'VTP_AGRO', 'E_ORI_GOV', 'SIST_CRIA')
        st.rerun()
    st.markdown("---")

    st.subheader("3. Área de Pastagem vs. Criação de Galináceos")
    st.write(f"**Eixo X:** {descricao_variaveis.get('A_PAST_PLANT', 'A_PAST_PLANT')}  \n**Eixo Y:** {descricao_variaveis.get('GAL_ENG', 'GAL_ENG')}  \n**Cores:** {descricao_variaveis.get('E_ASSOC_COOP', 'E_ASSOC_COOP')}  \n**Filtro:** {descricao_variaveis.get('CL_GAL', 'CL_GAL')}")
    if st.button("Ver Sugestão 3", key="sugestao3"):
        set_scatter_vars('A_PAST_PLANT', 'GAL_ENG', 'E_ASSOC_COOP', 'CL_GAL')
        st.rerun()
    st.markdown("---")

    st.subheader("4. Venda de Ovos vs. Número de Poedeiras")
    st.write(f"**Eixo X:** {descricao_variaveis.get('GAL_POED', 'GAL_POED')}  \n**Eixo Y:** {descricao_variaveis.get('Q_DZ_VEND', 'Q_DZ_VEND')}  \n**Cores:** {descricao_variaveis.get('E_COMERC', 'E_COMERC')}  \n**Filtro:** {descricao_variaveis.get('E_AGRIFAM', 'E_AGRIFAM')}")
    if st.button("Ver Sugestão 4", key="sugestao4"):
        set_scatter_vars('GAL_POED', 'Q_DZ_VEND', 'E_COMERC', 'E_AGRIFAM')
        st.rerun()
    st.markdown("---")

    st.subheader("5. Investimento vs. Receita Total")
    st.write(f"**Eixo X:** {descricao_variaveis.get('E_FINANC', 'E_FINANC')}  \n**Eixo Y:** {descricao_variaveis.get('RECT_AGRO', 'RECT_AGRO')}  \n**Cores:** {descricao_variaveis.get('E_FINANC_COOP', 'E_FINANC_COOP')}  \n**Filtro:** {descricao_variaveis.get('E_CNPJ', 'E_CNPJ')}")
    if st.button("Ver Sugestão 5", key="sugestao5"):
        set_scatter_vars('E_FINANC', 'RECT_AGRO', 'E_FINANC_COOP', 'E_CNPJ')
        st.rerun()
    st.markdown("---")


with tab3:
    st.header("Análise da Matriz de Correlação")

    if not df_numerico.empty:
        matriz_correlacao = df_numerico.corr()

        st.subheader("Mapa de Calor da Matriz de Correlação")
        fig_heatmap = px.imshow(
            matriz_correlacao,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Mapa de Calor da Matriz de Correlação",
            labels=dict(color="Correlação")
        )
        fig_heatmap.update_traces(textfont_size=10)
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.subheader("Top 10 Maiores Correlações (valores absolutos)")
        corr_abs = matriz_correlacao.abs()
        tri_superior = corr_abs.where(np.triu(np.ones(corr_abs.shape), k=1).astype(bool))
        pares_correlacao = tri_superior.stack()
        melhores_correlacoes_geral = pares_correlacao.sort_values(ascending=False)

        melhores_correlacoes_com_desc = melhores_correlacoes_geral.rename(
            index=lambda x: (descricao_variaveis.get(x[0], x[0]), descricao_variaveis.get(x[1], x[1]))
        )
        st.write(melhores_correlacoes_com_desc.head(10))

        st.subheader("Correlação com uma Variável Específica")
        variavel_alvo_corr = st.selectbox(
            "Selecione uma variável para ver suas correlações:",
            options=colunas_numericas,
            format_func=lambda x: descricao_variaveis.get(x, x),
            key='corr_target_var'
        )

        if variavel_alvo_corr:
            correlacoes_alvo = matriz_correlacao[variavel_alvo_corr].drop(variavel_alvo_corr).sort_values(ascending=False)
            correlacoes_alvo_com_desc = correlacoes_alvo.rename(
                index=lambda x: descricao_variaveis.get(x, x)
            )
            st.write(correlacoes_alvo_com_desc)
    else:
        st.warning("Não há colunas numéricas suficientes para calcular a matriz de correlação. Verifique o pré-processamento dos dados.")
