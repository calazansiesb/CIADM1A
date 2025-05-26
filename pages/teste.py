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
    st.info("Colunas de 'SIST_CRIA' mapeadas para descrições completas para melhor legibilidade.")

# Mostrar um preview dos dados (após o mapeamento, se aplicável)
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
        names=freq_sistemas.index, # Agora 'names' usará as descrições completas
        title='Distribuição Percentual dos Sistemas de Criação',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Adicionado st.expander para a interpretação do gráfico de sistemas de criação
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

    # Adicionado st.expander para a interpretação do gráfico de distribuição por UF
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
    # Conversão de tipos de dados (feito aqui para garantir que 'df' esteja atualizado com as descrições de SIST_CRIA)
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')
    
    corr = df['GAL_TOTAL'].corr(df['N_TRAB_TOTAL'])
    
    fig3 = px.scatter(
        df, # Passa o DataFrame completo para que Plotly possa usar outras colunas
        x='GAL_TOTAL',
        y='N_TRAB_TOTAL',
        title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
        labels={'GAL_TOTAL': 'Total de Galináceos', 'N_TRAB_TOTAL': 'Número de Trabalhadores'},
        trendline="ols",
        color='SIST_CRIA' # Adicionando cor pelo sistema de criação para melhor visualização
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.info(f"**Correlação Calculada:** {corr:.2f}")

    # Conteúdo da análise resumida para o gráfico de dispersão
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
# 🔹 5. Distribuição por Porte dos Estabelecimentos
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

if 'Q_DZ_PROD' in df.columns:
    df['Q_DZ_PROD'] = pd.to_numeric(df['Q_DZ_PROD'], errors='coerce')
    df.dropna(subset=['Q_DZ_PROD'], inplace=True)

    # Determine dynamic bins based on data range
    min_val = df['Q_DZ_PROD'].min()
    max_val = df['Q_DZ_PROD'].max()

    # Define thresholds. Adjust these as needed for your data distribution.
    # It's important that thresholds are ordered and make sense with min/max values.
    threshold_small = 1000
    threshold_medium = 5000

    # Initialize bins to ensure monotonicity
    bins_list = [-float('inf')] # Start with negative infinity for the lowest bin

    # Add thresholds ensuring they are strictly increasing
    if threshold_small > -float('inf'): # Add if valid
        bins_list.append(threshold_small)
    if threshold_medium > threshold_small: # Add if valid and larger than previous
        bins_list.append(threshold_medium)
    
    # Ensure the last bin covers up to the max value of the data
    # If max_val is less than the highest threshold, we need to adjust
    if max_val >= bins_list[-1]: # If max_val is greater than or equal to the last threshold, extend to it
        bins_list.append(max_val + 1) # Add a small epsilon to include max_val
    elif len(bins_list) > 1 and max_val < bins_list[-1]: # If max_val is smaller than the last threshold, ensure it's included as the last bin
        # If the last bin is already greater than max_val, we're good unless max_val is the only significant value
        # This condition helps if max_val falls between two defined thresholds.
        # Ensure we don't duplicate values or have non-monotonic sequence.
        # A simpler approach is to use the standard thresholds and let pd.cut handle the range.
        # However, for the 'Grande' category, we need to ensure it actually captures the max.
        if max_val < threshold_small and max_val > -float('inf'): # If max_val is very small, adjust the thresholds
            bins_list = [-float('inf'), max_val + 1] # Only 'Pequeno' category if max_val is tiny
            labels = ['Pequeno'] # Only one category
        elif max_val < threshold_medium and max_val >= threshold_small:
            bins_list = [-float('inf'), threshold_small, max_val + 1]
            labels = ['Pequeno', 'Médio']
        else: # Default case, use all thresholds defined
            bins_list.append(float('inf')) # Ensure it always goes to infinity if max_val is large
            labels = ['Pequeno', 'Médio', 'Grande']

    # Final check and adjust labels if bins_list changes
    if bins_list == [-float('inf'), 1000, 5000, float('inf')]:
        labels = ['Pequeno', 'Médio', 'Grande']
    elif bins_list == [-float('inf'), 1000, float('inf')]:
        labels = ['Pequeno', 'Médio_Grande'] # Adjust label if only 2 bins
    elif bins_list == [-float('inf'), float('inf')]:
        labels = ['Único Porte'] # Adjust label if only 1 bin

    # Simplified and more robust bin definition:
    # Use fixed thresholds and let pd.cut handle values outside the range,
    # or ensure the last bin covers up to infinity if data extends beyond it.
    bins = [0, 1000, 5000, float('inf')] # Using 0 as lowest bin to avoid -inf for practical "small" numbers
    labels = ['Pequeno (0-1k)', 'Médio (1k-5k)', 'Grande (>5k)']
    
    # Handle potential empty dataframe or all NaNs after dropna
    if df['Q_DZ_PROD'].empty:
        st.warning("Não há dados válidos para a produção de ovos para categorizar por porte.")
    else:
        df['Porte'] = pd.cut(
            df['Q_DZ_PROD'],
            bins=bins,
            labels=labels,
            include_lowest=True, # Include the left-most bin edge
            right=False # Interval is [a, b)
        )

        freq_portes = df['Porte'].value_counts().reindex(labels, fill_value=0)

        fig4 = px.bar(
            x=freq_portes.index,
            y=freq_portes.values,
            title='Distribuição de Estabelecimentos por Porte',
            labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
            color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96']
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Adicionado st.expander para a interpretação do gráfico de porte dos estabelecimentos
        with st.expander("💡 Interpretação do Gráfico de Distribuição por Porte dos Estabelecimentos"):
            st.info("""
            **🏭 Análise da Distribuição por Porte dos Estabelecimentos**

            📌 **Principais observações:**
            - A maioria dos estabelecimentos se enquadra no porte **"Pequeno"** (produção de até 1.000 dúzias de ovos), indicando uma base ampla de pequenos produtores.
            - O número de estabelecimentos de porte **"Médio"** (entre 1.000 e 5.000 dúzias) é significativamente menor que o dos pequenos.
            - Estabelecimentos de porte **"Grande"** (acima de 5.000 dúzias) são os menos numerosos, mas representam as maiores produções individuais.

            💡 **Interpretação:**
            - A predominância de pequenos estabelecimentos pode refletir a estrutura da avicultura familiar ou de subsistência no Brasil.
            - A menor quantidade de estabelecimentos de médio e grande porte sugere uma concentração da produção em poucas unidades de maior escala.
            - Essa distribuição indica a necessidade de políticas diferenciadas para apoiar os diversos portes de produtores, visando tanto o fortalecimento da base quanto o incentivo à expansão e modernização.
            """)
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
