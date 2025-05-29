import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ===============================================================================
# 0. Carregamento do DataFrame (USANDO DADOS REAIS DO GITHUB)
# ===============================================================================
url_galinaceos_csv = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

try:
    df = pd.read_csv(url_galinaceos_csv, sep=';')
except Exception as e:
    st.error(f"Erro ao carregar o DataFrame do GitHub: {e}")
    st.info("Por favor, verifique a URL e a acessibilidade do arquivo CSV e o formato (delimitador).")
    df = pd.DataFrame()


# =============================================
# 4. Relação: Tamanho × Trabalhadores
# =============================================
st.header('👥 Relação entre Tamanho do Estabelecimento e Número de Trabalhadores')

# Verifica se as colunas necessárias existem no DataFrame e se não está vazio
if not df.empty and 'GAL_TOTAL' in df.columns and 'N_TRAB_TOTAL' in df.columns and 'SIST_CRIA' in df.columns:

    # --- INÍCIO: Mapeamento e Limpeza da coluna SIST_CRIA ---
    st.write("--- Depuração SIST_CRIA ---") # Linha de depuração
    st.write(f"Valores únicos de 'SIST_CRIA' ANTES da limpeza e mapeamento: {df['SIST_CRIA'].unique().tolist()}") # Linha de depuração

    df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()
    mapeamento_sistemas = {
        '1-SIST_POC': 'Produtores de Ovos para Consumo',
        '2-SIST_POI': 'Produtores de Ovos para Incubacao',
        '3-SIST_PFC': 'Produtores de Frangos de Corte',
        '4-Outro': 'Outros Produtores'
    }
    df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)

    st.write(f"Valores únicos de 'SIST_CRIA' DEPOIS da limpeza e mapeamento: {df['SIST_CRIA'].unique().tolist()}") # Linha de depuração
    st.write("--- Fim Depuração SIST_CRIA ---") # Linha de depuração
    # --- FIM: Mapeamento e Limpeza da coluna SIST_CRIA ---

    # Converte as colunas para numérico, tratando erros
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')

    # Remove linhas com valores NaN resultantes da coerção para as colunas essenciais
    df_clean = df.dropna(subset=['GAL_TOTAL', 'N_TRAB_TOTAL', 'SIST_CRIA'])

    if not df_clean.empty:
        # Calcula a correlação
        corr = df_clean['GAL_TOTAL'].corr(df_clean['N_TRAB_TOTAL'])

        # Cria o gráfico de dispersão com linha de tendência OLS e cor por sistema de criação
        fig3 = px.scatter(
            df_clean,
            x='GAL_TOTAL',
            y='N_TRAB_TOTAL',
            title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
            labels={'GAL_TOTAL': 'Total de Galináceos', 'N_TRAB_TOTAL': 'Número de Trabalhadores', 'SIST_CRIA': 'Sistema de Criação'},
            trendline="ols",
            color='SIST_CRIA',
            hover_name="SIST_CRIA"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Exibe a correlação calculada
        st.info(f"**Correlação Calculada:** {corr:.2f}")

        # Seção de interpretação expansível
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
        st.warning("Não há dados válidos (não-nulos) nas colunas 'GAL_TOTAL', 'N_TRAB_TOTAL' ou 'SIST_CRIA' para exibir o gráfico após o tratamento de valores ausentes. Verifique seus dados de origem e o mapeamento dos sistemas de criação.")
else:
    st.warning("As colunas 'GAL_TOTAL', 'N_TRAB_TOTAL' ou 'SIST_CRIA' não foram encontradas no DataFrame principal ou o DataFrame está vazio. Verifique o nome das colunas no seu arquivo CSV e a acessibilidade do mesmo.")
