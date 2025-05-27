import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Dashboard Avícola - Análise de Sistemas de Criação",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .st-emotion-cache-1kyxreq {
        justify-content: center;
    }
    .stPlotlyChart {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .st-expander {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stAlert {
        border-radius: 10px;
    }
    .title-wrapper {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Título principal com estilo aprimorado
st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #2c3e50; font-weight: 700;">Análise de Sistemas de Criação Avícola</h1>
    <p style="color: #7f8c8d; font-size: 1.1rem;">Dashboard interativo para análise de produção e distribuição avícola</p>
</div>
""", unsafe_allow_html=True)

# Divisor estilizado
st.markdown("---")

# Carregamento do arquivo local com tratamento aprimorado
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("GALINACEOS.csv", sep=';', encoding='utf-8')
        
        # Conversão de colunas numéricas com tratamento de erros
        numeric_cols = ['GAL_TOTAL', 'GAL_VEND', 'Q_DZ_PROD']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Limpeza e mapeamento da coluna SIST_CRIA
        if 'SIST_CRIA' in df.columns:
            df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()
            mapeamento_sistemas = {
                '1-SIST_POC': 'Produtores de ovos para consumo',
                '2-SIST_POI': 'Produtores de ovos para incubação',
                '3-SIST_PFC': 'Produtores de frangos de corte',
                '4-Outro': 'Outros produtores'
            }
            df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)
        
        return df
    
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {str(e)}")
        return None

df = load_data()

if df is None:
    st.stop()

# Sidebar com filtros
with st.sidebar:
    st.markdown("## 🔍 Filtros")
    
    # Filtro por sistema de criação
    sistemas = df['SIST_CRIA'].unique().tolist()
    sistemas_selecionados = st.multiselect(
        "Sistemas de Criação",
        options=sistemas,
        default=sistemas,
        help="Selecione os sistemas de criação para análise"
    )
    
    # Filtro por quantidade mínima de aves
    min_aves = st.slider(
        "Quantidade mínima de aves",
        min_value=0,
        max_value=int(df['GAL_TOTAL'].max()),
        value=0,
        step=1000,
        help="Filtrar por estabelecimentos com no mínimo X aves"
    )
    
    # Aplicar filtros
    df_filtrado = df[df['SIST_CRIA'].isin(sistemas_selecionados)]
    df_filtrado = df_filtrado[df_filtrado['GAL_TOTAL'] >= min_aves]

# Função para formatar números grandes
def format_number(num):
    if num >= 1e6:
        return f"{num/1e6:.1f}M"
    if num >= 1e3:
        return f"{num/1e3:.1f}K"
    return str(num)

# Métricas principais
st.markdown("## 📊 Visão Geral")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Estabelecimentos", len(df_filtrado))
with col2:
    st.metric("Total de Aves", format_number(df_filtrado['GAL_TOTAL'].sum()))
with col3:
    st.metric("Aves Vendidas", format_number(df_filtrado['GAL_VEND'].sum()))
with col4:
    st.metric("Ovos Produzidos (dúzias)", format_number(df_filtrado['Q_DZ_PROD'].sum()))

# Gráfico de Densidade de Aves por Sistema de Criação
def grafico_densidade_aves():
    st.markdown("### 📈 Densidade de Aves por Sistema")
    
    if df_filtrado.empty:
        st.warning("Nenhum dado disponível com os filtros atuais.")
        return
    
    fig = px.density_heatmap(
        df_filtrado,
        x='GAL_TOTAL',
        y='SIST_CRIA',
        title='Distribuição de Densidade de Aves por Sistema',
        labels={'GAL_TOTAL': 'Total de Aves', 'SIST_CRIA': 'Sistema de Criação'},
        color_continuous_scale='Oranges',
        nbinsx=20,
        height=500
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        title_font_size=20,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("🔍 Interpretação"):
        st.info("""
        Este gráfico mostra a concentração de estabelecimentos em diferentes faixas de quantidade de aves por sistema de criação.
        - Cores mais escuras indicam maior concentração de estabelecimentos
        - Permite identificar os padrões de distribuição para cada sistema
        """)

# Gráfico de Produção/Vendas
def grafico_producao(tipo='aves'):
    if tipo == 'aves':
        coluna = 'GAL_VEND'
        titulo = "📊 Vendas de Aves por Sistema"
        rotulo = "Aves Vendidas"
        cor = px.colors.sequential.Oranges
    else:
        coluna = 'Q_DZ_PROD'
        titulo = "🥚 Produção de Ovos por Sistema"
        rotulo = "Dúzias de Ovos"
        cor = px.colors.sequential.Blues
    
    st.markdown(f"### {titulo}")
    
    if df_filtrado.empty:
        st.warning("Nenhum dado disponível com os filtros atuais.")
        return
    
    fig = px.bar(
        df_filtrado.groupby('SIST_CRIA')[coluna].sum().reset_index(),
        x='SIST_CRIA',
        y=coluna,
        color='SIST_CRIA',
        color_discrete_sequence=cor,
        text=coluna,
        labels={'SIST_CRIA': 'Sistema de Criação', coluna: rotulo}
    )
    
    fig.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        opacity=0.8
    )
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=rotulo,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("🔍 Interpretação"):
        st.info(f"""
        Este gráfico mostra a {rotulo.lower()} por sistema de criação.
        - Permite comparar o desempenho de cada sistema
        - Identificar os sistemas com maior volume de produção/vendas
        """)

# Gráfico de Distribuição com Boxplot
def grafico_distribuicao():
    st.markdown("### 📦 Distribuição de Aves por Sistema")
    
    if df_filtrado.empty:
        st.warning("Nenhum dado disponível com os filtros atuais.")
        return
    
    fig = px.box(
        df_filtrado,
        x='SIST_CRIA',
        y='GAL_TOTAL',
        color='SIST_CRIA',
        color_discrete_sequence=px.colors.sequential.Oranges,
        labels={'GAL_TOTAL': 'Total de Aves', 'SIST_CRIA': 'Sistema de Criação'},
        points="all"
    )
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Total de Aves",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50'),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("🔍 Interpretação"):
        st.info("""
        Este boxplot mostra a distribuição do número de aves por sistema de criação.
        - A linha no meio da caixa representa a mediana
        - As extremidades da caixa mostram o primeiro e terceiro quartis
        - Os "bigodes" mostram o intervalo interquartil
        - Pontos fora dos bigodes são considerados outliers
        """)

# Layout dos gráficos
tab1, tab2 = st.tabs(["📊 Análise de Densidade", "📈 Análise de Produção"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        grafico_densidade_aves()
    with col2:
        tipo_analise = st.radio(
            "Tipo de análise:",
            ('aves', 'ovos'),
            format_func=lambda x: "Aves" if x == "aves" else "Ovos",
            key='tipo_analise'
        )

with tab2:
    grafico_producao(tipo_analise)
    grafico_distribuicao()

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    <p>Dashboard desenvolvido para análise de sistemas de criação avícola</p>
    <p>📅 Dados atualizados em Outubro 2023 | 🛠️ Desenvolvido com Streamlit e Plotly</p>
</div>
""", unsafe_allow_html=True)
