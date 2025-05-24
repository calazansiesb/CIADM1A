import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Análise de Lucratividade Avícola",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('📈 Fatores que Impactam a Lucratividade da Granja')
st.markdown("---")

## ----------------------------
## SEÇÃO 1: VISUALIZAÇÃO DOS FATORES
## ----------------------------

# Dados dos coeficientes
coef_data = {
    "Fator": ["Tecnologia", "Terra", "Mão de Obra", "Marketing", "Capital", "Insumos", 
             "Qualidade", "Logística", "Sanidade", "Clima"],
    "Impacto": [0.9, -0.8, 0.5, -0.3, 0.2, -0.1, 0.7, -0.4, 0.6, -0.2],
    "Categoria": ["Positivo", "Negativo", "Positivo", "Negativo", "Positivo", "Negativo",
                "Positivo", "Negativo", "Positivo", "Negativo"]
}

coef_df = pd.DataFrame(coef_data)
coef_df = coef_df.sort_values("Impacto", key=abs, ascending=False).head(10)

# Gráfico de barras interativo
fig = px.bar(coef_df, 
             x="Fator", 
             y="Impacto",
             color="Categoria",
             color_discrete_map={
                 "Positivo": "#4CAF50",
                 "Negativo": "#F44336"
             },
             title="📊 Top Fatores que Impactam a Lucratividade",
             labels={"Impacto": "Coeficiente de Impacto"},
             text_auto=True,
             height=500)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="",
    yaxis_title="Força do Impacto",
    showlegend=False
)

# Destaque os maiores impactos
fig.add_annotation(
    x="Tecnologia", y=0.9,
    text="Maior impacto positivo",
    showarrow=True,
    arrowhead=1,
    ax=0, ay=-40
)

fig.add_annotation(
    x="Terra", y=-0.8,
    text="Maior impacto negativo",
    showarrow=True,
    arrowhead=1,
    ax=0, ay=40
)

st.plotly_chart(fig, use_container_width=True)

## ----------------------------
## SEÇÃO 2: ANÁLISE DOS RESULTADOS
## ----------------------------

st.header("🔍 Interpretação dos Fatores")

# Criar colunas para organização
col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Fatores Positivos")
    st.markdown("""
    - **Tecnologia (0.90)**: Automação e sistemas de monitoramento
    - **Qualidade (0.70)**: Padrões de produção e certificações
    - **Sanidade (0.60)**: Controle de doenças e biossegurança
    - **Mão de Obra (0.50)**: Treinamento e especialização
    - **Capital (0.20)**: Investimento em infraestrutura
    """)

with col2:
    st.subheader("❌ Fatores Negativos")
    st.markdown("""
    - **Terra (-0.80)**: Custo de expansão e manutenção
    - **Logística (-0.40)**: Transporte e distribuição
    - **Marketing (-0.30)**: Custos de promoção e divulgação
    - **Clima (-0.20)**: Variáveis meteorológicas
    - **Insumos (-0.10)**: Preço de ração e medicamentos
    """)

## ----------------------------
## SEÇÃO 3: RECOMENDAÇÕES ESTRATÉGICAS
## ----------------------------

st.header("🚀 Recomendações para Aumentar a Lucratividade")

with st.expander("📌 Estratégias Baseadas nos Dados", expanded=True):
    st.markdown("""
    **1. Priorize Investimentos em Tecnologia**  
    → Sistemas de automação podem gerar até 90% mais lucro  
    → Monitoramento em tempo real reduz perdas  
    
    **2. Otimize o Uso da Terra**  
    → Evite expansões desnecessárias (-80% impacto)  
    → Considere sistemas verticais ou intensivos  
    
    **3. Fortaleça Controles Sanitários**  
    → 60% de impacto positivo na lucratividade  
    → Programas preventivos reduzem custos com doenças  
    
    **4. Melhore a Qualidade dos Produtos**  
    → Diferencial competitivo com 70% de retorno  
    → Certificações agregam valor  
    """)

## ----------------------------
## SEÇÃO 4: DADOS DETALHADOS
## ----------------------------

st.header("📋 Detalhes Técnicos")

# Tabela interativa
st.dataframe(
    coef_df.sort_values("Impacto", ascending=False),
    column_config={
        "Fator": st.column_config.TextColumn("Fator Analisado"),
        "Impacto": st.column_config.NumberColumn(
            "Força do Impacto",
            format="%.2f",
            help="Coeficiente padronizado do modelo de regressão"
        ),
        "Categoria": st.column_config.TextColumn("Natureza do Impacto")
    },
    hide_index=True,
    use_container_width=True
)

# Gráfico adicional - Distribuição dos impactos
st.subheader("📈 Distribuição dos Fatores de Impacto")
fig2 = px.pie(coef_df, 
             names="Categoria", 
             values=coef_df["Impacto"].abs(),
             hole=0.4,
             title="Proporção do Impacto Total por Categoria")
st.plotly_chart(fig2, use_container_width=True)

## ----------------------------
## RODAPÉ
## ----------------------------
st.markdown("---")
st.caption("""
🔬 Análise desenvolvida com base em modelo de regressão multivariada |  
📅 Atualizado em Junho 2023 |  
📊 Fonte: Dados simulados para fins demonstrativos
""")
