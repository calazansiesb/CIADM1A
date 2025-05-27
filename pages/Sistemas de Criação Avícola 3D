import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # Importar para customizações avançadas se necessário

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola - Sistemas de Criação",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal com emojis e estilo
st.title('🐔 Análise de Sistemas de Criação Avícola do Brasil')
st.markdown("---")

# Carregamento do arquivo local
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
    # Convertendo 'GAL_TOTAL' e 'GAL_VEND' para numérico, tratando erros e preenchendo NaNs
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce').fillna(0)
    df['GAL_VEND'] = pd.to_numeric(df['GAL_VEND'], errors='coerce').fillna(0)
    df['Q_DZ_PROD'] = pd.to_numeric(df['Q_DZ_PROD'], errors='coerce').fillna(0)
    # Convertendo 'SIST_CRIA' para string e removendo espaços
    df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()

    # =============================================
    # ✨ NOVIDADE: Mapeamento e Limpeza da coluna SIST_CRIA
    # =============================================
    if 'SIST_CRIA' in df.columns:
        # Dicionário de mapeamento das abreviações para descrições completas
        mapeamento_sistemas = {
            '1-SIST_POC': 'Produtores de Ovos para Consumo',
            '2-SIST_POI': 'Produtores de Ovos para Incubação',
            '3-SIST_PFC': 'Produtores de Frangos de Corte',
            '4-Outro': 'Outros Produtores'
        }
        
        # Aplicar o mapeamento
        df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)
        # Lidar com possíveis valores não mapeados, tratando-os como 'Desconhecido'
        df['SIST_CRIA'] = df['SIST_CRIA'].apply(lambda x: x if x in mapeamento_sistemas.values() else 'Desconhecido')

    else:
        st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset. Gráficos dependentes dela podem não funcionar corretamente.")

except Exception as e:
    st.error(f"Erro ao carregar o arquivo GALINACEOS.csv: {e}. Certifique-se de que o arquivo está no mesmo diretório ou forneça o caminho completo.")
    st.stop()

# ---
## Gráfico de Densidade de Aves por Sistema de Criação (Heatmap)
# ---
def gerar_grafico_densidade_aves_por_sistema(df):
    st.subheader("📊 Densidade de Aves por Sistema de Criação")
    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou 'GAL_TOTAL').")
        return
    
    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
        return
    
    # Criando bins para GAL_TOTAL para ter uma visualização mais clara no heatmap
    max_gal_total = df_plot['GAL_TOTAL'].max()
    bins = np.linspace(0, max_gal_total, 20) # 20 bins para uma distribuição mais detalhada
    df_plot['GAL_TOTAL_BIN'] = pd.cut(df_plot['GAL_TOTAL'], bins=bins, include_lowest=True, labels=[f'{int(bins[i])}-{int(bins[i+1])}' for i in range(len(bins)-1)])

    fig = px.density_heatmap(
        df_plot,
        x='GAL_TOTAL_BIN', # Usando os bins para o eixo X
        y='SIST_CRIA',
        z='GAL_TOTAL', # Agrega valores para a cor (soma padrão)
        histfunc='count', # Contar a frequência
        title='Densidade de Estabelecimentos por Número de Aves e Sistema de Criação',
        labels={'GAL_TOTAL_BIN': 'Total de Aves (Cabeça)', 'SIST_CRIA': 'Sistema de Criação', 'count': 'Número de Estabelecimentos'},
        color_continuous_scale=px.colors.sequential.Sunsetdark, # Paleta de cores mais vibrante
        nbinsx=len(bins)-1, # Número de bins no eixo X
        height=550,
        template="plotly_white" # Tema branco para elegância
    )
    
    fig.update_layout(
        title_x=0.5, # Centraliza o título
        font=dict(family="Arial", size=12, color="#333"), # Fonte mais limpa
        plot_bgcolor='rgba(0,0,0,0)', # Fundo transparente
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=True, yaxis_showgrid=True, # Mostra as grades
        xaxis_gridcolor='lightgray', yaxis_gridcolor='lightgray',
        xaxis_tickangle=-45, # Rotação dos rótulos do eixo X
        coloraxis_colorbar=dict(title="Contagem") # Título da barra de cores
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Interpretação do Gráfico de Densidade"): # Adicionado st.expander
        st.info("""
        **🔍 Análise da Distribuição de Densidade de Aves por Sistema de Criação**
        📌 **Principais observações:**
        - Este mapa de calor mostra onde a concentração de estabelecimentos é maior, com base no número total de aves e no sistema de criação.
        - **Cores mais escuras** indicam uma maior quantidade de estabelecimentos com aquela combinação de total de aves e sistema.
        - Observe as faixas de aves onde cada sistema de criação tem sua maior densidade.
        💡 **Interpretação:**
        - O gráfico evidencia diferentes perfis produtivos, onde alguns sistemas podem ter maior representatividade em faixas específicas de tamanho de plantel.
        - Isso pode sugerir especializações ou diferentes escalas operacionais predominantes para cada tipo de sistema de criação.
        """)

# ---
## Gráfico de Distribuição da Produção por Sistema (Barras)
# ---
def gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao='aves'):
    if tipo_producao == 'aves':
        coluna_producao = 'GAL_VEND'
        rotulo_eixo_y = 'Quantidade de Aves Vendidas (Cabeça)'
        titulo_grafico = '📈 Distribuição da Venda de Aves por Sistema de Criação'
        color_palette = px.colors.sequential.Agsunset # Outra paleta
    elif tipo_producao == 'ovos':
        coluna_producao = 'Q_DZ_PROD'
        rotulo_eixo_y = 'Quantidade de Ovos Produzidos (Dúzia)'
        titulo_grafico = '🥚 Distribuição da Produção de Ovos por Sistema de Criação'
        color_palette = px.colors.sequential.Greens # Paleta para ovos
    else:
        st.warning("Tipo de produção inválido. Escolha 'aves' ou 'ovos'.")
        return
    
    if 'SIST_CRIA' not in df.columns or coluna_producao not in df.columns:
        st.warning(f"O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou '{coluna_producao}').")
        return
    
    producao_por_sistema = df.groupby('SIST_CRIA')[coluna_producao].sum().reset_index()
    
    fig = px.bar(
        producao_por_sistema,
        x='SIST_CRIA',
        y=coluna_producao,
        title=titulo_grafico,
        labels={'SIST_CRIA': 'Sistema de Criação', coluna_producao: rotulo_eixo_y},
        color='SIST_CRIA',
        color_discrete_sequence=color_palette, # Paleta de cores selecionada
        text=coluna_producao,
        template="plotly_white"
    )
    fig.update_traces(
        texttemplate='%{text:,.0f}', # Formato para números grandes
        textposition='outside',
        marker_line_color='black', # Borda preta
        marker_line_width=1.5 # Largura da borda
    )
    fig.update_layout(
        title_x=0.5,
        xaxis_tickangle=-45,
        font=dict(family="Arial", size=12, color="#333"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=False, yaxis_showgrid=True,
        yaxis_gridcolor='lightgray',
        yaxis_title_standoff=25 # Espaçamento do título do eixo Y
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander(f"💡 Interpretação do Gráfico de {('Venda de Aves' if tipo_producao == 'aves' else 'Produção de Ovos')}"): # Adicionado st.expander
        st.info(f"""
        **🔍 Análise da Distribuição da {'Venda de Aves' if tipo_producao == 'aves' else 'Produção de Ovos'} por Sistema de Criação**
        📌 **Principais observações:**
        - Este gráfico de barras compara a contribuição de cada sistema de criação para o total de {'aves vendidas' if tipo_producao == 'aves' else 'ovos produzidos'}.
        - Observe qual sistema de criação tem o maior volume de produção/venda e qual tem o menor.
        💡 **Interpretação:**
        - O volume de produção reflete a especialização e a escala de operação de cada sistema.
        - Sistemas com maior volume são geralmente os pilares da produção avícola nacional.
        """)

# ---
## Histograma de Distribuição de Aves por Sistema
# ---
def gerar_histograma_aves_por_sistema(df):
    st.subheader("📊 Histograma de Distribuição de Aves por Sistema")
    if 'SIST_CRIA' not in df.columns or 'GAL_TOTAL' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou 'GAL_TOTAL').")
        return
    
    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o histograma.")
        return
    
    fig = px.histogram(
        df_plot,
        x='GAL_TOTAL',
        color='SIST_CRIA',
        title='Frequência de Estabelecimentos por Faixa de Aves e Sistema de Criação',
        labels={'GAL_TOTAL': 'Total de Aves (Cabeça)', 'count': 'Número de Estabelecimentos', 'SIST_CRIA': 'Sistema de Criação'},
        color_discrete_sequence=px.colors.qualitative.Pastel, # Paleta suave e distinguível
        nbins=30, # Aumentar o número de bins para mais detalhe
        barmode='overlay', # 'overlay' para ver as distribuições sobrepostas
        opacity=0.7, # Transparência para ver as sobreposições
        template="plotly_white",
        marginal="box" # Adiciona um box plot marginal para cada distribuição
    )
    fig.update_layout(
        title_x=0.5,
        font=dict(family="Arial", size=12, color="#333"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_showgrid=True, yaxis_showgrid=True,
        xaxis_gridcolor='lightgray', yaxis_gridcolor='lightgray',
        legend_title_text='Sistema de Criação' # Título da legenda
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Interpretação do Histograma"): # Adicionado st.expander
        st.info("""
        **🔍 Análise do Histograma de Distribuição de Aves por Sistema**
        📌 **Principais observações:**
        - Este histograma mostra a frequência de estabelecimentos em diferentes faixas de total de aves, separadas por sistema de criação.
        - A sobreposição ('overlay') permite comparar diretamente as distribuições de cada sistema.
        - O box plot marginal no topo oferece um resumo estatístico (mediana, quartis, outliers) para cada distribuição.
        💡 **Interpretação:**
        - Permite identificar se um sistema de criação tende a ter estabelecimentos com poucos ou muitos animais, e quão variados são os tamanhos de plantel dentro de cada sistema.
        - Desvios em relação a uma distribuição normal (por exemplo, assimetria, múltiplos picos) podem indicar subsegmentos dentro de um mesmo sistema.
        """)

# --- Layout da Aplicação ---
col1, col2 = st.columns([3, 1]) # Proporção ajustada para o rádio button
with col1:
    gerar_grafico_densidade_aves_por_sistema(df)
with col2:
    tipo = st.radio(
        "Tipo de produção:",
        ('aves', 'ovos'),
        format_func=lambda x: "Aves Vendidas" if x=="aves" else "Ovos Produzidos",
        key='tipo_producao'
    )

# Garantir que os gráficos de produção e histograma sempre sejam exibidos
gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao=tipo)
gerar_histograma_aves_por_sistema(df)


# Rodapé
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base em dados de produção avícola* | 📅 *Atualizado em Maio 2024* | ✨ *Melhorias visuais e interativas*
""")
