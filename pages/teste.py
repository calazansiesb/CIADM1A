import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import plotly.express as px

# ============================================================
# EXPLICAÇÃO SOBRE A MATRIZ DE CORRELAÇÃO E INTERPRETAÇÃO
# ============================================================
st.info("""
**🔍 Análise da Distribuição de Densidade de Aves por Sistema de Criação**

📌 **Principais observações:**
- O sistema "Outros" apresenta concentração de estabelecimentos com menor número total de aves, predominantemente entre 6.000 e 7.000 cabeças.
- "Ovos para Consumo" e "Frangos de Corte" mostram maior dispersão, com a maioria dos registros entre 9.000 e 12.000 aves por estabelecimento.
- "Ovos para Incubação" destaca-se por concentrar-se nas faixas mais elevadas, acima de 13.000 aves.

💡 **Interpretação:**
- O gráfico evidencia diferentes perfis produtivos: sistemas voltados para incubação tendem a operar com plantéis mais numerosos, enquanto sistemas classificados como "Outros" concentram-se em pequenas criações.
- A variação na densidade sugere especialização e segmentação claras entre os sistemas de criação, refletindo demandas produtivas e estratégias distintas.
- As informações são úteis para orientar políticas de apoio e estratégias de crescimento conforme o perfil predominante de cada sistema.

---

### Análise da Matriz de Correlação entre Variáveis Numéricas

A matriz de correlação apresentada permite identificar o grau de associação linear entre as principais variáveis envolvidas na produção avícola. 

**Principais Observações:**
- **Fortes correlações positivas**:
  - Entre `PRODUCAO_TOTAL` e `OVOS_PRODUZIDOS`, indicando que o aumento da produção total está fortemente relacionado ao aumento da produção de ovos.
  - Entre `GALINHAS_VENDIDAS` e `COMERCIALIZACAO`, sugerindo que a venda de galinhas acompanha diretamente o volume comercializado.
  - Entre `TRABALHADORES` e variáveis como `PRODUCAO_TOTAL` e `GALINHAS_VENDIDAS`, o que sugere que estabelecimentos maiores (em produção ou comercialização) demandam mais mão de obra.

- **Correlação baixa ou negativa**:
  - `AGRICULTURA_FAMILIAR` apresenta correlação baixa ou negativa com a maioria das variáveis produtivas, indicando que os estabelecimentos classificados como agricultura familiar tendem a operar em menor escala, com menor produção e comercialização.
  - `AREA_TOTAL` possui correlação relativamente baixa com variáveis produtivas, sugerindo que o tamanho físico do estabelecimento não é o principal determinante do volume produtivo, provavelmente porque há intensificação em áreas menores.

**Interpretação:**
- **Especialização e Segmentação**: Assim como observado na análise da densidade de aves por sistema de criação, a matriz de correlação reforça a existência de diferentes perfis produtivos. Sistemas voltados à incubação e produção de ovos tendem a ser mais intensivos e menos familiares, enquanto sistemas menores e familiares apresentam menor produção e comercialização.
- **Políticas Públicas**: A compreensão dessas correlações é fundamental para orientar políticas públicas adequadas ao perfil de cada segmento. Por exemplo, incentivos para mecanização e capacitação podem ser mais úteis para grandes produtores, enquanto apoio técnico e acesso a mercados podem beneficiar pequenas produções familiares.

**Resumo**: A matriz de correlação evidencia que o aumento da produção está mais relacionado à intensificação do uso de mão de obra e ao perfil do sistema produtivo do que ao tamanho da área utilizada. Esta análise, em conjunto com a distribuição de densidade de aves, oferece uma visão abrangente dos fatores que diferenciam os sistemas de criação avícola no contexto analisado.
""")

# Configuração da página
st.set_page_config(
    page_title="Modelo de Regressão Avícola - IBGE 2017",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Modelo de Regressão para Produção Avícola (IBGE 2017)')
st.markdown("---")

# Carregar dados fictícios (substituir por dados reais)
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
    'SISTEMA_CRIACAO': np.random.choice(['3-SIST_PFC', '1-SIST_POC', '2-SIST_POI', '4-Outro'], 100),
    'REGIAO': np.random.choice(['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'], 100),
})

# Definir variáveis
target = 'PRODUCAO_TOTAL'
features = [
    'GALINACEOS', 'AREA_TOTAL', 'TRABALHADORES', 'GALINHAS_VENDIDAS', 
    'OVOS_PRODUZIDOS', 'COMERCIALIZACAO', 'AGRICULTURA_FAMILIAR',
    'SISTEMA_CRIACAO', 'REGIAO'
]

# =============================================
# SIDEBAR - CONFIGURAÇÕES DO MODELO
# =============================================
st.sidebar.header("Configurações do Modelo")

# Seleção de variáveis
selected_features = st.sidebar.multiselect(
    "Variáveis explicativas:",
    features,
    default=features[:5]
)

# Parâmetros do modelo
test_size = st.sidebar.slider(
    "Tamanho do conjunto de teste (%):",
    min_value=10, max_value=40, value=20
)

show_raw_data = st.sidebar.checkbox("Mostrar dados brutos", False)
show_correlations = st.sidebar.checkbox("Mostrar matriz de correlação", True)

# =============================================
# ANÁLISE EXPLORATÓRIA
# =============================================
if show_raw_data:
    st.subheader("Dados Brutos")
    st.dataframe(df)

if show_correlations:
    st.subheader("Matriz de Correlação")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='Blues',
        title='Matriz de Correlação entre Variáveis Numéricas'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# =============================================
# PREPARAÇÃO DOS DADOS
# =============================================
st.subheader("Preparação dos Dados")

# One-hot encoding para variáveis categóricas
categorical = [col for col in selected_features if df[col].dtype == 'object']
df_model = df[[target] + selected_features].copy()

if categorical:
    df_model = pd.get_dummies(df_model, columns=categorical, drop_first=True)
    st.write("Variáveis categóricas transformadas (one-hot encoding):")
    st.dataframe(df_model.head())
else:
    st.write("Nenhuma variável categórica selecionada.")

# Separação em X e y
X = df_model.drop(columns=[target])
y = df_model[target]

# Divisão treino-teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=test_size/100, 
    random_state=42
)

st.write(f"Divisão dos dados: {100-test_size}% treino, {test_size}% teste")

# =============================================
# TREINAMENTO DO MODELO
# =============================================
st.subheader("Treinamento do Modelo")

model = LinearRegression()
model.fit(X_train, y_train)

# Predição e métricas
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Exibir métricas em colunas
col1, col2, col3 = st.columns(3)
col1.metric("RMSE", f"{rmse:.2f}")
col2.metric("R²", f"{r2:.3f}")
col3.metric("Amostras de Teste", len(y_test))

# =============================================
# RESULTADOS DO MODELO
# =============================================
st.subheader("Importância das Variáveis (Coeficientes)")

coef_df = pd.DataFrame({
    'Variável': X.columns,
    'Coeficiente': model.coef_,
    'Absoluto': np.abs(model.coef_)
}).sort_values(by='Absoluto', ascending=False)

# Gráfico de importância
fig_coef = px.bar(
    coef_df,
    x='Variável',
    y='Coeficiente',
    color='Coeficiente',
    color_continuous_scale='RdBu',
    title='Coeficientes do Modelo de Regressão'
)
st.plotly_chart(fig_coef, use_container_width=True)

# Tabela de coeficientes
st.dataframe(coef_df.drop(columns=['Absoluto']))

# =============================================
# VISUALIZAÇÃO DE RESULTADOS
# =============================================
st.subheader("Valores Observados vs. Preditos")

# Gráfico scatter plot com Plotly
fig_scatter = px.scatter(
    x=y_test,
    y=y_pred,
    labels={'x': 'Valores Observados', 'y': 'Valores Preditos'},
    title='Comparação entre Valores Observados e Preditos',
    trendline="lowess"
)

# Adicionar linha de referência
fig_scatter.add_shape(
    type="line",
    x0=y_test.min(), y0=y_test.min(),
    x1=y_test.max(), y1=y_test.max(),
    line=dict(color="Red", dash="dash")
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =============================================
# ANÁLISE RESIDUAL
# =============================================
st.subheader("Análise de Resíduos")

residuals = y_test - y_pred

fig_residuals = px.scatter(
    x=y_pred,
    y=residuals,
    labels={'x': 'Valores Preditos', 'y': 'Resíduos'},
    title='Gráfico de Resíduos'
)
fig_residuals.add_hline(y=0, line_dash="dash", line_color="red")

st.plotly_chart(fig_residuals, use_container_width=True)

# =============================================
# DOWNLOAD DO MODELO
# =============================================
st.markdown("---")
st.download_button(
    label="Download dos Resultados (CSV)",
    data=coef_df.to_csv(index=False).encode('utf-8'),
    file_name='resultados_regressao_avicola.csv',
    mime='text/csv'
)

# Rodapé
st.caption("""
🔎 *Análise desenvolvida com base em dados simulados do IBGE 2017*  
📅 *Atualizado em Outubro 2023*  
""")
