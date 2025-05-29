import streamlit as st
import plotly.express as px
import pandas as pd

# URL do novo arquivo CSV no GitHub (versão raw)
url_novo = "https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/correlacao_resultado.csv"

# Carregar os dados corretamente
# Tenta carregar com ';' como separador, se falhar, tenta com ','
try:
    df_corr = pd.read_csv(url_novo, sep=";", encoding="utf-8", index_col=0)
except Exception:
    df_corr = pd.read_csv(url_novo, encoding="utf-8", index_col=0)

# Dicionário de descrições das variáveis
# Este dicionário é usado para exibir nomes mais amigáveis na interface
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

# Garante que todas as colunas no DataFrame de correlação tenham uma descrição
# Se uma coluna não estiver no dicionário, usa o próprio nome da coluna como fallback
for col in df_corr.columns:
    if col not in descricao_variaveis:
        descricao_variaveis[col] = col

# Configuração da interface do Streamlit
st.title("Mapa de Calor de Correlação entre Métricas")

# Multi-seleção para as variáveis a serem exibidas no mapa de calor
all_variables = df_corr.columns.tolist()
selected_variables = st.multiselect(
    "Selecione as variáveis para exibir no mapa de calor:",
    options=all_variables,
    default=all_variables, # Por padrão, todas as variáveis são selecionadas
    format_func=lambda x: descricao_variaveis.get(x, x) # Exibe nomes amigáveis
)

# Verifica se alguma variável foi selecionada antes de gerar o gráfico
if not selected_variables:
    st.warning("Por favor, selecione pelo menos uma variável para exibir o mapa de calor.")
else:
    # Filtra o DataFrame de correlação com base nas variáveis selecionadas
    df_filtered_corr = df_corr.loc[selected_variables, selected_variables]

    # Renomeia os índices e colunas do DataFrame filtrado para as descrições completas
    # Isso torna o mapa de calor mais legível
    df_filtered_corr.index = [descricao_variaveis.get(var, var) for var in df_filtered_corr.index]
    df_filtered_corr.columns = [descricao_variaveis.get(var, var) for var in df_filtered_corr.columns]

    # Cria o mapa de calor usando plotly.express.imshow
    fig = px.imshow(
        df_filtered_corr,
        text_auto=True, # Exibe os valores de correlação nas células do mapa
        color_continuous_scale=px.colors.sequential.RdBu, # Escala de cores divergente (vermelho-azul)
        title="Mapa de Calor de Correlação",
        labels=dict(x="Variável", y="Variável", color="Coeficiente de Correlação")
    )

    # Melhora o layout do mapa de calor para melhor visualização
    fig.update_xaxes(side="top") # Coloca os rótulos do eixo X na parte superior
    fig.update_layout(
        xaxis_showgrid=False, # Remove as grades do eixo X
        yaxis_showgrid=False, # Remove as grades do eixo Y
        xaxis_nticks=len(selected_variables), # Garante que todos os rótulos do eixo X sejam exibidos
        yaxis_nticks=len(selected_variables), # Garante que todos os rótulos do eixo Y sejam exibidos
        height=600, # Define a altura do gráfico
        width=800 # Define a largura do gráfico
    )

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig)

    # Expander para exibir sugestões adicionais de análises de correlação
    with st.expander("Sugestões de Análises de Correlação"):
        st.write(f"""
        Este mapa de calor exibe os coeficientes de correlação entre as variáveis selecionadas.
        - **Valores próximos a 1 (vermelho forte):** Indicam uma forte correlação positiva. Isso significa que, quando uma variável aumenta, a outra tende a aumentar também.
        - **Valores próximos a -1 (azul forte):** Indicam uma forte correlação negativa. Isso significa que, quando uma variável aumenta, a outra tende a diminuir.
        - **Valores próximos a 0 (branco/cinza):** Indicam pouca ou nenhuma correlação linear entre as variáveis.

        **Sugestões de pares de variáveis para análise:**

        **1. Correlação entre Produção e Valor de Venda:**
        - **Variáveis:** `{descricao_variaveis["GAL_TOTAL"]}` e `{descricao_variaveis["V_GAL_VEND"]}`
        - **Objetivo:** Verificar se um maior número de galináceos está diretamente associado a um maior valor de vendas. Uma correlação positiva forte seria esperada, indicando que mais produção leva a mais receita.

        **2. Impacto da Orientação Técnica na Receita:**
        - **Variáveis:** `{descricao_variaveis["E_RECEBE_ORI"]}` e `{descricao_variaveis["RECT_AGRO"]}`
        - **Objetivo:** Analisar se estabelecimentos que recebem orientação técnica tendem a ter uma receita agropecuária total maior. Uma correlação positiva aqui sugeriria a eficácia da orientação.

        **3. Relação entre Poedeiras e Venda de Ovos:**
        - **Variáveis:** `{descricao_variaveis["GAL_POED"]}` e `{descricao_variaveis["Q_DZ_VEND"]}`
        - **Objetivo:** Observar a força da correlação entre o número de galináceos poedeiras e a quantidade de dúzias de ovos vendidas. Uma correlação forte indicaria que o tamanho do plantel de poedeiras é um bom preditor da produção de ovos.

        **4. Financiamento e Crescimento da Produção:**
        - **Variáveis:** `{descricao_variaveis["E_FINANC"]}` e `{descricao_variaveis["GAL_TOTAL"]}` (ou `{descricao_variaveis["VTP_AGRO"]}`)
        - **Objetivo:** Investigar se o acesso a financiamento (seja geral ou de cooperativas) está correlacionado com o aumento do efetivo de galináceos ou do valor total da produção. Uma correlação positiva pode indicar que o financiamento impulsiona o crescimento.

        **5. Associação a Cooperativas e Comercialização:**
        - **Variáveis:** `{descricao_variaveis["E_ASSOC_COOP"]}` e `{descricao_variaveis["E_COMERC"]}` (ou `{descricao_variaveis["V_GAL_VEND"]}`)
        - **Objetivo:** Entender se a associação a cooperativas influencia a propensão a ter estabelecimentos comerciais ou o valor de galináceos vendidos. Uma correlação positiva poderia indicar benefícios da associação.

        **Lembre-se:** Correlação não implica causalidade. Este mapa ajuda a identificar relações lineares, mas outros fatores podem estar envolvidos e a correlação não prova que uma variável causa a outra.
        """)
