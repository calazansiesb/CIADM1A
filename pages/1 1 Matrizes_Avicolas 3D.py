import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # Importado, mas px já faz muito do trabalho

# Configuração da página
st.set_page_config(
    page_title="Análise de Matrizes Avícolas - IBGE",
    page_icon="🐣",
    layout="wide", # Manter wide para gráficos 3D
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Matrizes Avícolas por Unidade Territorial')
st.markdown("---")

# Carregar dados
try:
    df = pd.read_csv("GALINACEOS.csv", sep=';')
    df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()
    df['GAL_MATR'] = pd.to_numeric(df['GAL_MATR'], errors='coerce').fillna(0)
    # Adicionar tratamento para outras colunas numéricas que podem ser usadas no 3D
    if 'GAL_TOTAL' in df.columns:
        df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce').fillna(0)
    else:
        st.warning("Coluna 'GAL_TOTAL' não encontrada. O gráfico 3D pode ter dados limitados.")
        df['GAL_TOTAL'] = 0 # Define como 0 para evitar erros se a coluna não existir

    if 'N_TRAB_TOTAL' in df.columns:
        df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce').fillna(0)
    else:
        st.warning("Coluna 'N_TRAB_TOTAL' não encontrada. O gráfico 3D pode ter dados limitados.")
        df['N_TRAB_TOTAL'] = 0 # Define como 0 para evitar erros se a coluna não existir

except FileNotFoundError:
    st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado. Por favor, certifique-se de que o arquivo está no mesmo diretório da aplicação.")
    st.stop()

# =============================================
# ✨ NOVIDADE: Mapeamento e Limpeza da coluna SIST_CRIA
# =============================================
if 'SIST_CRIA' in df.columns:
    # Limpar espaços em branco e garantir que é string antes de mapear
    df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()

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
    st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset. Verifique o nome da coluna.")

# Listas de regiões
regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
df_estados = df[~df['NOM_TERR'].isin(regioes + ['Brasil'])].copy()
df_regioes = df[df['NOM_TERR'].isin(regioes)].copy()


# =============================================
# 1. GRÁFICO DE BARRAS - MATRIZES POR ESTADO (Estilizado)
# =============================================
st.header('📊 Distribuição de Matrizes por Estado')

if not df_estados.empty:
    # Processamento dos dados
    matrizes_por_estado = df_estados.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum()
    matrizes_por_estado = matrizes_por_estado.sort_values('GAL_MATR', ascending=False)
    
    # Gráfico interativo com cores mais vivas e tema elegante
    fig1 = px.bar(
        matrizes_por_estado,
        x='NOM_TERR',
        y='GAL_MATR',
        title='Total de Matrizes por Estado',
        labels={'NOM_TERR': 'Estado', 'GAL_MATR': 'Número de Matrizes'},
        color='GAL_MATR', # Colorir por valor para gradiente
        color_continuous_scale=px.colors.sequential.Tealgrn, # Escala de cor elegante
        template="plotly_white" # Tema limpo
    )
    fig1.update_layout(
        xaxis_tickangle=-45,
        title_x=0.5, # Centralizar título
        plot_bgcolor='rgba(0,0,0,0)', # Fundo transparente
        paper_bgcolor='rgba(0,0,0,0)', # Fundo do papel transparente
        xaxis=dict(showgrid=True, gridcolor='lightgray'), # Mostrar grid no eixo X
        yaxis=dict(showgrid=True, gridcolor='lightgray') # Mostrar grid no eixo Y
    )
    fig1.update_traces(marker_line_color='black', marker_line_width=0.5) # Borda nas barras
    st.plotly_chart(fig1, use_container_width=True)
    
    with st.expander("💡 Interpretação do Gráfico de Barras"):
        st.markdown("""
        **🔍 Análise por Estado**
        
        📌 **Principais observações:**
        - **Mato Grosso do Sul** e **Pernambuco** lideram em número absoluto de matrizes avícolas.
        - **Distrito Federal** e **Pará** também apresentam valores expressivos, compondo o grupo dos quatro estados com maior concentração.
        - A distribuição é bastante desigual, com alguns estados apresentando números significativamente mais baixos.
        
        💡 **Interpretação:**
        - A concentração de matrizes em poucos estados pode refletir fatores como infraestrutura, tradição produtiva e incentivos regionais.
        - Estados do **Centro-Oeste** e **Nordeste** se destacam como polos importantes na produção de matrizes.
        - Estados com menor número de matrizes podem representar oportunidades para crescimento e investimento no setor avícola.
        """)
    
else:
    st.warning("Não há dados disponíveis para os estados.")

# =============================================
# 2. GRÁFICO DE PIZZA - MATRIZES POR REGIÃO (Estilizado)
# =============================================
st.header('🌎 Distribuição Regional de Matrizes')

if not df_regioes.empty:
    # Processamento dos dados
    matrizes_por_regiao = df_regioes.groupby('NOM_TERR', as_index=False)['GAL_MATR'].sum()
    matrizes_por_regiao['Porcentagem'] = (matrizes_por_regiao['GAL_MATR'] / matrizes_por_regiao['GAL_MATR'].sum()) * 100
    
    # Gráfico interativo com cores mais vivas e tema elegante
    fig2 = px.pie(
        matrizes_por_regiao,
        values='GAL_MATR',
        names='NOM_TERR',
        title='Proporção de Matrizes por Região',
        color_discrete_sequence=px.colors.qualitative.Pastel, # Uma paleta de cores suaves e agradáveis
        hover_data=['Porcentagem'],
        labels={'NOM_TERR': 'Região', 'GAL_MATR': 'Matrizes'},
        hole=0.4, # Adiciona um "buraco" para transformar em gráfico de rosca (donut chart)
        template="plotly_white"
    )
    fig2.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1)) # Adiciona bordas nas fatias
    )
    fig2.update_layout(title_x=0.5) # Centralizar título
    st.plotly_chart(fig2, use_container_width=True)
    
    with st.expander("💡 Interpretação do Gráfico de Pizza"):
        st.info("""
        **🔍 Análise por Região**
        
        📌 **Principais observações:**
        - **Nordeste** lidera com **40,2%** das matrizes avícolas do Brasil.
        - **Centro-Oeste** é o segundo maior polo, com **30,7%**.
        - Sul, Norte e Sudeste têm participações menores (11,4%, 9,89% e 7,95%).
        
        💡 **Interpretação:**
        - Forte concentração da produção de matrizes nas regiões **Nordeste** e **Centro-Oeste**.
        - A distribuição pode estar relacionada à disponibilidade de áreas, clima e incentivos regionais.
        - Indica a necessidade de estratégias regionais para o desenvolvimento do setor.
        """)
else:
    st.warning("Não há dados disponíveis para as regiões.")

# =============================================
# 3. GRÁFICO ADICIONAL - SISTEMAS DE CRIAÇÃO (Estilizado)
# =============================================
st.header('🏭 Sistemas de Criação por Região')

if 'SIST_CRIA' in df.columns and not df_regioes.empty:
    # Processamento dos dados
    sistemas_por_regiao = df_regioes.groupby(['NOM_TERR', 'SIST_CRIA'])['GAL_MATR'].sum().reset_index()
    
    # Gráfico interativo com cores mais vivas e tema elegante
    fig3 = px.bar(
        sistemas_por_regiao,
        x='NOM_TERR',
        y='GAL_MATR',
        color='SIST_CRIA', # Esta coluna agora terá os nomes completos
        title='Sistemas de Criação por Região',
        labels={'NOM_TERR': 'Região', 'GAL_MATR': 'Matrizes', 'SIST_CRIA': 'Sistema de Criação'},
        barmode='group', # Para barras agrupadas
        color_discrete_sequence=px.colors.qualitative.Set2, # Outra paleta qualitativa vibrante
        template="plotly_white"
    )
    fig3.update_layout(
        title_x=0.5, # Centralizar título
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        legend_title_text='Sistema de Criação' # Título para a legenda
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    with st.expander("💡 Interpretação dos Sistemas de Criação por Região"):
        st.info("""
        **🔍 Análise por Região — Sistemas de Criação**

        📌 **Principais observações:**
        - O sistema de produção de ovos para consumo (**Produtores de ovos para consumo**) é predominante no **Centro-Oeste**, **Nordeste** e **Sul**.
        - O **Nordeste** apresenta a maior quantidade de matrizes, especialmente no sistema **Produtores de ovos para consumo**, seguido por relevante participação do sistema **Produtores de frangos de corte**.
        - O **Sudeste** e o **Norte** possuem menor representatividade, com destaque para o Sudeste na produção de frangos de corte.
        - Baixa expressão dos sistemas **Produtores de ovos para incubação** e **Outros produtores** em todas as regiões.

        💡 **Interpretação:**
        - Há especialização regional nos sistemas de criação, com o **Centro-Oeste** e **Nordeste** se destacando na produção de ovos e o **Sudeste** e **Sul** mostrando variações nos tipos de produção.
        - As diferenças refletem fatores como tradição produtiva, demanda de mercado e adequação das condições regionais.
        - Os resultados indicam a necessidade de estratégias regionais para aprimorar a competitividade e a sustentabilidade do setor avícola.
        """)
else:
    st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset ou não há dados para regiões.")

# =============================================
# 4. NOVO GRÁFICO: DISPERSÃO 3D (Elegante)
# =============================================
st.header('🌐 Relação 3D: Matrizes, Galináceos Totais e Trabalhadores por Sistema')

# Verificação para o gráfico 3D
cols_for_3d = ['GAL_MATR', 'GAL_TOTAL', 'N_TRAB_TOTAL', 'SIST_CRIA']
if all(col in df.columns for col in cols_for_3d):
    df_plot_3d = df.dropna(subset=cols_for_3d).copy()
    
    if not df_plot_3d.empty:
        fig_3d = px.scatter_3d(
            df_plot_3d,
            x='GAL_MATR',
            y='GAL_TOTAL',
            z='N_TRAB_TOTAL',
            color='SIST_CRIA', # Colorir por Sistema de Criação
            title='Distribuição 3D de Matrizes, Galináceos Totais e Trabalhadores',
            labels={
                'GAL_MATR': 'Número de Matrizes',
                'GAL_TOTAL': 'Total de Galináceos',
                'N_TRAB_TOTAL': 'Número de Trabalhadores',
                'SIST_CRIA': 'Sistema de Criação'
            },
            color_discrete_sequence=px.colors.qualitative.Bold, # Paleta de cores vibrantes
            height=700,
            template="plotly_dark" # Tema escuro para um visual 3D impactante
        )

        fig_3d.update_layout(
            scene = dict(
                xaxis_title_text='Número de Matrizes',
                yaxis_title_text='Total de Galináceos',
                zaxis_title_text='Número de Trabalhadores',
                # Ajuste da câmera para uma visão inicial mais interessante
                camera = dict(
                    eye=dict(x=1.8, y=1.8, z=0.8) # Um pouco de cima e de lado
                )
            ),
            title_x=0.5 # Centralizar título
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)

        with st.expander("💡 Interpretação do Gráfico de Dispersão 3D"):
            st.info("""
            **🌐 Análise do Gráfico de Dispersão 3D:**
            Este gráfico visualiza a inter-relação entre três métricas-chave: o número de matrizes, o total de galináceos e o número de trabalhadores, com cada ponto colorido pelo sistema de criação.

            📌 **Principais observações:**
            - **Agrupamentos:** Observe se existem agrupamentos de pontos para sistemas de criação específicos em certas regiões do espaço 3D, o que indicaria padrões de escala de produção e uso de mão de obra.
            - **Escalas:** Identifique se sistemas com muitas matrizes também têm um alto número de galináceos totais e/ou trabalhadores.
            - **Outliers:** Pontos muito distantes dos demais podem representar granjas com perfis de produção ou operação incomuns para seu sistema.

            💡 **Interpretação:**
            - A distribuição dos pontos pode revelar a eficiência ou a intensidade de trabalho em diferentes sistemas de criação (e.g., granjas com muitas aves mas poucos trabalhadores podem ser altamente automatizadas).
            - Permite identificar se a produção de matrizes está correlacionada com o tamanho total do plantel e a força de trabalho, e como isso varia entre os sistemas.
            - É uma ferramenta poderosa para entender a estrutura e a diversidade das operações avícolas em múltiplas dimensões.
            """)
    else:
        st.warning("Não há dados suficientes para gerar o gráfico de dispersão 3D após a remoção de valores ausentes.")
else:
    st.warning("Colunas necessárias para o gráfico 3D ('GAL_TOTAL' ou 'N_TRAB_TOTAL') não foram encontradas no dataset.")

# Rodapé
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base nos dados do IBGE* 📅 *Atualizado em Outubro 2023* """)
