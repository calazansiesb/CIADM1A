# --- 0. CONFIGURAÇÃO DA PÁGINA (DEVE SER A PRIMEIRA INSTRUÇÃO) ---
import streamlit as st
st.set_page_config(
    layout="wide",
    page_title="Análise de Galináceos",
    page_icon="🐔",
    initial_sidebar_state="expanded"
)

# --- 1. IMPORTAÇÕES ---
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import unicodedata

# --- 2. INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if 'scatter_x' not in st.session_state:
    st.session_state.scatter_x = None
if 'scatter_y' not in st.session_state:
    st.session_state.scatter_y = None
if 'scatter_color' not in st.session_state:
    st.session_state.scatter_color = "Nenhuma"
if 'scatter_filter_col' not in st.session_state:
    st.session_state.scatter_filter_col = "Nenhuma"

# --- 3. CARREGAMENTO E PRÉ-PROCESSAMENTO DOS DADOS ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"
    try:
        df = pd.read_csv(url, sep=";", encoding="latin1")
    except UnicodeDecodeError:
        df = pd.read_csv(url, sep=";", encoding="utf-8")
    
    # Limpeza das colunas
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except ValueError:
                pass
    
    return df

df = load_data()

# --- 4. DICIONÁRIO DE DESCRIÇÕES ---
descricao_variaveis = {
    "SIST_CRIA": "Sistema de criação",
    "NIV_TERR": "Nível territorial",
    "COD_TERR": "Código territorial",
    "NOM_TERR": "Nome territorial",
    "GAL_TOTAL": "Total de galináceos",
    "V_GAL_VEND": "Valor de venda",
    "E_RECEBE_ORI": "Recebe orientação",
    "VTP_AGRO": "Valor total produção",
    "E_ORI_GOV": "Orientação governo",
    "A_PAST_PLANT": "Área pastagem",
    "GAL_ENG": "Galináceos engorda",
    "E_ASSOC_COOP": "Associado a cooperativa",
    "CL_GAL": "Classe galináceos",
    "GAL_POED": "Galináceos poedeiras",
    "Q_DZ_VEND": "Dúzias vendidas",
    "E_COMERC": "Estabelecimento comercial",
    "E_AGRIFAM": "Agricultura familiar",
    "E_FINANC": "Recebe financiamento",
    "RECT_AGRO": "Receita agropecuária",
    "E_FINANC_COOP": "Financiamento cooperativa",
    "E_CNPJ": "Possui CNPJ",
    "E_SUBS": "Produção subsistência",
    "E_DAP": "Possui DAP",
    "N_TRAB_TOTAL": "Total trabalhadores",
    "E_PRODUTOR": "Produtor individual",
    "GAL_MATR": "Galináceos matrizes",
    "GAL_VEND": "Galináceos vendidos",
    "E_ORI_INTEG": "Orientação integradora",
    "E_GAL_MATR": "Possui matrizes"
}

# --- 5. FILTROS DE COLUNAS ---
df_numerico = df.select_dtypes(include=[np.number])
colunas_numericas = df_numerico.columns.tolist()

colunas_para_cor = [col for col in df.columns if col not in colunas_numericas and df[col].nunique() < 20] + \
                   [col for col in colunas_numericas if df[col].nunique() < 20 and df[col].isin([0, 1]).all()]
colunas_para_cor_map = {col: descricao_variaveis.get(col, col) for col in colunas_para_cor}
colunas_para_cor_map["Nenhuma"] = "Nenhuma"

# --- 6. INTERFACE PRINCIPAL ---
st.title("🐔 Análise de Dados de Galináceos")
st.markdown("Explore as relações entre diferentes métricas da avicultura brasileira")

tab1, tab2, tab3 = st.tabs(["Gráfico Personalizado", "Sugestões", "Correlações"])

# --- 7. FUNÇÃO AUXILIAR ---
def set_scatter_vars(x, y, color, filter_col=None):
    st.session_state.scatter_x = x
    st.session_state.scatter_y = y
    st.session_state.scatter_color = color
    st.session_state.scatter_filter_col = filter_col if filter_col else "Nenhuma"

# --- 8. ABA GRÁFICO PERSONALIZADO ---
with tab1:
    st.header("Gráfico de Dispersão Interativo")
    
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox(
            "Eixo X:", 
            colunas_numericas,
            format_func=lambda x: descricao_variaveis.get(x, x),
            key='scatter_x'
        )
    with col2:
        y_col = st.selectbox(
            "Eixo Y:", 
            colunas_numericas,
            format_func=lambda y: descricao_variaveis.get(y, y),
            key='scatter_y'
        )
    
    color_col = st.selectbox(
        "Colorir por:",
        list(colunas_para_cor_map.keys()),
        format_func=lambda x: colunas_para_cor_map.get(x, x),
        key='scatter_color'
    )
    
    # Filtros adicionais
    filter_col = st.selectbox(
        "Filtrar por:",
        ["Nenhuma"] + [col for col in df.columns if df[col].nunique() < 50],
        format_func=lambda x: descricao_variaveis.get(x, x) if x != "Nenhuma" else "Nenhum filtro",
        key='scatter_filter_col'
    )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if filter_col != "Nenhuma":
        selected_values = st.multiselect(
            f"Valores de {descricao_variaveis.get(filter_col, filter_col)}",
            df[filter_col].unique(),
            default=df[filter_col].unique()
        )
        df_filtrado = df_filtrado[df_filtrado[filter_col].isin(selected_values)]
    
    # Plotar gráfico
    if x_col and y_col:
        fig = px.scatter(
            df_filtrado.dropna(subset=[x_col, y_col]),
            x=x_col,
            y=y_col,
            color=color_col if color_col != "Nenhuma" else None,
            hover_name="NOM_TERR" if "NOM_TERR" in df.columns else None,
            labels={x_col: descricao_variaveis.get(x_col, x_col),
                    y_col: descricao_variaveis.get(y_col, y_col)},
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

# --- 9. ABA SUGESTÕES ---
with tab2:
    st.header("Análises Pré-definidas")
    
    suggestions = [
        ("Produção vs Vendas", "GAL_TOTAL", "V_GAL_VEND", "NIV_TERR", "NOM_TERR"),
        ("Orientação vs Produtividade", "E_RECEBE_ORI", "VTP_AGRO", "E_ORI_GOV", "SIST_CRIA"),
        ("Área vs Produção", "A_PAST_PLANT", "GAL_ENG", "E_ASSOC_COOP", "CL_GAL")
    ]
    
    for name, x, y, color, filtro in suggestions:
        if st.button(f"{name}: {descricao_variaveis[x]} × {descricao_variaveis[y]}", 
                    on_click=set_scatter_vars, args=(x, y, color, filtro)):
            st.experimental_rerun()

# --- 10. ABA CORRELAÇÕES ---
with tab3:
    st.header("Análise de Correlação")
    
    if not df_numerico.empty:
        corr_matrix = df_numerico.corr()
        
        # Heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            labels=dict(color="Correlação"),
            height=800
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top correlações
        st.subheader("Principais Correlações")
        corr_series = corr_matrix.unstack().sort_values(key=abs, ascending=False)
        corr_series = corr_series[corr_series != 1].drop_duplicates()
        st.dataframe(corr_series.head(10).rename(descricao_variaveis))

# --- 11. RODAPÉ ---
st.markdown("---")
st.caption("Dados do IBGE 2017 | Análise CIADM1A 2025")
