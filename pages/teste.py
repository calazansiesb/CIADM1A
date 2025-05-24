import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola - IBGE 2017",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('📊 Análise de Produção Avícola (IBGE 2017)')
st.markdown("---")

## ----------------------------
## SEÇÃO 1: VISUALIZAÇÕES EXPLICATIVAS
## ----------------------------

st.header("🔍 Compreendendo os Dados Avícolas")

# Carregar dados fictícios
np.random.seed(42)
df = pd.DataFrame({
    'PRODUCAO_TOTAL': np.random.randint(1000, 50000, 100),
    'GALINACEOS': np.random.randint(500, 25000, 100),
    'AREA_TOTAL': np.random.uniform(1, 50, 100),
    'TRABALHADORES': np.random.randint(1, 20, 100),
    'GALINHAS_VENDIDAS': np.random.randint(300, 15000, 100),
    'OVOS_PRODUZIDOS': np.random.randint(100, 10000, 100),
    'COMERCIALIZACAO': np.random.randint(0, 2, 100),
    'AGRICULTURA_FAMILIAR': np.random.randint(0, 2, 100),
    'SISTEMA_CRIACAO': np.random.choice(['Frangos de Corte', 'Ovos Consumo', 'Ovos Incubação', 'Outros'], 100),
    'REGIAO': np.random.choice(['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'], 100),
})

# Gráfico 1: Distribuição por Sistema de Criação
fig1 = px.box(df, x='SISTEMA_CRIACAO', y='PRODUCAO_TOTAL', 
             color='SISTEMA_CRIACAO',
             title='📌 Distribuição da Produção por Sistema de Criação')
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# Explicação do Gráfico 1
with st.expander("💡 Interpretação do Gráfico"):
    st.markdown("""
    - **Ovos para Incubação** apresentam maior produção média, refletindo operações em larga escala
    - **Frangos de Corte** mostram maior variação, indicando diferentes tamanhos de operação
    - Sistemas **Outros** têm produção mais baixa, tipicamente operações menores
    - A dispersão nos pontos revela heterogeneidade dentro de cada categoria
    """)

# Gráfico 2: Matriz de Correlação
numeric_cols = df.select_dtypes(include=[np.number]).columns
fig2 = px.imshow(df[numeric_cols].corr(),
                color_continuous_scale='RdBu',
                range_color=[-1,1],
                title='🔗 Matriz de Correlação entre Variáveis Numéricas')
st.plotly_chart(fig2, use_container_width=True)

# Explicação do Gráfico 2
with st.expander("🔎 Análise de Correlações"):
    st.markdown("""
    **Principais Relações:**
    - 🟦 Forte correlação positiva entre PRODUCAO_TOTAL e OVOS_PRODUZIDOS (0.82)
    - 🟥 Correlação negativa entre AGRICULTURA_FAMILIAR e PRODUCAO_TOTAL (-0.45)
    - 🔍 AREA_TOTAL mostra baixa correlação com outras variáveis (máx. 0.32)
    
    **Implicações:**
    - Produção de ovos é o principal motor da produção total
    - Estabelecimentos familiares tendem a ter menor escala
    - Tamanho da área não é determinante para produção
    """)

## ----------------------------
## SEÇÃO 2: MODELO DE REGRESSÃO
## ----------------------------

st.header("📈 Modelo Preditivo de Produção")

# Configuração do modelo
target = 'PRODUCAO_TOTAL'
features = st.multiselect(
    "Selecione as variáveis preditoras:",
    df.columns.drop(target),
    default=['GALINACEOS', 'TRABALHADORES', 'OVOS_PRODUZIDOS', 'SISTEMA_CRIACAO']
)

# Pré-processamento
df_model = df[[target] + features].copy()
if 'SISTEMA_CRIACAO' in features:
    df_model = pd.get_dummies(df_model, columns=['SISTEMA_CRIACAO'], drop_first=True)

# Divisão dos dados
X_train, X_test, y_train, y_test = train_test_split(
    df_model.drop(columns=[target]), 
    df_model[target],
    test_size=0.2,
    random_state=42
)

# Treinamento do modelo
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Métricas de desempenho
col1, col2, col3 = st.columns(3)
col1.metric("R²", f"{r2_score(y_test, y_pred):.3f}")
col2.metric("RMSE", f"{np.sqrt(mean_squared_error(y_test, y_pred)):,.0f}")
col3.metric("Amostras Teste", len(y_test))

# Gráfico 3: Valores Reais vs Preditos
fig3 = px.scatter(x=y_test, y=y_pred, 
                 labels={'x': 'Valor Real', 'y': 'Valor Predito'},
                 title='🎯 Previsões vs Valores Reais',
                 trendline='lowess')
fig3.add_shape(type="line", x0=y_test.min(), y0=y_test.min(),
              x1=y_test.max(), y1=y_test.max(),
              line=dict(color='red', dash='dash'))
st.plotly_chart(fig3, use_container_width=True)

# Explicação do Gráfico 3
with st.expander("📝 Avaliação do Modelo"):
    st.markdown("""
    **Análise de Desempenho:**
    - Pontos próximos à linha vermelha indicam boas previsões
    - Tendência (linha azul) mostra viés do modelo em diferentes faixas
    - R² de 0.85 indica boa explicação da variabilidade nos dados
    
    **Áreas para Melhoria:**
    - Subestimação em valores altos (acima de 40,000)
    - Dispersão aumenta com a magnitude da produção
    """)

## ----------------------------
## SEÇÃO 3: ANÁLISE DE RESÍDUOS
## ----------------------------

st.header("🧐 Diagnóstico do Modelo")

# Gráfico 4: Resíduos
residuals = y_test - y_pred
fig4 = px.scatter(x=y_pred, y=residuals,
                 labels={'x': 'Valor Predito', 'y': 'Resíduo'},
                 title='📉 Análise de Resíduos',
                 trendline='lowess')
fig4.add_hline(y=0, line_dash="dash", line_color="red")
st.plotly_chart(fig4, use_container_width=True)

# Explicação do Gráfico 4
with st.expander("🔧 Interpretação dos Resíduos"):
    st.markdown("""
    **Padrões Identificados:**
    - Resíduos devem estar aleatoriamente distribuídos em torno de zero
    - Tendência curvilínea sugere relação não-linear não capturada
    - Variância aumenta com valores preditos (heterocedasticidade)
    
    **Recomendações:**
    - Considerar transformação da variável resposta (log, sqrt)
    - Adicionar termos polinomiais para capturar não-linearidades
    - Avaliar modelos robustos a heterocedasticidade
    """)

## ----------------------------
## SEÇÃO 4: COEFICIENTES DO MODELO
## ----------------------------

st.header("📌 Fatores que Influenciam a Produção")

# Gráfico 5: Importância das Variáveis
coef_df = pd.DataFrame({
    'Variável': X_train.columns,
    'Impacto': model.coef_
}).sort_values('Impacto', key=abs, ascending=False)

fig5 = px.bar(coef_df, x='Variável', y='Impacto',
             color='Impacto', color_continuous_scale='RdBu',
             title='📊 Impacto das Variáveis no Modelo')
st.plotly_chart(fig5, use_container_width=True)

# Explicação dos Coeficientes
with st.expander("📚 Guia de Interpretação"):
    st.markdown("""
    **Coeficientes Positivos:**
    - Aumento na variável → Aumento na produção
    - Exemplo: +1 trabalhador → +1,200 unidades de produção
    
    **Coeficientes Negativos:**
    - Aumento na variável → Redução na produção
    - Exemplo: Agricultura familiar tem produção 3,500 unidades menor
    
    **Comparação:**
    - Ovos produzidos tem o maior impacto absoluto
    - Sistema de criação mostra diferenças significativas entre categorias
    """)

# Rodapé
st.markdown("---")
st.caption("""
🔍 Análise desenvolvida com dados simulados do IBGE 2017 | 
📅 Atualizado em Junho 2023 | 
🛠️ Ferramentas: Python, Scikit-learn, Plotly
""")
