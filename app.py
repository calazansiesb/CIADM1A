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
st.subheader("Alunos: Diego Sá, Ewerton Calazans")

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
    

# Mostrar um preview dos dados (após o mapeamento, se aplicável)
st.subheader("Visualização dos Dados")
with st.expander("🔎 Ver primeiros registros do conjunto de dados"):
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

    with st.expander("💡 Interpretação do Gráfico de Proporção dos Sistemas de Criação"):
        st.info("""
        **📊 Análise dos Sistemas de Criação**

        📌 **Principais observações:**
        - Os sistemas **Produtores de frangos de corte** (28,3%) e **Produtores de ovos para consumo** (28,1%) apresentam proporções muito semelhantes, sendo os mais representativos do total.
        - A categoria **Outros produtores** (27,3%) também possui participação relevante, indicando diversidade e presença de outros sistemas além dos principais.
        - O sistema **Produtores de ovos para incubação** (16,4%) apresenta a menor fatia, mas ainda assim representa uma parcela considerável.

        💡 **Interpretação:**
        - O equilíbrio entre Produtores de frangos de corte e Produtores de ovos para consumo sugere concorrência ou complementaridade entre esses sistemas na criação.
        - A expressiva participação da categoria "Outros produtores" ressalta a existência de múltiplos sistemas alternativos, possivelmente personalizados ou regionais.
        - A presença significativa dos Produtores de ovos para incubação, mesmo sendo a menor, pode indicar nichos produtivos ou oportunidades para expansão.
        """)
else:
    st.warning("A coluna 'SIST_CRIA' não foi encontrada no dataset.")

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

    with st.expander("💡 Interpretação do Gráfico de Distribuição por Unidade Federativa"):
        st.info("""
        **🌎 Análise da Distribuição por Unidade Federativa**

        📌 **Principais observações:**
        - Os maiores valores de estabelecimentos estão concentrados nas regiões **Sul, Sudeste e Nordeste**, com estados como **Paraná, Santa Catarina, Bahia, Pernambuco e Rio Grande do Sul** entre os primeiros colocados.
        - O número de estabelecimentos por UF apresenta uma distribuição relativamente homogênea nos estados líderes, com leve declínio nos estados das regiões Norte e Centro-Oeste.
        - Estados como **Acre, Amapá, Roraima e Amazonas** estão entre os que apresentam menor quantidade de estabelecimentos.

        💡 **Interpretação:**
        - A forte presença de estabelecimentos nas regiões Sul, Sudeste e Nordeste pode estar relacionada à infraestrutura mais desenvolvida, tradição produtiva e maior demanda de mercado.
        - A menor concentração de estabelecimentos em estados do Norte e parte do Centro-Oeste pode indicar desafios logísticos, menor densidade populacional ou potencial para expansão do setor.
        - A análise sugere oportunidades de investimento e crescimento nas regiões menos representadas, promovendo maior equilíbrio nacional na distribuição de estabelecimentos.
        """)
else:
    st.warning("A coluna 'NOM_TERR' não foi encontrada no dataset.")

# =============================================
# 🔹 4. Relação: Tamanho × Trabalhadores
# =============================================
st.header('👥 Relação entre Tamanho do Estabelecimento e Número de Trabalhadores')

if 'GAL_TOTAL' in df.columns and 'N_TRAB_TOTAL' in df.columns:
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')
    corr = df['GAL_TOTAL'].corr(df['N_TRAB_TOTAL'])
    fig3 = px.scatter(
        df,
        x='GAL_TOTAL',
        y='N_TRAB_TOTAL',
        title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
        labels={'GAL_TOTAL': 'Total de Galináceos', 'N_TRAB_TOTAL': 'Número de Trabalhadores'},
        trendline="ols",
        color='SIST_CRIA'
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.info(f"**Correlação Calculada:** {corr:.2f}")

    with st.expander("💡 Interpretação do Gráfico de Relação entre Tamanho e Trabalhadores"):
        st.info("""
        **👥 Análise da Relação entre Tamanho do Estabelecimento e Número de Trabalhadores**

        📌 **Principais observações:**
        - A maioria dos estabelecimentos é de **pequeno a médio porte** (poucos galináceos), empregando, em geral, **menos de 200 trabalhadores**.
        - Há uma **alta dispersão** na quantidade de trabalhadores em estabelecimentos menores, indicando variabilidade nas operações.
        - A correlação geral (-0.08) é muito fraca, mas a análise por sistema de criação revela tendências distintas.
        - Para **Produtores de frangos de corte** e **Outros produtores**, a linha de tendência é **levemente negativa/plana**, sugerindo que o aumento da escala pode ser acompanhado por maior automação e eficiência de mão de obra.
        - Para **Produtores de ovos para consumo** e **incubação**, a relação tende a ser mais **estável ou ligeiramente positiva**, indicando que a demanda por mão de obra é menos reduzida com o aumento da escala.

        💡 **Interpretação:**
        - A relação entre o tamanho do plantel e o número de trabalhadores é **complexa e não linear**, sendo fortemente influenciada pelo **sistema de criação**.
        - Sistemas como **frangos de corte** podem se beneficiar mais de **automação em larga escala**, enquanto a **produção de ovos** pode ter uma necessidade de mão de obra mais **constante** por unidade produzida.
        - As diferenças observadas indicam que o setor avícola possui **perfis operacionais diversos**, que dependem não apenas do tamanho, mas também da especialização do estabelecimento.
        """)
else:
    st.warning("As colunas 'GAL_TOTAL' ou 'N_TRAB_TOTAL' não foram encontradas no dataset.")

# =============================================
# 🔹 5. Distribuição por Porte dos Estabelecimentos (CORRIGIDO + ANÁLISE DO GRÁFICO)
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

if 'NOM_CL_GAL' in df.columns:
    freq_portes = df['NOM_CL_GAL'].value_counts().sort_index()
    fig4 = px.bar(
        x=freq_portes.index,
        y=freq_portes.values,
        title='Distribuição de Estabelecimentos por Porte (Faixas IBGE)',
        labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
        color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    st.plotly_chart(fig4, use_container_width=True)

    with st.expander("💡 Interpretação do Gráfico de Distribuição por Porte dos Estabelecimentos"):
        st.info("""
        **🏭 Análise da Distribuição por Porte dos Estabelecimentos**

        O gráfico mostra a quantidade de estabelecimentos distribuídos por diferentes faixas de porte (definidas pelo IBGE):

        - As faixas intermediárias, especialmente entre **201 e 5.000 aves**, concentram os maiores números de estabelecimentos, sugerindo predominância de produtores de médio porte no setor.
        - Pequenos produtores ("De 1 a 100" e "De 101 a 200") também são numerosos, mas em menor quantidade que as faixas intermediárias.
        - Faixas extremas ("De 100.001 e mais" e "Sem galináceos em 30.09.2017") apresentam participação reduzida, indicando que grandes produtores e estabelecimentos temporariamente inativos são minoria.
        - A categoria "Total" pode representar registros agregados ou casos não classificados nas demais faixas, devendo ser analisada com cautela.
        - A presença de estabelecimentos "Sem galináceos" reforça a importância de considerar sazonalidade ou inatividade temporária.

        **Conclusão:** 
        - O perfil da produção avícola brasileira é fortemente marcado pela presença de estabelecimentos de porte intermediário, com pequena participação de grandes produtores e um contingente relevante de pequenos estabelecimentos. Isso tem implicações para políticas públicas, estratégias de mercado e apoio ao setor.
        """)
elif 'Q_DZ_PROD' in df.columns:
    df['Q_DZ_PROD'] = pd.to_numeric(df['Q_DZ_PROD'], errors='coerce')
    df_filtered = df.dropna(subset=['Q_DZ_PROD']).copy()

    if df_filtered.empty:
        st.warning("Não há dados válidos para a produção de ovos para categorizar por porte após a remoção de valores ausentes.")
    else:
        num_bins = 3

        if df_filtered['Q_DZ_PROD'].nunique() < num_bins:
            st.warning(f"Atenção: A coluna 'Q_DZ_PROD' tem apenas {df_filtered['Q_DZ_PROD'].nunique()} valores únicos. Pode não ser possível criar {num_bins} grupos distintos. Exibindo grupos existentes.")
            bins = [0, 1, 1000, 5000, float('inf')]
            labels = ['Nulo (0)', 'Muito Pequeno (0-1k)', 'Pequeno (1k-5k)', 'Médio-Grande (>5k)']
            df_filtered['Porte'] = pd.cut(
                df_filtered['Q_DZ_PROD'],
                bins=bins,
                labels=labels,
                include_lowest=True,
                right=False
            )
            freq_portes = df_filtered['Porte'].value_counts()
            labels_with_data = [label for label in labels if label in freq_portes.index]
            freq_portes = freq_portes.reindex(labels_with_data, fill_value=0)
        else:
            bins = pd.qcut(
                df_filtered['Q_DZ_PROD'],
                q=num_bins,
                duplicates='drop',
                retbins=True
            )[1]
            if bins[0] > 0:
                bins[0] = 0
            if bins[-1] < df_filtered['Q_DZ_PROD'].max():
                bins[-1] = df_filtered['Q_DZ_PROD'].max() + 1e-9

            if num_bins == 3 and len(bins) == 4:
                labels = [
                    f'Pequeno (até {int(bins[1])})',
                    f'Médio ({int(bins[1])} - {int(bins[2])})',
                    f'Grande (acima de {int(bins[2])})'
                ]
            elif len(bins) > 1:
                labels = [f'{int(bins[i])} - {int(bins[i+1])}' for i in range(len(bins)-1)]
            else:
                labels = ["Único Porte"]

            df_filtered['Porte'] = pd.cut(
                df_filtered['Q_DZ_PROD'],
                bins=bins,
                labels=labels,
                include_lowest=True,
                right=False
            )
            freq_portes = df_filtered['Porte'].value_counts().reindex(labels, fill_value=0)

        fig4 = px.bar(
            x=freq_portes.index,
            y=freq_portes.values,
            title='Distribuição de Estabelecimentos por Porte',
            labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
            color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96']
        )
        st.plotly_chart(fig4, use_container_width=True)

        with st.expander("💡 Interpretação do Gráfico de Distribuição por Porte dos Estabelecimentos"):
            st.info("""
            **🏭 Análise da Distribuição por Porte dos Estabelecimentos**

            O gráfico mostra a quantidade de estabelecimentos distribuídos por diferentes faixas de porte (definidas dinamicamente):

            - As faixas intermediárias concentram os maiores números de estabelecimentos, sugerindo predominância de produtores de médio porte no setor.
            - A maior parte dos estabelecimentos tende a se concentrar nos portes menores, enquanto os maiores produtores são menos numerosos, mas contribuem significativamente para o volume total de produção.
            - A presença de estabelecimentos "Nulo" ou "Sem produção" reforça a importância de considerar sazonalidade ou inatividade temporária.

            **Conclusão:** 
            - O perfil da produção avícola brasileira é fortemente marcado pela presença de estabelecimentos de porte intermediário, com pequena participação de grandes produtores e um contingente relevante de pequenos estabelecimentos. Isso tem implicações para políticas públicas, estratégias de mercado e apoio ao setor.
            """)
else:
    st.warning("A coluna 'NOM_CL_GAL' ou 'Q_DZ_PROD' não foi encontrada no dataset.")

# =============================================
# 🔹 Rodapé
# =============================================
st.markdown("---")
st.caption("""
🔎 *Análise desenvolvida com base nos dados reais do IBGE 2017*
📅 *Atualizado em Maio 2025*
""")
