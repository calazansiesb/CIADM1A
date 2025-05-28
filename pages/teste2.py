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
    "CL_GAL": "Número da classe de cabeças de galináceos em 30.09.2022",
    "NOM_CL_GAL": "Nome da classe de cabeças de galináceos em 30.09.2022",
    "E_CRIA_GAL": "Número de estabelecimentos agropecuários com criação de galináceos (Unidades)",
    "E_TEM_GAL": "Número de estabelecimentos agropecuários com galináceos na data de referência (Unidades)",
    "E_GAL_VEND": "Número de estabelecimentos agropecuários que venderam galináceos (Unidades)",
    "E_OVOS_PROD": "Número de estabelecimentos agropecuários com produção de ovos de galinha (Unidades)",
    "E_OVOS_VEND": "Número de estabelecimentos agropecuários que venderam ovos de galinha (Unidades)",
    "E_SUBS": "Número de estabelecimentos agropecuários com finalidade principal da produção para consumo próprio e de pessoas com laços de parentesco com o produtor",
    "E_COMERC": "Número de estabelecimentos agropecuários com finalidade principal da produção voltada para comercialização (inclusive troca ou escambo)",
    "E_RECEBE_ORI": "O estabelecimento recebe orientação de técnico especializado em agropecuária",
    "E_ORI_GOV": "Origem da orientação - governo (federal, estadual ou municipal)",
    "E_ORI_PROPRIA": "Origem da orientação - própria",
    "E_ORI_COOP": "Origem da orientação - cooperativas",
    "E_ORI_EMP_INT": "Origem da orientação - empresas integradoras",
    "E_ORI_EMP_PRI": "Origem da orientação - empresas privadas de planejamento",
    "E_ORI_ONG": "Origem da orientação - organização não-governamental (ONG)",
    "E_ORI_SIST_S": "Origem da orientação - Sistema S",
    "E_ORI_OUTRA": "Origem da orientação - outra origem",
    "E_GAL_ENG": "Número de estabelecimentos agropecuários com galináceos para engorda",
    "E_GAL_GALOS": "Número de estabelecimentos agropecuários com galos",
    "E_GAL_POED": "Número de estabelecimentos agropecuários com poedeiras",
    "E_GAL_MATR": "Número de estabelecimentos agropecuários com matrizeiras",
    "E_ASSOC_COOP": "Número de estabelecimentos agropecuários com produtor(a) associado(a) à cooperativa",
    "E_FINANC": "Número de estabelecimentos agropecuários que obtiveram investimento",
    "E_FINANC_COOP": "Número de estabelecimentos agropecuários que obtiveram investimento proveniente de cooperativas de crédito",
    "E_FINANC_INTEG": "Número de estabelecimentos agropecuários que obtiveram investimento proveniente de empresa integradora",
    "E_DAP": "Número de estabelecimentos agropecuários em que o(a) produtor(a) possui DAP (documento de aptidão ao PRONAF)",
    "E_AGRIFAM": "Número de estabelecimentos agropecuários classificados como de Agricultura familiar - Lei 11.326 de 24.07.2017",
    "E_N_AGRIFAM": "Número de estabelecimentos agropecuários classificados como não sendo de Agricultura familiar - Lei 11.326 de 24.07.2017",
    "E_PRODUTOR": "Número de estabelecimentos agropecuários com condição legal do(a) produtor(a) - Produtor(a) individual",
    "E_COOPERATIVA": "Número de estabelecimentos agropecuários com condição legal do(a) produtor(a) - Cooperativa",
    "E_SA_LDTA": "Número de estabelecimentos agropecuários com condição legal do(a) produtor(a) - Sociedade anônima ou por cotas de responsabilidade limitada",
    "E_CNPJ": "Número de estabelecimentos agropecuários com CNPJ",
    "GAL_TOTAL": "Total efetivo de galinhas, galos, frangas, frangos e pintos (Cabeça)",
    "GAL_ENG": "Total de galináceos para engorda (Cabeça)",
    "GAL_GALOS": "Total de galos (Cabeça)",
    "GAL_POED": "Total de poedeiras (Cabeça)",
    "GAL_MATR": "Total de matrizes (Cabeça)",
    "GAL_VEND": "Quantidade de galináceos vendidos (Cabeça)",
    "V_GAL_VEND": "Valor dos galináceos vendidos (R$)",
    "Q_DZ_PROD": "Quantidade de ovos de galinha produzidos (Dúzia)",
    "Q_DZ_VEND": "Quantidade de ovos de galinha vendidos (Dúzia)",
    "V_Q_DZ_PROD": "Valor dos ovos de galinha produzidos (R$/dúzia)",
    "V_Q_DZ_VEND": "Valor dos ovos de galinha vendidos (R$/dúzia)",
    "A_TOTAL": "Área total do estabelecimento agropecuário (ha)",
    "A_PAST_PLANT": "Área de pastagem plantada (ha)",
    "A_LAV_PERM": "Área de lavoura permanente (ha)",
    "A_LAV_TEMP": "Área de lavoura temporária (ha)",
    "A_APPRL": "Área de matas e/ou florestas naturais destinadas à preservação permanente ou reserva legal (ha)",
    "VTP_AGRO": "Valor total da produção agropecuária (R$)",
    "RECT_AGRO": "Receita total da produção agropecuária (R$)",
    "N_TRAB_TOTAL": "Total de trabalhadores em 30.09.2017",
    "N_TRAB_LACOS": "Total de trabalhadores com laços de parentesco com o produtor em 30.09.2017"
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
