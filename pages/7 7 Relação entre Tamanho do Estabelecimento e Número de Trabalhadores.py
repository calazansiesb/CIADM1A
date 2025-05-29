import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ===============================================================================
# 0. Carregamento do DataFrame (USANDO DADOS REAIS DO GITHUB)
# ===============================================================================
# URL direta para o arquivo CSV no GitHub (usando raw.githubusercontent.com)
url_galinaceos_csv = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

try:
    df = pd.read_csv(url_galinaceos_csv)
    st.success(f"Dados carregados com sucesso de: {url_galinaceos_csv}")
except Exception as e:
    st.error(f"Erro ao carregar o DataFrame do GitHub: {e}")
    st.info("Por favor, verifique a URL e a acessibilidade do arquivo CSV.")
    # Se o DataFrame não puder ser carregado, definimos um df vazio para evitar erros posteriores
    df = pd.DataFrame()


# =============================================
# 4. Relação: Tamanho × Trabalhadores
# =============================================
st.header('👥 Relação entre Tamanho do Estabelecimento e Número de Trabalhadores')

# --- INÍCIO DA DEPURACÃO ---
st.write("--- Verificações de Depuração ---")
st.write(f"DataFrame 'df' está vazio? {df.empty}")
st.write(f"Colunas em 'df': {df.columns.tolist()}")

col_gal_total_exists = 'GAL_TOTAL' in df.columns
col_n_trab_total_exists = 'N_TRAB_TOTAL' in df.columns
col_sist_cria_exists = 'SIST_CRIA' in df.columns

st.write(f"Coluna 'GAL_TOTAL' existe? {col_gal_total_exists}")
st.write(f"Coluna 'N_TRAB_TOTAL' existe? {col_n_trab_total_exists}")
st.write(f"Coluna 'SIST_CRIA' existe? {col_sist_cria_exists}")
st.write("---------------------------------")
# --- FIM DA DEPURACÃO ---


if col_gal_total_exists and col_n_trab_total_exists and col_sist_cria_exists:
    st.write("Todas as colunas necessárias foram encontradas. Prosseguindo...") # Depuração
    # Converte as colunas para numérico, tratando erros
    df['GAL_TOTAL'] = pd.to_numeric(df['GAL_TOTAL'], errors='coerce')
    df['N_TRAB_TOTAL'] = pd.to_numeric(df['N_TRAB_TOTAL'], errors='coerce')

    # Remove linhas com valores NaN resultantes da coerção, se aplicável
    df_clean = df.dropna(subset=['GAL_TOTAL', 'N_TRAB_TOTAL'])

    st.write(f"DataFrame 'df_clean' após remover NaNs: {df_clean.head()}") # Depuração
    st.write(f"DataFrame 'df_clean' está vazio após NaNs? {df_clean.empty}") # Depuração

    if not df_clean.empty:
        st.write("DataFrame limpo não está vazio. Gerando gráfico...") # Depuração
        # Calcula a correlação
        corr = df_clean['GAL_TOTAL'].corr(df_clean['N_TRAB_TOTAL'])

        # Cria o gráfico de dispersão com linha de tendência OLS e cor por sistema de criação
        fig3 = px.scatter(
            df_clean, # Use o DataFrame limpo aqui
            x='GAL_TOTAL',
            y='N_TRAB_TOTAL',
            title='Relação entre Tamanho do Estabelecimento e Número de Trabalhadores',
            labels={'GAL_TOTAL': 'Total de Galináceos', 'N_TRAB_TOTAL': 'Número de Trabalhadores'},
            trendline="ols", # Linha de tendência de Mínimos Quadrados Ordinários
            color='SIST_CRIA' # Colore os pontos com base no sistema de criação
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
            - Para **Produtores de frangos de corte** e **Outros produtores**, a linha de tendência pode ser **levemente negativa/plana**, sugerindo que o aumento da escala pode ser acompanhado por maior automação e eficiência de mão de obra.
            - Para **Produtores de ovos para consumo** e **incubação**, a relação tende a ser mais **estável ou ligeiramente positiva**, indicando que a demanda por mão de obra é menos reduzida com o aumento da escala por unidade produzida.

            💡 **Interpretação:**
            - A relação entre o tamanho do plantel e o número de trabalhadores é **complexa e não linear**, sendo fortemente influenciada pelo **sistema de criação**.
            - Sistemas como **frangos de corte** podem se beneficiar mais de **automação em larga escala**, enquanto a **produção de ovos** pode ter uma necessidade de mão de obra mais **constante** por unidade produzida.
            - As diferenças observadas indicam que o setor avícola possui **perfis operacionais diversos**, que dependem não apenas do tamanho, mas também da especialização do estabelecimento.
            """)
    else:
        st.warning("Não há dados válidos (não-nulos) nas colunas 'GAL_TOTAL' e 'N_TRAB_TOTAL' para exibir o gráfico após o tratamento de valores ausentes.")
else:
    st.warning("As colunas 'GAL_TOTAL', 'N_TRAB_TOTAL' ou 'SIST_CRIA' não foram encontradas no DataFrame principal 'df'. Verifique os nomes das colunas no seu arquivo CSV e a acessibilidade.")
