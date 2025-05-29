import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ===============================================================================
# 0. Carregamento do DataFrame
# ===============================================================================
url_galinaceos_csv = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

try:
    df = pd.read_csv(url_galinaceos_csv, sep=';')
    # st.success("Dados 'GALINACEOS.csv' carregados com sucesso!") # Comentar para não poluir a interface
except Exception as e:
    st.error(f"Erro ao carregar o DataFrame 'GALINACEOS.csv' do GitHub: {e}")
    st.info("Por favor, verifique a URL, a acessibilidade do arquivo CSV e o formato (delimitador ';').")
    df = pd.DataFrame() # Define um df vazio para evitar erros posteriores

# ===============================================================================
# 1. Pré-processamento Comum do DataFrame (seções anteriores)
# ===============================================================================

# Mapeamento e Limpeza da coluna SIST_CRIA (aplicado globalmente ao df)
if not df.empty and 'SIST_CRIA' in df.columns:
    df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()
    mapeamento_sistemas = {
        '1-SIST_POC': 'Produtores de Ovos para Consumo',
        '2-SIST_POI': 'Produtores de Ovos para Incubacao',
        '3-SIST_PFC': 'Produtores de Frangos de Corte',
        '4-Outro': 'Outros Produtores'
    }
    df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)
else:
    if not df.empty:
        st.warning("Coluna 'SIST_CRIA' não encontrada para mapeamento.")


# =============================================
# 4. Relação: Tamanho × Trabalhadores
# =============================================
st.header('👥 Relação entre Tamanho do Estabelecimento e Número de Trabalhadores')

if not df.empty and 'GAL_TOTAL' in df.columns and 'N_TRAB_TOTAL' in df.columns and 'SIST_CRIA' in df.columns:
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')

    df_clean_trab = df.dropna(subset=['GAL_TOTAL', 'N_TRAB_TOTAL', 'SIST_CRIA'])

    if not df_clean_trab.empty:
        corr = df_clean_trab['GAL_TOTAL'].corr(df_clean_trab['N_TRAB_TOTAL'])
        fig3 = px.scatter(
            df_clean_trab,
            x='GAL_TOTAL',
            y='N_TRAB_TOTAL',
            title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
            labels={'GAL_TOTAL': 'Total de Galináceos', 'N_TRAB_TOTAL': 'Número de Trabalhadores', 'SIST_CRIA': 'Sistema de Criação'},
            trendline="ols",
            color='SIST_CRIA',
            hover_name="SIST_CRIA"
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.info(f"**Correlação Calculada:** {corr:.2f}")

        with st.expander("💡 Interpretação do Gráfico de Relação entre Tamanho e Trabalhadores"):
            st.info("""
            **👥 Análise da Relação entre Tamanho do Estabelecimento e Número de Trabalhadores**

            📌 **Principais observações:**
            - A maioria dos estabelecimentos é de **pequeno a médio porte** (poucos galináceos), empregando, em geral, **menos de 200 trabalhadores**.
            - Há uma **alta dispersão** na quantidade de trabalhadores em estabelecimentos menores, indicando variabilidade nas operações.
            - A correlação geral (que você verá no `st.info` acima) é geralmente **muito fraca ou quase nula**, mas a análise por sistema de criação (as cores dos pontos) revela tendências distintas.
            - Para **Produtores de Frangos de Corte** e **Outros Produtores**, a linha de tendência pode ser **levemente negativa/plana**, sugerindo que o aumento da escala pode ser acompanhado por maior automação e eficiência de mão de obra.
            - Para **Produtores de Ovos para Consumo** e **Produtores de Ovos para Incubacao**, a relação tende a ser mais **estável ou ligeiramente positiva**, indicando que a demanda por mão de obra é menos reduzida com o aumento da escala por unidade produzida.

            💡 **Interpretação:**
            - A relação entre o tamanho do plantel e o número de trabalhadores é **complexa e não linear**, sendo fortemente influenciada pelo **sistema de criação**.
            - Sistemas como **Produtores de Frangos de Corte** podem se beneficiar mais de **automação em larga escala**, enquanto a **produção de ovos** pode ter uma necessidade de mão de obra mais **constante** por unidade produzida.
            - As diferenças observadas indicam que o setor avícola possui **perfis operacionais diversos**, que dependem não apenas do tamanho, mas também da especialização do estabelecimento.
            """)
    else:
        st.warning("Não há dados válidos (não-nulos) nas colunas 'GAL_TOTAL', 'N_TRAB_TOTAL' ou 'SIST_CRIA' para exibir o gráfico após o tratamento de valores ausentes na seção de Trabalhadores. Verifique seus dados de origem.")
else:
    st.warning("As colunas 'GAL_TOTAL', 'N_TRAB_TOTAL' ou 'SIST_CRIA' não foram encontradas no DataFrame principal ou o DataFrame está vazio para a seção de Trabalhadores. Verifique o nome das colunas no seu arquivo CSV e a acessibilidade.")


# =============================================
# 5. Distribuição por Porte dos Estabelecimentos
# =============================================
st.markdown("---") # Linha divisória
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

# Adaptação para usar df_clean ou df e tratar NaNs se houver
if not df.empty and 'NOM_CL_GAL' in df.columns:
    # O .value_counts() já ignora NaN por padrão, mas é bom garantir a tipagem
    df['NOM_CL_GAL'] = df['NOM_CL_GAL'].astype(str).str.strip()
    
    # Se houver valores como 'nan' (string) após o strip, podemos querer removê-los
    # ou tratá-los de outra forma, dependendo do que NOM_CL_GAL possa ter.
    # Por enquanto, assumimos que são strings válidas ou nulos reais.
    
    # É uma boa prática filtrar antes de fazer value_counts se houver NaNs que você não quer contar
    freq_portes = df['NOM_CL_GAL'].value_counts().sort_index()

    # Filtra valores que podem ter se tornado "nan" (string) se houverem
    if 'nan' in freq_portes.index:
        freq_portes = freq_portes.drop('nan')

    if not freq_portes.empty: # Verifica se há dados para plotar
        fig4 = px.bar(
            x=freq_portes.index,
            y=freq_portes.values,
            title='Distribuição de Estabelecimentos por Porte (Faixas IBGE)',
            labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
            color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#FF6692'] # Adicionei mais uma cor se houver mais de 5 categorias
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
    else:
        st.warning("Não há dados válidos na coluna 'NOM_CL_GAL' para exibir o gráfico de Distribuição por Porte após a filtragem.")
else:
    st.warning("A coluna 'NOM_CL_GAL' não foi encontrada no DataFrame principal ou o DataFrame está vazio para a seção de Distribuição por Porte.")
