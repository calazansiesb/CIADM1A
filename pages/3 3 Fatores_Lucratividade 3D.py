import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Impacto na Lucratividade (3D)",
    page_icon="📊",
    layout="wide", # Mudar para wide para melhor visualização 3D
)

# Título principal
st.title("💰 Fatores que Mais Impactam a Lucratividade da Granja (Visualização 3D)")

# Dados dos coeficientes
coefs = {
    "Tecnologia": 0.9,
    "Terra": -0.8,
    "Mão de Obra": 0.5,
    "Marketing": -0.3,
    "Capital": 0.2,
    "Insumos": -0.1,
}

# Preparação dos dados
coef_df = pd.DataFrame(list(coefs.items()), columns=["Fator", "Coeficiente"])
coef_df["Categoria"] = coef_df["Coeficiente"].apply(lambda x: "Positivo" if x > 0 else "Negativo")
# Adicionar uma "terceira dimensão" para o 3D: pode ser a Magnitude
coef_df["Magnitude_Absoluta"] = coef_df["Coeficiente"].abs()
# Ou uma variável dummy fixa para apenas visualizar os pontos em um plano 3D:
# coef_df["Z_Dummy"] = 1 # Todos os pontos em Z=1

coef_df = coef_df.sort_values("Coeficiente", key=abs, ascending=True)

# Gráfico de Dispersão 3D
st.subheader("🌐 Visualização 3D dos Coeficientes de Impacto")

fig_3d = px.scatter_3d(
    coef_df,
    x="Fator",
    y="Coeficiente",
    z="Magnitude_Absoluta", # Usar a magnitude como o terceiro eixo (profundidade)
    color="Categoria", # Colorir pela categoria (Positivo/Negativo)
    color_discrete_map={"Positivo": "#4CAF50", "Negativo": "#F44336"},
    size="Magnitude_Absoluta", # Fazer o tamanho do ponto proporcional à magnitude
    hover_name="Fator",
    hover_data={"Coeficiente": ":.2f", "Magnitude_Absoluta": False}, # Mostrar coeficiente no hover, ocultar magnitude
    title='Impacto dos Fatores na Lucratividade (3D)',
    labels={
        "Fator": "Fator",
        "Coeficiente": "Coeficiente de Impacto",
        "Magnitude_Absoluta": "Magnitude do Impacto"
    },
    height=600,
    template="plotly_dark" # Tema escuro para um visual mais "tecnológico" em 3D
)

fig_3d.update_layout(
    scene = dict(
        xaxis_title='Fator',
        yaxis_title='Coeficiente de Impacto',
        zaxis_title='Magnitude Absoluta',
        # Ajustar a câmera para uma melhor visão inicial
        camera = dict(
            eye=dict(x=1.8, y=1.8, z=0.8) # Mais de cima e de lado
        )
    )
)

st.plotly_chart(fig_3d, use_container_width=True)

with st.expander("💡 Interpretação do Gráfico 3D"):
    st.info("""
    **🌐 Análise do Gráfico de Dispersão 3D:**
    Este gráfico tenta representar a magnitude do impacto de cada fator em uma terceira dimensão.
    - **Eixo X (Fator):** Mostra os diferentes fatores.
    - **Eixo Y (Coeficiente de Impacto):** Indica se o impacto é positivo ou negativo e sua força.
    - **Eixo Z (Magnitude do Impacto):** Representa o valor absoluto do coeficiente, ou seja, o quão forte é o impacto, independentemente de ser positivo ou negativo.
    - O tamanho e a cor dos pontos também reforçam a categoria (positivo/negativo) e a magnitude.

    **💡 Interpretação:**
    - Fatores com maior magnitude (ponto mais alto no eixo Z e/ou ponto maior) são os mais relevantes para a lucratividade, seja positiva ou negativamente.
    - A visualização 3D permite girar o gráfico para observar as relações de diferentes ângulos.
    - **Tecnologia** (verde, ponto maior) e **Terra** (vermelho, ponto maior) se destacam pela sua alta magnitude no eixo Z, confirmando seu papel crucial.
    """)


# Tabela de dados (mantida)
st.subheader("📋 Detalhes dos Coeficientes")
st.dataframe(
    coef_df.sort_values("Coeficiente", ascending=False),
    column_config={
        "Fator": "Fator Analisado",
        "Coeficiente": st.column_config.NumberColumn(
            "Impacto",
            format="%.2f",
            help="Coeficiente padronizado do modelo"
        ),
        "Categoria": "Tipo de Impacto",
        "Magnitude_Absoluta": "Magnitude" # Mostrar a nova coluna
    },
    hide_index=True,
    use_container_width=True
)

# Análise automática (mantida)
st.markdown("---")
st.subheader("🔎 Principais Insights")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Fator Mais Positivo",
        value="Tecnologia",
        delta="Coef: +0.90"
    )
    st.markdown("""
    **Recomendações:**
    - Investir em automação
    - Adotar sistemas de monitoramento
    - Implementar tecnologias de precisão
    """)

with col2:
    st.metric(
        label="Fator Mais Negativo",
        value="Terra",
        delta="Coef: -0.80"
    )
    st.markdown("""
    **Recomendações:**
    - Otimizar uso do espaço
    - Considerar sistemas verticais
    - Reduzir expansões desnecessárias
    """)

# Rodapé
st.markdown("---")
st.caption("Análise desenvolvida com base em modelo de regressão linear multivariada | Dados simulados")
