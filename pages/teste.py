import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Impacto na Lucratividade",
    page_icon="📊",
    layout="centered",
)

# Título principal
st.title("💰 Fatores que Mais Impactam a Lucratividade da Granja")

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
coef_df = coef_df.sort_values("Coeficiente", key=abs, ascending=True)

# Gráfico de barras interativo
st.subheader("📈 Importância dos Fatores para a Lucratividade")
fig = px.bar(
    coef_df,
    x="Coeficiente",
    y="Fator",
    color="Categoria",
    color_discrete_map={"Positivo": "#4CAF50", "Negativo": "#F44336"},
    orientation='h',
    text_auto=True,
    labels={"Coeficiente": "Impacto no Modelo", "Fator": ""},
    height=400
)

fig.update_layout(
    hovermode="y unified",
    showlegend=False,
    yaxis={'categoryorder':'total ascending'},
    margin=dict(l=0, r=0, t=30, b=0)
)

# Destaques no gráfico
fig.add_annotation(
    x=0.85, y="Tecnologia",
    text="Maior impacto positivo",
    showarrow=True,
    arrowhead=1,
    ax=50,
    ay=0
)

fig.add_annotation(
    x=-0.75, y="Terra",
    text="Maior impacto negativo",
    showarrow=True,
    arrowhead=1,
    ax=-50,
    ay=0
)

st.plotly_chart(fig, use_container_width=True)

# Tabela de dados
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
        "Categoria": "Tipo de Impacto"
    },
    hide_index=True,
    use_container_width=True
)

# Análise automática
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
