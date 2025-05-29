import streamlit as st
import plotly.express as px
import plotly.graph_objects as go # Para o mapa de calor
import pandas as pd
import numpy as np

# --- 0. CONFIGURAÇÃO DA PÁGINA STREAMLIT (DEVE SER A PRIMEIRA COISA) ---
st.set_page_config(layout="wide", page_title="Análise de Galináceos")

# --- 1. Carregar e Pré-processar os Dados ---
# URL do arquivo CSV no GitHub (versão raw)
url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

@st.cache_data # Armazena em cache o carregamento dos dados para melhor performance
def load_data(url):
    try:
        # Tenta com latin1 primeiro, que é comum para CSVs brasileiros
        df = pd.read_csv(url, sep=";", encoding="latin1")
    except UnicodeDecodeError:
        # Se latin1 falhar, tenta com utf-8
        df = pd.read_csv(url, sep=";", encoding="utf-8")
    
    # Tentativa de converter colunas que deveriam ser numéricas
    # para numéricas, tratando possíveis vírgulas como decimais e NaNs
    for col in df.columns:
        if df[col].dtype == 'object': # Se a coluna é de texto (object)
            try:
                # Substituir vírgula por ponto para conversão para float
                df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce') # 'coerce' transforma erros em NaN
            except ValueError:
                pass # Não faz nada se não conseguir converter, mantém como texto
    
    return df

df = load_data(url)

# --- 2. Dicionário de Descrições das Variáveis ---
descricao_variaveis = {
    # ... (seu dicionário de descrições das variáveis) ...
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

# --- 3. Filtro de Colunas Numéricas e Categóricas ---
df_numerico = df.select_dtypes(include=[np.number])
colunas_numericas = df_numerico.columns.tolist()

colunas_para_cor = [col for col in df.columns if col not in colunas_numericas and df[col].nunique() < 20] + \
                   [col for col in colunas_numericas if df[col].nunique() < 20 and df[col].isin([0, 1]).all()]
colunas_para_cor_map = {col: descricao_variaveis.get(col, col) for col in colunas_para_cor}
colunas_para_cor_map["Nenhuma"] = "Nenhuma" # Opção para não usar cor (corrigido para "Nenhuma")

# --- 4. Configuração da Interface do Streamlit (títulos principais) ---
st.title("🐔 Análise de Dados de Galináceos")
st.markdown("Explore as relações entre diferentes métricas usando gráficos de dispersão e mapas de calor.")

# --- 5. Abas para Organização ---
tab1, tab2, tab3 = st.tabs(["Gráfico de Dispersão Personalizado", "Sugestões de Análise", "Matriz de Correlação"])

with tab1:
    st.header("Gráfico de Dispersão Personalizado")

    col1, col2 = st.columns(2)
    with col1:
        # Seletores para métricas (apenas numéricas para X e Y)
        col_x = st.selectbox(
            "Selecione a métrica para o eixo X:", 
            options=colunas_numericas, 
            format_func=lambda x: descricao_variaveis.get(x, x),
            key='scatter_x'
        )
    with col2:
        col_y = st.selectbox(
            "Selecione a métrica para o eixo Y:", 
            options=colunas_numericas, 
            format_func=lambda y: descricao_variaveis.get(y, y),
            key='scatter_y'
        )

    # Seletor para cor (colunas categóricas ou numéricas discretas)
    cor_selecionada = st.selectbox(
        "Colorir pontos por:", 
        options=list(colunas_para_cor_map.keys()),
        format_func=lambda x: colunas_para_cor_map.get(x, x),
        key='scatter_color'
    )
    # Se a opção for "Nenhuma", defina plot_color como None para o plotly
    plot_color = colunas_para_cor_map[cor_selecionada] if cor_selecionada != "Nenhuma" else None

    # Seletor para filtro de NOM_TERR ou NIV_TERR
    # Filtrar apenas colunas que são de tipo 'object' ou que tem poucos valores únicos (potencialmente categóricas)
    colunas_para_filtro_opcoes = ["Nenhuma"] + [
        col for col in df.columns 
        if df[col].dtype == 'object' or (df[col].nunique() < 50 and df[col].nunique() > 1)
    ]
    filtro_col = st.selectbox(
        "Filtrar por:",
        options=colunas_para_filtro_opcoes,
        format_func=lambda x: descricao_variaveis.get(x, x) if x != "Nenhuma" else "Nenhum Filtro",
        key='scatter_filter_col'
    )

    df_filtrado_scatter = df.copy()
    if filtro_col != "Nenhuma":
        opcoes_filtro = df[filtro_col].unique().tolist()
        valor_filtro = st.multiselect(
            f"Selecione valores para {descricao_variaveis.get(filtro_col, filtro_col)}:",
            options=opcoes_filtro,
            default=opcoes_filtro, # Seleciona todos por padrão
            key='scatter_filter_val'
        )
        if valor_filtro:
            df_filtrado_scatter = df_filtrado_scatter[df_filtrado_scatter[filtro_col].isin(valor_filtro)]

    # Criar o gráfico de dispersão
    if col_x and col_y:
        # Removendo NaNs para o gráfico de dispersão para evitar pontos isolados
        df_plot = df_filtrado_scatter.dropna(subset=[col_x, col_y])

        fig_scatter = px.scatter(
            df_plot, # Usar df_plot
            x=col_x,
            y=col_y,
            color=plot_color,
            title=f"Correlação entre {descricao_variaveis.get(col_x, col_x)} e {descricao_variaveis.get(col_y, col_y)}",
            labels={col_x: descricao_variaveis.get(col_x, col_x), col_y: descricao_variaveis.get(col_y, col_y)},
            hover_name="NOM_TERR" if "NOM_TERR" in df.columns else None, # Mostra o nome do território no hover
            height=500
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Selecione as métricas para os eixos X e Y para gerar o gráfico.")

with tab2:
    st.header("Sugestões de Análise Pré-definidas")
    st.markdown("Clique em uma sugestão para carregar automaticamente as variáveis no gráfico de dispersão na aba **'Gráfico de Dispersão Personalizado'**.")

    # Função para setar as variáveis no estado da sessão
    # O filtro_val precisa ser tratado manualmente no multiselect default,
    # então por enquanto não passaremos o valor exato, apenas a coluna.
    def set_scatter_vars(x, y, color, filter_col_name=None):
        st.session_state.scatter_x = x
        st.session_state.scatter_y = y
        st.session_state.scatter_color = color
        if filter_col_name: # Se houver uma coluna de filtro sugerida
            st.session_state.scatter_filter_col = filter_col_name
        else: # Caso contrário, resetar o filtro
             st.session_state.scatter_filter_col = "Nenhuma"
        st.rerun() # Recarregar a página para aplicar as mudanças nos seletores

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
        # Ajustar tamanho do texto para melhor visualização em células pequenas
        fig_heatmap.update_traces(textfont_size=10)
        st.plotly_chart(fig_heatmap, use_container_width=True)

        st.subheader("Top 10 Maiores Correlações (valores absolutos)")
        corr_abs = matriz_correlacao.abs()
        tri_superior = corr_abs.where(np.triu(np.ones(corr_abs.shape), k=1).astype(bool))
        pares_correlacao = tri_superior.stack()
        melhores_correlacoes_geral = pares_correlacao.sort_values(ascending=False)

        # Mapear os nomes das colunas para suas descrições amigáveis
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
            # Exclui a correlação da variável com ela mesma (que é 1)
            correlacoes_alvo = matriz_correlacao[variavel_alvo_corr].drop(variavel_alvo_corr).sort_values(ascending=False)
            # Mapear os nomes das colunas para suas descrições amigáveis
            correlacoes_alvo_com_desc = correlacoes_alvo.rename(
                index=lambda x: descricao_variaveis.get(x, x)
            )
            st.write(correlacoes_alvo_com_desc)
    else:
        st.warning("Não há colunas numéricas suficientes para calcular a matriz de correlação. Verifique o pré-processamento dos dados.")
