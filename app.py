import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Trabalho Final - Introdução à Ciência de Dados CIADM1A-CIA001-20251",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title("Trabalho Final - Introdução à Ciência de Dados CIADM1A-CIA001-20251")
st.subheader("Professor: Alexandre Vaz Roriz")
st.subheader("Alunos: DIEGO ALEXANDRE, Ewerton Calazans")

st.title('Análise de Galináceos no Brasil (IBGE 2017)')
st.markdown("---")

# =============================================
# 🔹 1. Carregar Dados Reais do GitHub
# =============================================
st.header("📂 Carregando Dados Reais")

# URL do arquivo no GitHub (Substitua pelo correto caso necessário)
csv_url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

# Carregar dados
try:
    df = pd.read_csv(csv_url, sep=';')
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# Mostrar um preview dos dados
st.subheader("Visualização dos Dados")
st.dataframe(df.head())

# =============================================
# 🔹 2. Proporção dos Sistemas de Criação
# =============================================
st.header('📊 Proporção dos Sistemas de Criação')

if 'SIST_CRIA' in df.columns:
    freq_sistemas = df['SIST_CRIA'].value_counts(normalize=True) * 100
    fig1 = px.pie(
        values=freq_sistemas.values,
        names=freq_sistemas.index,
        title='Distribuição Percentual dos Sistemas de Criação',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset.")

st.info("""
    **📊 Análise dos Sistemas de Criação**
    
    📌 **Principais observações:**
    - Os sistemas 3-SIST_PFC (28,3%) e 1-SIST_POC (28,1%) apresentam proporções muito semelhantes, sendo os mais representativos do total.
    - A categoria 4-Outro (27,3%) também possui participação relevante, indicando diversidade e presença de outros sistemas além dos principais.
    - O sistema 2-SIST_POI (16,4%) apresenta a menor fatia, mas ainda assim representa uma parcela considerável.

    💡 **Interpretação:**
    - O equilíbrio entre SIST_PFC e SIST_POC sugere concorrência ou complementaridade entre esses sistemas na criação.
    - A expressiva participação da categoria "Outro" ressalta a existência de múltiplos sistemas alternativos, possivelmente personalizados ou regionais.
    - A presença significativa do SIST_POI, mesmo sendo a menor, pode indicar nichos produtivos ou oportunidades para expansão.
""")

# =============================================
# 🔹 3. Distribuição por Unidade Federativa
# =============================================
st.header('🌎 Distribuição por Unidade Federativa')

if 'NOM_TERR' in df.columns:
    freq_estab_por_uf = df['NOM_TERR'].value_counts()
    fig2 = px.bar(
        x=freq_estab_por_uf.index,
        y=freq_estab_por_uf.values,
        title='Número de Estabelecimentos por UF',
        labels={'x': 'Unidade Federativa', 'y': 'Quantidade'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("A coluna 'NOM_TERR' não foi encontrada no dataset.")

st.info("""
    **🌎 Análise da Distribuição por Unidade Federativa**
    
    📌 **Principais observações:**
    - Os maiores valores de estabelecimentos estão concentrados nas regiões Sul, Sudeste e Nordeste, com estados como Paraná, Santa Catarina, Bahia, Pernambuco e Rio Grande do Sul entre os primeiros colocados.
    - O número de estabelecimentos por UF apresenta uma distribuição relativamente homogênea nos estados líderes, com leve declínio nos estados das regiões Norte e Centro-Oeste.
    - Estados como Acre, Amapá, Roraima e Amazonas estão entre os que apresentam menor quantidade de estabelecimentos.

    💡 **Interpretação:**
    - A forte presença de estabelecimentos nas regiões Sul, Sudeste e Nordeste pode estar relacionada à infraestrutura mais desenvolvida, tradição produtiva e maior demanda de mercado.
    - A menor concentração de estabelecimentos em estados do Norte e parte do Centro-Oeste pode indicar desafios logísticos, menor densidade populacional ou potencial para expansão do setor.
    - A análise sugere oportunidades de investimento e crescimento nas regiões menos representadas, promovendo maior equilíbrio nacional na distribuição de estabelecimentos.
""")

# =============================================
# 🔹 4. Relação: Tamanho × Trabalhadores
# =============================================
st.header('👥 Relação entre Tamanho do Estabelecimento e Número de Trabalhadores')

if 'GAL_TOTAL' in df.columns and 'N_TRAB_TOTAL' in df.columns:
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')
    
    corr = df['GAL_TOTAL'].corr(df['N_TRAB_TOTAL'])
    
    fig3 = px.scatter(
        x=df['GAL_TOTAL'],
        y=df['N_TRAB_TOTAL'],
        title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
        labels={'x': 'Total de Galináceos', 'y': 'Número de Trabalhadores'},
        trendline="ols"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.info(f"**Correlação Calculada:** {corr:.2f}")
else:
    st.warning("As colunas 'GAL_TOTAL' ou 'N_TRAB_TOTAL' não foram encontradas no dataset.")

# =============================================
# 🔹 5. Distribuição por Porte dos Estabelecimentos
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

if 'Q_DZ_PROD' in df.columns:
    df['Q_DZ_PROD'] = pd.to_numeric(df['Q_DZ_PROD'], errors='coerce')
    df.dropna(subset=['Q_DZ_PROD'], inplace=True)

    df['Porte'] = pd.cut(df['Q_DZ_PROD'], bins=[0, 5000, 20000, np.inf], labels=['Pequeno', 'Médio', 'Grande'])
    freq_portes = df['Porte'].value_counts()

    fig4 = px.bar(
        x=freq_portes.index,
        y=freq_portes.values,
        title='Distribuição de Estabelecimentos por Porte',
        labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
        color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96']
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("A coluna 'Q_DZ_PROD' não foi encontrada no dataset.")

# =============================================
# 🔹 Rodapé
# =============================================
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base nos dados reais do IBGE 2017*  
📅 *Atualizado em Maio 2025*  
""")
