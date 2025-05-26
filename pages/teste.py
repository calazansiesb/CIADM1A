import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola - Sistemas de Criação",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Análise de Sistemas de Criação Avícola')
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
            '1-SIST_POC': 'Produtores de ovos para consumo',
            '2-SIST_POI': 'Produtores de ovos para incubação',
            '3-SIST_PFC': 'Produtores de frangos de corte',
            '4-Outro': 'Outros produtores'
        }
        
        # Aplicar o mapeamento
        df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)
        st.info("Colunas de 'SIST_CRIA' mapeadas para descrições completas para melhor legibilidade.")
    else:
        st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset. Gráficos dependentes dela podem não funcionar corretamente.")

except Exception as e:
    st.error(f"Erro ao carregar o arquivo GALINACEOS.csv: {e}")
    st.stop()


# ---
## Gráfico de Densidade de Aves por Sistema de Criação
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
    
    fig = px.density_heatmap(
        df_plot,
        x='GAL_TOTAL',
        y='SIST_CRIA', # Agora com os nomes completos
        title='Distribuição de Densidade de Aves por Sistema de Criação',
        labels={'GAL_TOTAL': 'Total de Aves (Cabeça)', 'SIST_CRIA': 'Sistema de Criação'},
        color_continuous_scale='Oranges',
        nbinsx=20,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Interpretação do Gráfico de Densidade"): # Adicionado st.expander
        st.info("""
        **🔍 Análise da Distribuição de Densidade de Aves por Sistema de Criação**
        📌 **Principais observações:**
        - O sistema **"Outros produtores"** apresenta concentração de estabelecimentos com menor número total de aves, predominantemente entre **6.000 e 7.000 cabeças**.
        - **"Produtores de ovos para consumo"** e **"Produtores de frangos de corte"** mostram maior dispersão, com a maioria dos registros entre **9.000 e 12.000 aves** por estabelecimento.
        - **"Produtores de ovos para incubação"** destaca-se por concentrar-se nas faixas mais elevadas, **acima de 13.000 aves**.
        💡 **Interpretação:**
        - O gráfico evidencia diferentes perfis produtivos: sistemas voltados para incubação tendem a operar com plantéis mais numerosos, enquanto sistemas classificados como "Outros" concentram-se em pequenas criações.
        - A variação na densidade sugere especialização e segmentação claras entre os sistemas de criação, refletindo demandas produtivas e estratégias distintas.
        - As informações são úteis para orientar políticas de apoio e estratégias de crescimento conforme o perfil predominante de cada sistema.
        """)

# ---
## Gráfico de Distribuição da Produção por Sistema
# ---
def gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao='aves'):
    if tipo_producao == 'aves':
        coluna_producao = 'GAL_VEND'
        rotulo_eixo_y = 'Quantidade de Aves Vendidas (Cabeça)'
        titulo_grafico = '📈 Distribuição da Venda de Aves por Sistema de Criação'
    elif tipo_producao == 'ovos':
        coluna_producao = 'Q_DZ_PROD'
        rotulo_eixo_y = 'Quantidade de Ovos Produzidos (Dúzia)'
        titulo_grafico = '🥚 Distribuição da Produção de Ovos por Sistema de Criação'
    else:
        st.warning("Tipo de produção inválido. Escolha 'aves' ou 'ovos'.")
        return
    
    if 'SIST_CRIA' not in df.columns or coluna_producao not in df.columns:
        st.warning(f"O DataFrame não contém as colunas necessárias ('SIST_CRIA' ou '{coluna_producao}').")
        return
    
    producao_por_sistema = df.groupby('SIST_CRIA')[coluna_producao].sum().reset_index()
    
    fig = px.bar(
        producao_por_sistema,
        x='SIST_CRIA', # Agora com os nomes completos
        y=coluna_producao,
        title=titulo_grafico,
        labels={'SIST_CRIA': 'Sistema de Criação', coluna_producao: rotulo_eixo_y},
        color='SIST_CRIA', # Agora com os nomes completos
        color_discrete_sequence=px.colors.sequential.Oranges,
        text=coluna_producao
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander(f"💡 Interpretação do Gráfico de {('Venda de Aves' if tipo_producao == 'aves' else 'Produção de Ovos')}"): # Adicionado st.expander
        st.info(f"""
        **🔍 Análise da Distribuição da {'Venda de Aves' if tipo_producao == 'aves' else 'Produção de Ovos'} por Sistema de Criação**
        📌 **Principais observações:**
        - O sistema **"Produtores de frangos de corte"** lidera as vendas, com maior volume comercializado.
        - Os sistemas **"Produtores de ovos para consumo"** e **"Produtores de ovos para incubação"** também apresentam volumes elevados, evidenciando a importância dos sistemas voltados à produção de ovos tanto para consumo direto quanto para incubação.
        - O grupo **"Outros produtores"** registra o menor volume de vendas, indicando baixa participação desse segmento no mercado.
        💡 **Interpretação:**
        - O destaque do sistema de frangos de corte reforça o papel central da avicultura de corte na cadeia produtiva e comercial.
        - A significativa participação dos sistemas de ovos para consumo e incubação revela a diversificação da produção e a relevância desses segmentos no abastecimento do mercado.
        - A baixa representatividade do grupo "Outros" pode indicar oportunidades para o desenvolvimento de nichos ou sistemas alternativos, caso haja demanda específica.
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
        color='SIST_CRIA', # Agora com os nomes completos
        title='Distribuição de Aves por Sistema de Criação',
        labels={'GAL_TOTAL': 'Total de Aves (Cabeça)', 'SIST_CRIA': 'Sistema de Criação'},
        color_discrete_sequence=px.colors.sequential.Oranges,
        nbins=20,
        barmode='stack',
        opacity=0.7
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Interpretação do Histograma"): # Adicionado st.expander
        st.info("""
        **🔍 Análise do Histograma de Distribuição de Aves por Sistema**
        📌 **Principais observações:**
        - O histograma apresenta a distribuição do total de aves por estabelecimento, segmentado pelos sistemas: **Produtores de ovos para consumo**, **Produtores de frangos de corte**, **Outros produtores** e **Produtores de ovos para incubação**.
        - A maior concentração de registros ocorre nas faixas de **6.000 a 14.000 aves**, evidenciando uma ampla variação no porte dos estabelecimentos.
        - O sistema **"Produtores de ovos para incubação"** aparece tanto nas faixas mais baixas (cerca de 6.000 aves) quanto nas mais altas (acima de 13.000 aves), indicando diversidade de escalas dentro deste segmento.
        - Os sistemas **"Produtores de ovos para consumo"**, **"Produtores de frangos de corte"** e **"Outros produtores"** estão presentes principalmente nas faixas intermediárias e elevadas, sugerindo preferência por plantéis médios a grandes nesses sistemas.
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
    tipo = st.radio(
        "Tipo de produção:",
        ('aves', 'ovos'),
        format_func=lambda x: "Aves vendidas" if x=="aves" else "Ovos produzidos",
        key='tipo_producao'
    )

# Garantir que os gráficos de produção e histograma sempre sejam exibidos
gerar_grafico_distribuicao_producao_por_sistema(df, tipo_producao=tipo)
gerar_histograma_aves_por_sistema(df)


# Rodapé
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base em dados de produção avícola* 📅 *Atualizado em Outubro 2023* """)
