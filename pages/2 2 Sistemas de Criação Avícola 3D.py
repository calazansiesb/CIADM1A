import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola - Sistemas de Criação",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Análise de Sistemas de Criação Avícola')
st.markdown("Uma visão aprofundada dos diferentes sistemas de criação de aves e seus impactos na produção.")
st.markdown("---")

# Carregamento do arquivo local
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
    # Limpar nomes das colunas (remover espaços, acentos, padronizar maiúsculas)
    df.columns = [unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8').strip().upper() for col in df.columns]
    # REMOVIDO: st.write("Colunas disponíveis no DataFrame:", list(df.columns))
    
    # Convertendo para numérico e preenchendo NaNs
    for col in ['GAL_TOTAL', 'GAL_VEND', 'Q_DZ_PROD']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            st.warning(f"A coluna '{col}' não foi encontrada no dataset.")
    
    # Convertendo 'SIST_CRIA' para string e removendo espaços
    if 'SIST_CRIA' in df.columns:
        df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()
        # Mapeamento e Limpeza da coluna SIST_CRIA
        mapeamento_sistemas = {
            '1-SIST_POC': 'Produtores de Ovos para Consumo',
            '2-SIST_POI': 'Produtores de Ovos para Incubacao',
            '3-SIST_PFC': 'Produtores de Frangos de Corte',
            '4-Outro': 'Outros Produtores'
        }
        df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)
    else:
        st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset. Gráficos dependentes dela podem não funcionar corretamente.")

except Exception as e:
    st.error(f"Erro ao carregar o arquivo GALINACEOS.csv: {e}")
    st.stop()


# ---
# Gráfico de Densidade de Aves por Sistema de Criação
# ---
def gerar_grafico_densidade_aves_por_sistema(df):
    st.subheader("📊 Densidade de Aves por Sistema de Criação")
    st.markdown("Explore a distribuição da densidade de aves por diferentes sistemas de criação, identificando padrões e concentrações.")
    if not set(['SIST_CRIA', 'GAL_TOTAL']).issubset(df.columns):
        st.error("Colunas 'SIST_CRIA' ou 'GAL_TOTAL' não estão presentes no DataFrame. Verifique o CSV.")
        st.write("Colunas atuais:", df.columns)
        return

    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o gráfico de densidade.")
        return

    fig = px.density_heatmap(
        df_plot,
        x='GAL_TOTAL',
        y='SIST_CRIA', # Agora com os nomes completos
        title='Distribuição da Densidade de Aves por Sistema de Criação',
        labels={'GAL_TOTAL': 'Total de Aves (Cabeça)', 'SIST_CRIA': 'Sistema de Criação'},
        color_continuous_scale='Plasma',
        nbinsx=30,
        height=500,
        template='plotly_white'
    )
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        coloraxis_colorbar=dict(title='Densidade')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Interpretação do Gráfico de Densidade"):
        st.info("""
        **🔍 Análise da Distribuição de Densidade de Aves por Sistema de Criação**
        📌 **Principais observações:**
        - O sistema **"Outros Produtores"** apresenta concentração de estabelecimentos com menor número total de aves, predominantemente entre **6.000 e 7.000 cabeças**.
        - **"Produtores de Ovos para Consumo"** e **"Produtores de Frangos de Corte"** mostram maior dispersão, com a maioria dos registros entre **9.000 e 12.000 aves** por estabelecimento.
        - **"Produtores de Ovos para Incubacao"** destaca-se por concentrar-se nas faixas mais elevadas, **acima de 13.000 aves**.
        💡 **Interpretação:**
        - O gráfico evidencia diferentes perfis produtivos: sistemas voltados para incubação tendem a operar com plantéis mais numerosos, enquanto sistemas classificados como "Outros" concentram-se em pequenas criações.
        - A variação na densidade sugere especialização e segmentação claras entre os sistemas de criação, refletindo demandas produtivas e estratégias distintas.
        - As informações são úteis para orientar políticas de apoio e estratégias de crescimento conforme o perfil predominante de cada sistema.
        """)

# ---
# Gráfico de Distribuição da Produção por Sistema
# ---
def gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao='aves'):
    if tipo_producao == 'aves':
        coluna_producao = 'GAL_VEND'
        rotulo_eixo_y = 'Quantidade de Aves Vendidas (Cabeça)'
        titulo_grafico = '📈 Distribuição da Venda de Aves por Sistema de Criação'
        hover_data = ['GAL_VEND']
    elif tipo_producao == 'ovos':
        coluna_producao = 'Q_DZ_PROD'
        rotulo_eixo_y = 'Quantidade de Ovos Produzidos (Dúzia)'
        titulo_grafico = '🥚 Distribuição da Produção de Ovos por Sistema de Criação'
        hover_data = ['Q_DZ_PROD']
    else:
        st.warning("Tipo de produção inválido. Escolha 'aves' ou 'ovos'.")
        return
    
    st.subheader(titulo_grafico)
    st.markdown(f"Visualize como a {'venda de aves' if tipo_producao == 'aves' else 'produção de ovos'} se distribui entre os diferentes sistemas de criação.")
    
    if 'SIST_CRIA' not in df.columns or coluna_producao not in df.columns:
        st.warning(f"O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou '{coluna_producao}').")
        st.write("Colunas atuais:", df.columns)
        return
    
    producao_por_sistema = df.groupby('SIST_CRIA')[coluna_producao].sum().reset_index()
    
    fig = px.bar(
        producao_por_sistema,
        x='SIST_CRIA',
        y=coluna_producao,
        title=titulo_grafico,
        labels={'SIST_CRIA': 'Sistema de Criação', coluna_producao: rotulo_eixo_y},
        color=coluna_producao,
        color_continuous_scale='Viridis',
        text=coluna_producao,
        template='plotly_white',
        hover_data=hover_data
    )
    fig.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander(f"💡 Interpretação do Gráfico de {('Venda de Aves' if tipo_producao == 'aves' else 'Produção de Ovos')}"):
        st.info(f"""
        **🔍 Análise da Distribuição da {'Venda de Aves' if tipo_producao == 'aves' else 'Produção de Ovos'} por Sistema de Criação**
        📌 **Principais observações:**
        - O sistema **"Produtores de Frangos de Corte"** lidera as vendas, com maior volume comercializado.
        - Os sistemas **"Produtores de Ovos para Consumo"** e **"Produtores de Ovos para Incubacao"** também apresentam volumes elevados, evidenciando a importância dos sistemas voltados à produção de ovos tanto para consumo direto quanto para incubação.
        - O grupo **"Outros Produtores"** registra o menor volume de vendas, indicando baixa participação desse segmento no mercado.
        💡 **Interpretação:**
        - O destaque do sistema de frangos de corte reforça o papel central da avicultura de corte na cadeia produtiva e comercial.
        - A significativa participação dos sistemas de ovos para consumo e incubação revela a diversificação da produção e a relevância desses segmentos no abastecimento do mercado.
        - A baixa representatividade do grupo "Outros" pode indicar oportunidades para o desenvolvimento de nichos ou sistemas alternativos, caso haja demanda específica.
        """)

# ---
# Histograma de Distribuição de Aves por Sistema
# ---
def gerar_histograma_aves_por_sistema(df):
    st.subheader("📊 Histograma de Distribuição de Aves por Sistema")
    st.markdown("Compreenda a frequência de estabelecimentos por faixa de total de aves, segmentada por sistema de criação.")
    if not set(['SIST_CRIA', 'GAL_TOTAL']).issubset(df.columns):
        st.error("Colunas 'SIST_CRIA' ou 'GAL_TOTAL' não estão presentes no DataFrame. Verifique o CSV.")
        st.write("Colunas atuais:", df.columns)
        return

    df_plot = df[['SIST_CRIA', 'GAL_TOTAL']].dropna()
    if df_plot.empty:
        st.warning("Não há dados suficientes para gerar o histograma.")
        return

    fig = px.histogram(
        df_plot,
        x='GAL_TOTAL',
        color='SIST_CRIA',
        title='Distribuição de Aves por Sistema de Criação',
        labels={'GAL_TOTAL': 'Total de Aves (Cabeça)', 'SIST_CRIA': 'Sistema de Criação'},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        nbins=40,
        barmode='overlay',
        opacity=0.7,
        template='plotly_white',
        hover_data=['GAL_TOTAL']
    )
    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        legend_title_text='Sistema de Criação'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Interpretação do Histograma"):
        st.info("""
        **🔍 Análise do Histograma de Distribuição de Aves por Sistema**
        📌 **Principais observações:**
        - O histograma apresenta a distribuição do total de aves por estabelecimento, segmentado pelos sistemas: **Produtores de Ovos para Consumo**, **Produtores de Frangos de Corte**, **Outros Produtores** e **Produtores de Ovos para Incubacao**.
        - A maior concentração de registros ocorre nas faixas de **6.000 a 14.000 aves**, evidenciando uma ampla variação no porte dos estabelecimentos.
        - O sistema **"Produtores de Ovos para Incubacao"** aparece tanto nas faixas mais baixas (cerca de 6.000 aves) quanto nas mais altas (acima de 13.000 aves), indicando diversidade de escalas dentro deste segmento.
        - Os sistemas **"Produtores de Ovos para Consumo"**, **"Produtores de Frangos de Corte"** e **"Outros Produtores"** estão presentes principalmente nas faixas intermediárias e elevadas, sugerindo preferência por plantéis médios a grandes nesses sistemas.
        💡 **Interpretação:**
        - O gráfico revela que a produção avícola é marcada por grande heterogeneidade no tamanho dos plantéis, mesmo dentro de um mesmo sistema de criação.
        - A presença de sistemas de incubação em diferentes faixas pode indicar estratégias produtivas distintas, enquanto os demais sistemas tendem a se concentrar em faixas médias e altas de produção.
        - Essas informações são relevantes para o planejamento do setor, permitindo identificar oportunidades de apoio e desenvolvimento conforme o perfil produtivo predominante em cada sistema.
        """)

# Seção de gráficos
col1, col2 = st.columns([3, 1])
with col1:
    gerar_grafico_densidade_aves_por_sistema(df)
with col2:
    st.markdown("Selecione o tipo de produção para visualizar as vendas:")
    tipo = st.radio(
        "Tipo de Produção:",
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
🔎 *Análise desenvolvida com base em dados de produção avícola* 📅 *Atualizado em Outubro 2023*
""")
