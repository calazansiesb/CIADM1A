import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- 0. CONFIGURAÇÃO DA PÁGINA STREAMLIT (DEVE SER A PRIMEIRA COISA) ---
# Define o layout da página, o título que aparece na aba do navegador e o ícone.
st.set_page_config(layout="wide", page_title="Análise de Galináceos", icon="🐔")

# --- 1. Inicializar st.session_state para os seletores ---
# Isso garante que as chaves existam antes de serem lidas ou modificadas por widgets.
# Pre-define os valores iniciais para evitar erros na primeira execução ou ao recarregar.
if 'scatter_x' not in st.session_state:
    st.session_state.scatter_x = None
if 'scatter_y' not in st.session_state:
    st.session_state.scatter_y = None
if 'scatter_color' not in st.session_state:
    st.session_state.scatter_color = "Nenhuma"
if 'scatter_filter_col' not in st.session_state:
    st.session_state.scatter_filter_col = "Nenhuma"
# O multiselect (valor_filtro) não precisa de um default inicial aqui, pois ele gerencia seu próprio estado
# e pode ser preenchido com todas as opções por padrão mais adiante no código.

# --- 2. Carregar e Pré-processar os Dados ---
# URL do arquivo CSV no GitHub (versão raw)
url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

# Decorador @st.cache_data armazena em cache o resultado da função.
# Isso melhora a performance, pois os dados só são carregados e processados uma vez,
# a menos que a URL ou o código da função mude.
@st.cache_data
def load_data(url):
    try:
        # Tenta carregar com codificação 'latin1', comum para CSVs brasileiros.
        df = pd.read_csv(url, sep=";", encoding="latin1")
    except UnicodeDecodeError:
        # Se 'latin1' falhar, tenta com 'utf-8'.
        df = pd.read_csv(url, sep=";", encoding="utf-8")
    
    # Processamento para garantir que colunas numéricas sejam tratadas corretamente.
    for col in df.columns:
        # Verifica se a coluna é de tipo 'object' (geralmente strings).
        if df[col].dtype == 'object':
            try:
                # Tenta substituir vírgulas por pontos para conversão de números decimais.
                # O .astype(str) garante que a operação .str.replace funcione mesmo se houver NaNs ou outros tipos.
                df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                # Converte para numérico, transformando erros em NaN (Not a Number).
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except ValueError:
                # Se não conseguir converter para numérico, a coluna permanece como string.
                pass
    
    return df

# Carrega os dados uma vez para o aplicativo.
df = load_data(url)

# --- 3. Dicionário de Descrições das Variáveis ---
# Mapeia nomes de colunas (códigos) para descrições mais amigáveis.
descricao_variaveis = {
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

# --- 4. Filtro de Colunas Numéricas e Categóricas ---
# Identifica colunas numéricas no DataFrame.
df_numerico = df.select_dtypes(include=[np.number])
colunas_numericas = df_numerico.columns.tolist()

# Prepara as opções de colunas para colorir o gráfico.
# Inclui colunas não numéricas com poucos valores únicos (categóricas)
# e colunas numéricas com poucos valores únicos (binárias, por exemplo).
colunas_para_cor = [col for col in df.columns if col not in colunas_numericas and df[col].nunique() < 20] + \
                   [col for col in colunas_numericas if df[col].nunique() < 20 and df[col].isin([0, 1]).all()]
# Cria um mapeamento para exibir as descrições amigáveis nos seletores.
colunas_para_cor_map = {col: descricao_variaveis.get(col, col) for col in colunas_para_cor}
# Adiciona uma opção para não usar cor.
colunas_para_cor_map["Nenhuma"] = "Nenhuma"

# --- 5. Configuração da Interface do Streamlit (títulos principais) ---
st.title("🐔 Análise de Dados de Galináceos")
st.markdown("Explore as relações entre diferentes métricas usando gráficos de dispersão e mapas de calor.")

# --- 6. Abas para Organização ---
# Cria abas para organizar o conteúdo do aplicativo.
tab1, tab2, tab3 = st.tabs(["Gráfico de Dispersão Personalizado", "Sugestões de Análise", "Matriz de Correlação"])

# --- 7. Função para Atualizar o Estado da Sessão ---
# Esta função é chamada pelos botões de sugestão.
# Ela define os valores de st.session_state e força um rerun do aplicativo.
def set_scatter_vars(x, y, color, filter_col_name=None):
    st.session_state.scatter_x = x
    st.session_state.scatter_y = y
    st.session_state.scatter_color = color
    st.session_state.scatter_filter_col = filter_col_name if filter_col_name else "Nenhuma"
    st.rerun() # Recarrega a página para aplicar as mudanças nos seletores.

# --- 8. Conteúdo da Aba "Gráfico de Dispersão Personalizado" ---
with tab1:
    st.header("Gráfico de Dispersão Personalizado")

    # Colunas para organizar os seletores.
    col1, col2 = st.columns(2)
    with col1:
        # Seletor para o eixo X.
        # O 'index' é definido lendo de st.session_state, garantindo que o valor persista
        # quando uma sugestão é clicada.
        default_x_index = 0
        if st.session_state.scatter_x in colunas_numericas:
            default_x_index = colunas_numericas.index(st.session_state.scatter_x)

        col_x = st.selectbox(
            "Selecione a métrica para o eixo X:", 
            options=colunas_numericas, 
            index=default_x_index,
            format_func=lambda x: descricao_variaveis.get(x, x),
            key='scatter_x' # A chave vincula o widget ao st.session_state.
        )
    with col2:
        # Seletor para o eixo Y.
        default_y_index = 0
        if st.session_state.scatter_y in colunas_numericas:
            default_y_index = colunas_numericas.index(st.session_state.scatter_y)

        col_y = st.selectbox(
            "Selecione a métrica para o eixo Y:", 
            options=colunas_numericas, 
            index=default_y_index,
            format_func=lambda y: descricao_variaveis.get(y, y),
            key='scatter_y'
        )

    # Seletor para a cor dos pontos.
    default_color_index = 0
    if st.session_state.scatter_color in colunas_para_cor_map:
        default_color_index = list(colunas_para_cor_map.keys()).index(st.session_state.scatter_color)

    cor_selecionada = st.selectbox(
        "Colorir pontos por:", 
        options=list(colunas_para_cor_map.keys()),
        index=default_color_index,
        format_func=lambda x: colunas_para_cor_map.get(x, x),
        key='scatter_color'
    )
    # Define a coluna a ser usada para a cor no Plotly; 'None' se "Nenhuma" for selecionada.
    plot_color = cor_selecionada if cor_selecionada != "Nenhuma" else None

    # Seletor para filtro por coluna.
    # Colunas para filtro: 'object' (categóricas) ou numéricas com poucos valores únicos.
    colunas_para_filtro_opcoes = ["Nenhuma"] + [
        col for col in df.columns 
        if df[col].dtype == 'object' or (df[col].nunique() < 50 and df[col].nunique() > 1)
    ]
    default_filter_index = 0
    if st.session_state.scatter_filter_col in colunas_para_filtro_opcoes:
        default_filter_index = colunas_para_filtro_opcoes.index(st.session_state.scatter_filter_col)

    filtro_col = st.selectbox(
        "Filtrar por:",
        options=colunas_para_filtro_opcoes,
        index=default_filter_index,
        format_func=lambda x: descricao_variaveis.get(x, x) if x != "Nenhuma" else "Nenhum Filtro",
        key='scatter_filter_col'
    )

    # Aplica o filtro selecionado.
    df_filtrado_scatter = df.copy()
    if filtro_col != "Nenhuma":
        opcoes_filtro = df[filtro_col].unique().tolist()
        # O multiselect permite selecionar vários valores para o filtro.
        valor_filtro = st.multiselect(
            f"Selecione valores para {descricao_variaveis.get(filtro_col, filtro_col)}:",
            options=opcoes_filtro,
            default=opcoes_filtro, # Todos selecionados por padrão.
            key='scatter_filter_val'
        )
        if valor_filtro:
            df_filtrado_scatter = df_filtrado_scatter[df_filtrado_scatter[filtro_col].isin(valor_filtro)]

    # Cria e exibe o gráfico de dispersão.
    if col_x and col_y:
        # Remove NaNs das colunas X e Y para o gráfico para evitar pontos vazios.
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

# --- 9. Conteúdo da Aba "Sugestões de Análise" ---
with tab2:
    st.header("Sugestões de Análise Pré-definidas")
    st.markdown("Clique em uma sugestão para carregar automaticamente as variáveis no gráfico de dispersão na aba **'Gráfico de Dispersão Personalizado'**.")

    # Blocos de sugestão com botões que chamam set_scatter_vars.
    st.subheader("1. Produção vs. Comercialização")
    st.write(f"**Eixo X:** {descricao_variaveis.get('GAL_TOTAL', 'GAL_TOTAL')}  \n**Eixo Y:** {descricao_variaveis.get('V_GAL_VEND', 'V_GAL_VEND')}  \n**Cores:** {descricao_variaveis.get('NIV_TERR', 'NIV_TERR')}  \n**Filtro:** {descricao_variaveis.get('NOM_TERR', 'NOM_TERR')}")
    if st.button("Ver Sugestão 1", key="sugestao1"):
        set_scatter_vars('GAL_TOTAL', 'V_GAL_VEND', 'NIV_TERR', 'NOM_TERR')
    st.markdown("---")

    st.subheader("2. Orientação Técnica vs. Produtividade")
    st.write(f"**Eixo X:** {descricao_variaveis.get('E_RECEBE_ORI', 'E_RECEBE_ORI')}  \n**Eixo Y:** {descricao_variaveis.get('VTP_AGRO', 'VTP_AGRO')}  \n**Cores:** {descricao_variaveis.get('E_ORI_GOV', 'E_ORI_GOV')}  \n**Filtro:** {descricao_variaveis.get('SIST_CRIA', 'SIST_CRIA')}")
    if st.button("Ver Sugestão 2", key="sugestao2"):
        set_scatter_vars('E_RECEBE_ORI', 'VTP_AGRO', 'E_ORI_GOV', 'SIST_CRIA')
    st.markdown("---")

    st.subheader("3. Área de Pastagem vs. Criação de Galináceos")
    st.write(f"**Eixo X:** {descricao_variaveis.get('A_PAST_PLANT', 'A_PAST_PLANT')}  \n**Eixo Y:** {descricao_variaveis.get('GAL_ENG', 'GAL_ENG')}  \n**Cores:** {descricao_variaveis.get('E_ASSOC_COOP', 'E_ASSOC_COOP')}  \n**Filtro:** {descricao_variaveis.get('CL_GAL', 'CL_GAL')}")
    if st.button("Ver Sugestão 3", key="sugestao3"):
        set_scatter_vars('A_PAST_PLANT', 'GAL_ENG', 'E_ASSOC_COOP', 'CL_GAL')
    st.markdown("---")

    st.subheader("4. Venda de Ovos vs. Número de Poedeiras")
    st.write(f"**Eixo X:** {descricao_variaveis.get('GAL_POED', 'GAL_POED')}  \n**Eixo Y:** {descricao_variaveis.get('Q_DZ_VEND', 'Q_DZ_VEND')}  \n**Cores:** {descricao_variaveis.get('E_COMERC', 'E_COMERC')}  \n**Filtro:** {descricao_variaveis.get('E_AGRIFAM', 'E_AGRIFAM')}")
    if st.button("Ver Sugestão 4", key="sugestao4"):
        set_scatter_vars('GAL_POED', 'Q_DZ_VEND', 'E_COMERC', 'E_AGRIFAM')
    st.markdown("---")

    st.subheader("5. Investimento vs. Receita Total")
    st.write(f"**Eixo X:** {descricao_variaveis.get('E_FINANC', 'E_FINANC')}  \n**Eixo Y:** {descricao_variaveis.get('RECT_AGRO', 'RECT_AGRO')}  \n**Cores:** {descricao_variaveis.get('E_FINANC_COOP', 'E_FINANC_COOP')}  \n**Filtro:** {descricao_variaveis.get('E_CNPJ', 'E_CNPJ')}")
    if st.button("Ver Sugestão 5", key="sugestao5"):
        set_scatter_vars('E_FINANC', 'RECT_AGRO', 'E_FINANC_COOP', 'E_CNPJ')
    st.markdown("---")

# --- 10. Conteúdo da Aba "Matriz de Correlação" ---
with tab3:
    st.header("Análise da Matriz de Correlação")

    # Verifica se há colunas numéricas para calcular a correlação.
    if not df_numerico.empty:
        matriz_correlacao = df_numerico.corr()

        st.subheader("Mapa de Calor da Matriz de Correlação")
        # Cria um mapa de calor interativo da matriz de correlação usando Plotly Express.
        fig_heatmap = px.imshow(
            matriz_correlacao,
            text_auto=True, # Exibe os valores de correlação nas células.
            aspect="auto",
            color_continuous_scale="RdBu_r", # Escala de cores (vermelho-azul, invertida).
            title="Mapa de Calor da Matriz de Correlação",
            labels=dict(color="Correlação")
        )
        fig_heatmap.update_traces(textfont_size=10) # Ajusta o tamanho da fonte no mapa de calor.
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.subheader("Top 10 Maiores Correlações (valores absolutos)")
        corr_abs = matriz_correlacao.abs() # Pega o valor absoluto das correlações.
        # Seleciona apenas a parte superior da matriz (sem a diagonal) para evitar duplicações.
        tri_superior = corr_abs.where(np.triu(np.ones(corr_abs.shape), k=1).astype(bool))
        pares_correlacao = tri_superior.stack() # Transforma a matriz em uma Series de pares de correlação.
        melhores_correlacoes_geral = pares_correlacao.sort_values(ascending=False) # Ordena do maior para o menor.

        # --- CORREÇÃO DO ERRO 'NotImplementedError: isna is not defined for MultiIndex' ---
        # A nova abordagem evita o .rename() direto no MultiIndex.
        # 1. Converte a Series (com MultiIndex) em um DataFrame com colunas normais.
        df_temp_corr = melhores_correlacoes_geral.reset_index()
        df_temp_corr.columns = ['Variavel1', 'Variavel2', 'Correlacao']

        # 2. Mapeia os nomes das variáveis para suas descrições amigáveis.
        # O .fillna() garante que se a descrição não for encontrada, o nome original da variável seja mantido.
        df_temp_corr['Variavel1_desc'] = df_temp_corr['Variavel1'].map(descricao_variaveis).fillna(df_temp_corr['Variavel1'])
        df_temp_corr['Variavel2_desc'] = df_temp_corr['Variavel2'].map(descricao_variaveis).fillna(df_temp_corr['Variavel2'])

        # 3. Re-cria a Series com o novo MultiIndex usando as descrições amigáveis.
        melhores_correlacoes_com_desc = df_temp_corr.set_index(['Variavel1_desc', 'Variavel2_desc'])['Correlacao']
        # --- FIM DA CORREÇÃO ---

        st.write(melhores_correlacoes_com_desc.head(10))

        st.subheader("Correlação com uma Variável Específica")
        variavel_alvo_corr = st.selectbox(
            "Selecione uma variável para ver suas correlações:",
            options=colunas_numericas,
            format_func=lambda x: descricao_variaveis.get(x, x),
            key='corr_target_var'
        )

        # Exibe as correlações para a variável selecionada.
        if variavel_alvo_corr:
            # Exclui a correlação da variável com ela mesma (que é sempre 1).
            correlacoes_alvo = matriz_correlacao[variavel_alvo_corr].drop(variavel_alvo_corr).sort_values(ascending=False)
            # Mapeia os nomes das colunas para suas descrições amigáveis.
            correlacoes_alvo_com_desc = correlacoes_alvo.rename(
                index=lambda x: descricao_variaveis.get(x, x)
            )
            st.write(correlacoes_alvo_com_desc)
    else:
        st.warning("Não há colunas numéricas suficientes para calcular a matriz de correlação. Verifique o pré-processamento dos dados.")
