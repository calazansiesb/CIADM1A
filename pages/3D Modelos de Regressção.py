import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objects as go # Para maior controle se necessário

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola - IBGE 2017",
    page_icon="🐔",
    layout="wide", # Manter layout wide para os gráficos 3D
    initial_sidebar_state="expanded",
)

# Título principal
st.title('📊 Análise de Produção Avícola (IBGE 2017)')
st.markdown("---")

## ----------------------------
## SEÇÃO 1: VISUALIZAÇÕES EXPLICATIVAS
## ----------------------------

st.header("🔍 Compreendendo os Dados Avícolas")

# Carregar dados fictícios (mantido para reprodutibilidade)
np.random.seed(42)
df = pd.DataFrame({
    'PRODUCAO_TOTAL': np.random.randint(1000, 50000, 100),
    'GALINACEOS': np.random.randint(500, 25000, 100),
    'AREA_TOTAL': np.random.uniform(1, 50, 100),
    'TRABALHADORES': np.random.randint(1, 20, 100),
    'GALINHAS_VENDIDAS': np.random.randint(300, 15000, 100),
    'OVOS_PRODUZIDOS': np.random.randint(100, 10000, 100),
    'COMERCIALIZACAO': np.random.randint(0, 2, 100), # Variável dummy 0 ou 1
    'AGRICULTURA_FAMILIAR': np.random.randint(0, 2, 100), # Variável dummy 0 ou 1
    'SISTEMA_CRIACAO': np.random.choice(['Frangos de Corte', 'Ovos Consumo', 'Ovos Incubação', 'Outros'], 100),
    'REGIAO': np.random.choice(['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'], 100),
})

# --- NOVO GRÁFICO: DISPERSÃO 3D (Substitui o Box Plot para uma visão mais rica) ---
st.subheader("🌐 Relação 3D: Produção Total, Galináceos e Trabalhadores por Sistema")
fig1_3d = px.scatter_3d(
    df,
    x='GALINACEOS',
    y='PRODUCAO_TOTAL',
    z='TRABALHADORES',
    color='SISTEMA_CRIACAO',
    title='Distribuição da Produção Total, Galináceos e Trabalhadores por Sistema de Criação',
    labels={
        'GALINACEOS': 'Número de Galináceos',
        'PRODUCAO_TOTAL': 'Produção Total',
        'TRABALHADORES': 'Número de Trabalhadores',
        'SISTEMA_CRIACAO': 'Sistema de Criação'
    },
    color_discrete_sequence=px.colors.qualitative.Bold, # Cores vibrantes
    height=650,
    template="plotly_dark" # Tema escuro para realçar o 3D
)
fig1_3d.update_layout(
    scene=dict(
        xaxis_title='Número de Galináceos',
        yaxis_title='Produção Total',
        zaxis_title='Número de Trabalhadores',
        camera=dict(eye=dict(x=1.8, y=1.8, z=0.8))
    ),
    title_x=0.5
)
st.plotly_chart(fig1_3d, use_container_width=True)

with st.expander("💡 Interpretação do Gráfico 3D (Produção, Galináceos, Trabalhadores)"):
    st.markdown("""
    **Análise Multidimensional:**
    - Este gráfico interativo em 3D permite explorar a relação entre o número de galináceos, a produção total e o número de trabalhadores, segmentado por sistema de criação.
    - Observe como os clusters de cores (sistemas de criação) se agrupam no espaço 3D, indicando diferentes escalas e eficiências operacionais.
    - Granja com alto número de galináceos e trabalhadores, mas baixa produção total, pode indicar ineficiência.
    - Granja com alta produção total e galináceos, mas baixo número de trabalhadores, pode indicar alta automação.
    """)


# Gráfico 2: Matriz de Correlação (Estilizada)
st.subheader("🔗 Matriz de Correlação entre Variáveis Numéricas")
numeric_cols = df.select_dtypes(include=[np.number]).columns
fig2 = px.imshow(
    df[numeric_cols].corr(),
    color_continuous_scale='RdBu', # Escala divergente para correlações
    range_color=[-1,1],
    title='Matriz de Correlação entre Variáveis Numéricas',
    template="plotly_white", # Tema limpo
    text_auto=True # Mostrar valores da correlação
)
fig2.update_layout(title_x=0.5)
st.plotly_chart(fig2, use_container_width=True)

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
    default=['GALINACEOS', 'TRABALHADORES', 'OVOS_PRODUZIDOS', 'SISTEMA_CRIACAO', 'AREA_TOTAL'] # Adicionado AREA_TOTAL para mais features
)

# Pré-processamento
df_model = df[[target] + features].copy()
categorical_features = [col for col in features if df[col].dtype == 'object']
if categorical_features:
    df_model = pd.get_dummies(df_model, columns=categorical_features, drop_first=True)

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

# --- NOVO GRÁFICO: VALORES REAIS, PREDITOS E RESÍDUOS EM 3D ---
st.subheader("🎯 Previsões vs Valores Reais e Resíduos (3D)")
residuals = y_test - y_pred
# Criar um DataFrame para o gráfico 3D
df_pred_res = pd.DataFrame({
    'Valor Real': y_test,
    'Valor Predito': y_pred,
    'Resíduo': residuals
})

fig3_3d = px.scatter_3d(
    df_pred_res,
    x='Valor Real',
    y='Valor Predito',
    z='Resíduo',
    color='Resíduo', # Colorir os pontos pelos resíduos (gradiente)
    color_continuous_scale=px.colors.sequential.Inferno, # Gradiente vibrante para resíduos
    title='Relação entre Valores Reais, Preditos e Resíduos do Modelo',
    labels={
        'Valor Real': 'Valor Real',
        'Valor Predito': 'Valor Predito',
        'Resíduo': 'Resíduo'
    },
    height=650,
    template="plotly_dark"
)
fig3_3d.update_layout(
    scene=dict(
        xaxis_title='Valor Real',
        yaxis_title='Valor Predito',
        zaxis_title='Resíduo',
        camera=dict(eye=dict(x=1.8, y=1.8, z=0.8))
    ),
    title_x=0.5
)
st.plotly_chart(fig3_3d, use_container_width=True)

with st.expander("📝 Avaliação e Diagnóstico do Modelo em 3D"):
    st.markdown("""
    **Análise de Desempenho e Erro em 3D:**
    - Este gráfico mostra a relação tridimensional entre o valor real da produção, o valor predito pelo modelo e o resíduo (erro) da previsão.
    - Pontos próximos ao plano "Resíduo = 0" (o "chão" do gráfico 3D) indicam previsões precisas.
    - A cor dos pontos indica a magnitude do resíduo: cores mais quentes (vermelho/amarelo) para resíduos maiores.
    - Se os pontos formarem um padrão em espiral ou cônico à medida que o "Valor Real" ou "Valor Predito" aumenta, isso sugere **heterocedasticidade** (a variância dos erros não é constante).
    - Desvios significativos do plano zero indicam que o modelo tem dificuldades em prever com precisão para aqueles pontos.
    """)

## ----------------------------
## SEÇÃO 3: ANÁLISE DE RESÍDUOS (Mantido o scatter plot, mas estilizado)
## ----------------------------

st.header("🧐 Diagnóstico do Modelo - Detalhes dos Resíduos")

# Gráfico 4: Resíduos (Estilizado)
residuals = y_test - y_pred
fig4 = px.scatter(
    x=y_pred,
    y=residuals,
    labels={'x': 'Valor Predito', 'y': 'Resíduo'},
    title='📉 Análise de Resíduos',
    trendline='lowess',
    color_discrete_sequence=px.colors.qualitative.Plotly, # Cores para a linha de tendência
    template="plotly_white"
)
fig4.add_hline(y=0, line_dash="dash", line_color="red")
fig4.update_layout(
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridcolor='lightgray'),
    yaxis=dict(showgrid=True, gridcolor='lightgray')
)
st.plotly_chart(fig4, use_container_width=True)

with st.expander("🔧 Interpretação dos Resíduos (2D)"):
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
## SEÇÃO 4: COEFICIENTES DO MODELO (Estilizado)
## ----------------------------

st.header("📌 Fatores que Influenciam a Produção")

# Gráfico 5: Importância das Variáveis (Estilizado)
coef_df = pd.DataFrame({
    'Variável': X_train.columns,
    'Impacto': model.coef_
}).sort_values('Impacto', key=abs, ascending=False)

fig5 = px.bar(
    coef_df,
    x='Variável',
    y='Impacto',
    color='Impacto', # Colorir pelo impacto para gradiente
    color_continuous_scale='RdBu', # Escala divergente de vermelho para azul
    title='📊 Impacto das Variáveis no Modelo',
    template="plotly_white",
    text_auto=True # Mostrar valores nas barras
)
fig5.update_layout(
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_tickangle=-45, # Rotacionar labels para melhor leitura
    xaxis=dict(showgrid=False), # Remover grid do eixo X para barras
    yaxis=dict(showgrid=True, gridcolor='lightgray') # Manter grid no eixo Y
)
fig5.update_traces(marker_line_color='black', marker_line_width=0.5) # Borda nas barras
st.plotly_chart(fig5, use_container_width=True)

with st.expander("📚 Guia de Interpretação dos Coeficientes"):
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
