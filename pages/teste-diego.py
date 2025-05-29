import streamlit as st
import plotly.express as px
import pandas as pd

# URL do arquivo CSV no GitHub (versão raw)
url = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv"

# Carregar os dados corretamente
df = pd.read_csv(url, sep=";", encoding="utf-8")

# Dicionário de descrições das variáveis
descricao_variaveis = {
    "SIST_CRIA": "Sistema de criação",
    "NIV_TERR": "Nível das unidades territoriais",
    "COD_TERR": "Código das unidades territoriais",
    "NOM_TERR": "Nome das unidades territoriais",
    "GAL_TOTAL": "Total efetivo de galináceos",
    "V_GAL_VEND": "Valor dos galináceos vendidos",
    "E_RECEBE_ORI": "Estabelecimentos com orientação técnica",
    "VTP_AGRO": "Valor total da produção agropecuária",
    "E_ORI_GOV": "Orientação do governo",
    "A_PAST_PLANT": "Área de pastagem plantada",
    "GAL_ENG": "Galináceos para engorda",
    "E_ASSOC_COOP": "Associação a cooperativas",
    "CL_GAL": "Classe de cabeças de galináceos",
    "GAL_POED": "Total de poedeiras",
    "Q_DZ_VEND": "Ovos vendidos em dúzias",
    "E_COMERC": "Estabelecimentos comerciais",
    "E_AGRIFAM": "Agricultura familiar",
    "E_FINANC": "Estabelecimentos com investimento",
    "RECT_AGRO": "Receita total agropecuária",
    "E_FINANC_COOP": "Investimento de cooperativas",
    "E_CNPJ": "Estabelecimentos com CNPJ",
    "E_SUBS": "Produção para consumo próprio",
    "E_DAP": "Possui DAP/PRONAF",
    "N_TRAB_TOTAL": "Total de trabalhadores",
    "E_PRODUTOR": "Produtor individual",
    "GAL_MATR": "Total de matrizes",
    "GAL_VEND": "Galináceos vendidos",
    "E_ORI_INTEG": "Orientação de integradoras",
    "E_GAL_MATR": "Estabelecimentos com matrizes"
}

# Configuração da interface do Streamlit
st.title("Gráfico de Dispersão - Correlação entre Métricas")

# Seletores para métricas
col_x = st.selectbox("Selecione a métrica para o eixo X:", df.columns, format_func=lambda x: descricao_variaveis.get(x, x))
col_y = st.selectbox("Selecione a métrica para o eixo Y:", df.columns, format_func=lambda y: descricao_variaveis.get(y, y))

# Seletor para região
if "NIV_TERR" in df.columns:
    regiao = st.selectbox("Selecione a Região:", df["NIV_TERR"].unique())
    df_filtrado = df[df["NIV_TERR"] == regiao]
else:
    st.error("Coluna 'NIV_TERR' não encontrada no arquivo.")
    df_filtrado = df

# Criar o gráfico de dispersão
fig = px.scatter(
    df_filtrado, 
    x=col_x, 
    y=col_y, 
    color="NOM_TERR" if "NOM_TERR" in df.columns else None,
    title=f"Correlação entre {col_x} e {col_y} para {regiao}",
    labels={col_x: col_x, col_y: col_y}
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

# Expander para exibir sugestões adicionais
with st.expander("Sugestões de Análises"):
    st.write(f"""
    **1. Produção vs. Comercialização**  
    - **Eixo X:** {descricao_variaveis["GAL_TOTAL"]}  
    - **Eixo Y:** {descricao_variaveis["V_GAL_VEND"]}  
    - **Cores:** {descricao_variaveis["NIV_TERR"]}  
    - **Filtro:** {descricao_variaveis["NOM_TERR"]}  
    - **Objetivo:** Verificar se estabelecimentos com maior efetivo de galináceos geram mais receita com vendas.  

    **2. Orientação Técnica vs. Produtividade**  
    - **Eixo X:** {descricao_variaveis["E_RECEBE_ORI"]}  
    - **Eixo Y:** {descricao_variaveis["VTP_AGRO"]}  
    - **Cores:** {descricao_variaveis["E_ORI_GOV"]}  
    - **Filtro:** {descricao_variaveis["SIST_CRIA"]}  
    - **Objetivo:** Analisar se a assistência técnica está correlacionada com maior valor de produção.  

    **3. Área de Pastagem vs. Criação de Galináceos**  
    - **Eixo X:** {descricao_variaveis["A_PAST_PLANT"]}  
    - **Eixo Y:** {descricao_variaveis["GAL_ENG"]}  
    - **Cores:** {descricao_variaveis["E_ASSOC_COOP"]}  
    - **Filtro:** {descricao_variaveis["CL_GAL"]}  
    - **Objetivo:** Investigar se propriedades com mais pastagem tendem a ter maior produção de aves para engorda.  

    **4. Venda de Ovos vs. Número de Poedeiras**  
    - **Eixo X:** {descricao_variaveis["GAL_POED"]}  
    - **Eixo Y:** {descricao_variaveis["Q_DZ_VEND"]}  
    - **Cores:** {descricao_variaveis["E_COMERC"]}  
    - **Filtro:** {descricao_variaveis["E_AGRIFAM"]}  
    - **Objetivo:** Correlacionar o tamanho do plantel de poedeiras com a comercialização de ovos.  

    **5. Investimento vs. Receita Total**  
    - **Eixo X:** {descricao_variaveis["E_FINANC"]}  
    - **Eixo Y:** {descricao_variaveis["RECT_AGRO"]}  
    - **Cores:** {descricao_variaveis["E_FINANC_COOP"]}  
    - **Filtro:** {descricao_variaveis["E_CNPJ"]}  
    - **Objetivo:** Avaliar se acesso a financiamento está ligado a maiores receitas.  
    """)

