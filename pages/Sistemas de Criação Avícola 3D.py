import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Análise Avícola - IBGE 2017 (Dados Reais)",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('📊 Análise de Produção Avícola (Dados Reais IBGE 2017)')
st.markdown("---")

## ----------------------------
## CARREGAMENTO E PRÉ-PROCESSAMENTO DOS DADOS REAIS
## ----------------------------

st.header("⚙️ Carregando e Preparando seus Dados Reais")

# Carregar o arquivo CSV do GitHub
github_csv_url = 'https://raw.githubusercontent.com/calazansiesb/CIADM1A/main/GALINACEOS.csv'
try:
    df = pd.read_csv(github_csv_url, sep=';')
    st.success(f"Arquivo '{github_csv_url}' carregado com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar o arquivo do GitHub: {e}. Verifique o URL ou o separador.")
    st.stop()

# Mapeamento das colunas do seu CSV para os nomes usados no script
column_mapping = {
    'GAL_TOTAL': 'GALINACEOS',
    'A_TOTAL': 'AREA_TOTAL',
    'N_TRAB_TOTAL': 'TRABALHADORES',
    'GAL_VEND': 'GALINHAS_VENDIDAS',
    'Q_DZ_PROD': 'OVOS_PRODUZIDOS',
    'E_COMERC': 'COMERCIALIZACAO',
    'E_AGRIFAM': 'AGRICULTURA_FAMILIAR',
    'SIST_CRIA': 'SISTEMA_CRIACAO',
    'NOM_TERR': 'REGIAO' # Esta será usada para filtrar e obter o nome da região/estado
}

df = df.rename(columns=column_mapping)

# --- Tratamento de Colunas ---
# Converter para numérico, tratando erros e preenchendo NaNs com 0
numeric_cols_to_convert = ['GALINACEOS', 'AREA_TOTAL', 'TRABALHADORES', 'GALINHAS_VENDIDAS', 'OVOS_PRODUZIDOS']
for col in numeric_cols_to_convert:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        st.warning(f"Coluna '{col}' não encontrada no CSV. Será preenchida com zeros.")
        df[col] = 0 # Adiciona a coluna com zeros para não quebrar o código

# Tratamento para COMERCIALIZACAO e AGRICULTURA_FAMILIAR (converter para 0/1 se necessário)
for col in ['COMERCIALIZACAO', 'AGRICULTURA_FAMILIAR']:
    if col in df.columns:
        # Assumindo que 'V' significa 'Sim' e 'F' significa 'Não' (ou similar)
        # Se os dados já forem 0/1, esta conversão não fará diferença
        df[col] = df[col].astype(str).str.strip().str.upper().map({'V': 1, 'F': 0}).fillna(0)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    else:
        st.warning(f"Coluna '{col}' não encontrada no CSV. Será preenchida com zeros.")
        df[col] = 0

# Criar PRODUCAO_TOTAL (Exemplo: soma de galinhas vendidas e ovos produzidos convertidos)
# Adapte esta lógica se 'PRODUCAO_TOTAL' tiver outra definição
if 'GALINHAS_VENDIDAS' in df.columns and 'OVOS_PRODUZIDOS' in df.columns:
    df['PRODUCAO_TOTAL'] = df['GALINHAS_VENDIDAS'] + (df['OVOS_PRODUZIDOS'] * 10) # Multiplica por 10 para dar um peso, ajuste se necessário
    st.info("Coluna 'PRODUCAO_TOTAL' criada como (GALINHAS_VENDIDAS + OVOS_PRODUZIDOS * 10).")
elif 'GALINHAS_VENDIDAS' in df.columns:
    st.warning("Coluna 'OVOS_PRODUZIDOS' não encontrada. Usando apenas GALINHAS_VENDIDAS para 'PRODUCAO_TOTAL'.")
    df['PRODUCAO_TOTAL'] = df['GALINHAS_VENDIDAS']
else:
    st.error("Não foi possível criar 'PRODUCAO_TOTAL'. Nenhuma coluna de vendas/produção de ovos encontrada.")
    st.stop()


# Mapeamento e Limpeza da coluna SISTEMA_CRIACAO
if 'SISTEMA_CRIACAO' in df.columns:
    df['SISTEMA_CRIACAO'] = df['SISTEMA_CRIACAO'].astype(str).str.strip()
    mapeamento_sistemas = {
        '1-SIST_POC': 'Produtores de Ovos p/ Consumo',
        '2-SIST_POI': 'Produtores de Ovos p/ Incubação',
        '3-SIST_PFC': 'Produtores de Frangos de Corte',
        '4-Outro': 'Outros Produtores',
        # Adicione outros mapeamentos se houver códigos diferentes em seus dados
        '1': 'Produtores de Ovos p/ Consumo',
        '2': 'Produtores de Ovos p/ Incubação',
        '3': 'Produtores de Frangos de Corte',
        '4': 'Outros Produtores'
    }
    df['SISTEMA_CRIACAO'] = df['SISTEMA_CRIACAO'].replace(mapeamento_sistemas)
    # Tratar valores que não foram mapeados (podem ser nan ou outros códigos)
    df['SISTEMA_CRIACAO'] = df['SISTEMA_CRIACAO'].fillna('Desconhecido')
    # Se ainda houver valores numéricos que não são 1,2,3,4, converter para string
    df['SISTEMA_CRIACAO'] = df['SISTEMA_CRIACAO'].apply(lambda x: str(x) if isinstance(x, (int, float)) and x not in [1,2,3,4] else x)

else:
    st.warning("A coluna 'SISTEMA_CRIACAO' não foi encontrada. Alguns gráficos podem ser afetados.")
    df['SISTEMA_CRIACAO'] = 'Desconhecido' # Preencher com valor padrão

# Limpeza da coluna REGIAO (NOM_TERR)
if 'REGIAO' in df.columns:
    df['REGIAO'] = df['REGIAO'].astype(str).str.strip().str.title()
else:
    st.warning("A coluna 'REGIAO' (NOM_TERR) não foi encontrada.")
    df['REGIAO'] = 'Desconhecida'

# --- Exibindo os dados processados (opcional) ---
if st.checkbox("Mostrar dados processados (amostra)", value=False):
    st.dataframe(df.head())
    st.write(f"Tamanho do DataFrame: {df.shape[0]} linhas, {df.shape[1]} colunas")
    st.dataframe(df.describe())

st.markdown("---")


## ----------------------------
## SEÇÃO 1: VISUALIZAÇÕES EXPLICATIVAS
## ----------------------------

st.header("🔍 Compreendendo os Dados Avícolas")

# --- NOVO GRÁFICO: DISPERSÃO 3D (Substitui o Box Plot para uma visão mais rica) ---
st.subheader("🌐 Relação 3D: Produção Total, Galináceos e Trabalhadores por Sistema")
# Filtrar NaNs para as colunas usadas no gráfico 3D
df_plot_3d_1 = df.dropna(subset=['GALINACEOS', 'PRODUCAO_TOTAL', 'TRABALHADORES', 'SISTEMA_CRIACAO']).copy()

if not df_plot_3d_1.empty:
    fig1_3d = px.scatter_3d(
        df_plot_3d_1,
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
        color_discrete_sequence=px.colors.qualitative.Bold,
        height=650,
        template="plotly_dark"
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
        - Granjas com alto número de galináceos e trabalhadores, mas baixa produção total, podem indicar ineficiência.
        - Granjas com alta produção total e galináceos, mas baixo número de trabalhadores, podem indicar alta automação.
        """)
else:
    st.warning("Não há dados suficientes para gerar o gráfico 3D de Produção Total, Galináceos e Trabalhadores. Verifique os valores nas colunas.")


# Gráfico 2: Matriz de Correlação (Estilizada)
st.subheader("🔗 Matriz de Correlação entre Variáveis Numéricas")
# Selecionar apenas as colunas numéricas relevantes para a correlação
numeric_cols_for_corr = [
    'PRODUCAO_TOTAL', 'GALINACEOS', 'AREA_TOTAL', 'TRABALHADORES',
    'GALINHAS_VENDIDAS', 'OVOS_PRODUZIDOS'
]
# Filtrar as colunas que realmente existem no DataFrame
existing_numeric_cols = [col for col in numeric_cols_for_corr if col in df.columns]

if len(existing_numeric_cols) > 1: # Precisa de pelo menos duas colunas para correlação
    corr_matrix = df[existing_numeric_cols].corr()
    fig2 = px.imshow(
        corr_matrix,
        color_continuous_scale='RdBu',
        range_color=[-1,1],
        title='Matriz de Correlação entre Variáveis Numéricas',
        template="plotly_white",
        text_auto=True
    )
    fig2.update_layout(title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("🔎 Análise de Correlações"):
        st.markdown("""
        **Principais Relações:**
        - Este gráfico mostra a força e a direção da relação linear entre pares de variáveis numéricas.
        - Valores próximos a +1 (azul escuro) indicam forte correlação positiva.
        - Valores próximos a -1 (vermelho escuro) indicam forte correlação negativa.
        - Valores próximos a 0 (branco/cinza) indicam pouca ou nenhuma correlação linear.
        """)
else:
    st.warning("Não há colunas numéricas suficientes para gerar a matriz de correlação.")


## ----------------------------
## SEÇÃO 2: MODELO DE REGRESSÃO
## ----------------------------

st.header("📈 Modelo Preditivo de Produção")

# Configuração do modelo
target = 'PRODUCAO_TOTAL'
# Verificar se as colunas existem antes de adicioná-las aos padrões
default_features = ['GALINACEOS', 'TRABALHADORES', 'OVOS_PRODUZIDOS']
if 'SISTEMA_CRIACAO' in df.columns:
    default_features.append('SISTEMA_CRIACAO')
if 'AREA_TOTAL' in df.columns:
    default_features.append('AREA_TOTAL')
if 'COMERCIALIZACAO' in df.columns:
    default_features.append('COMERCIALIZACAO')
if 'AGRICULTURA_FAMILIAR' in df.columns:
    default_features.append('AGRICULTURA_FAMILIAR')

# Garantir que as colunas padrão realmente existem no df antes de passá-las para multiselect
available_cols_for_features = [col for col in df.columns.drop(target, errors='ignore') if col in default_features]


features = st.multiselect(
    "Selecione as variáveis preditoras:",
    df.columns.drop(target, errors='ignore'),
    default=available_cols_for_features
)

# Pré-processamento
df_model = df[[target] + features].copy()
categorical_features = [col for col in features if col in df.columns and df[col].dtype == 'object']
if categorical_features:
    df_model = pd.get_dummies(df_model, columns=categorical_features, drop_first=True)

# Remover linhas com NaNs na df_model, caso haja valores que não foram tratados
df_model = df_model.dropna()

if df_model.empty or target not in df_model.columns or len(df_model.columns) < 2:
    st.error("Não há dados suficientes ou colunas válidas para treinar o modelo após o pré-processamento. Verifique a seleção de variáveis.")
    st.stop()

# Divisão dos dados
try:
    X = df_model.drop(columns=[target])
    y = df_model[target]
    
    if X.empty or len(X) < 2 or y.empty or len(y) < 2:
        st.error("Dados insuficientes para treinamento do modelo após a divisão. Verifique o tamanho do dataset e as features selecionadas.")
        st.stop()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )
except Exception as e:
    st.error(f"Erro na divisão dos dados para treinamento do modelo: {e}. Verifique se a variável alvo '{target}' e as features estão corretas.")
    st.stop()

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
df_pred_res = pd.DataFrame({
    'Valor Real': y_test,
    'Valor Predito': y_pred,
    'Resíduo': residuals
})

if not df_pred_res.empty:
    fig3_3d = px.scatter_3d(
        df_pred_res,
        x='Valor Real',
        y='Valor Predito',
        z='Resíduo',
        color='Resíduo',
        color_continuous_scale=px.colors.sequential.Inferno,
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
else:
    st.warning("Não há dados suficientes para gerar o gráfico 3D de Previsões vs Valores Reais e Resíduos.")

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
    color_discrete_sequence=px.colors.qualitative.Plotly,
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
## SEÇÃO 4: COEFICIENTES DO MODELO
## ----------------------------

st.header("📌 Fatores que Influenciam a Produção")

# Gráfico 5: Importância das Variáveis (Estilizado)
# Garantir que os coeficientes correspondam às colunas de X_train
if hasattr(model, 'coef_') and len(model.coef_) == len(X_train.columns):
    coef_df = pd.DataFrame({
        'Variável': X_train.columns,
        'Impacto': model.coef_
    }).sort_values('Impacto', key=abs, ascending=False)

    fig5 = px.bar(
        coef_df,
        x='Variável',
        y='Impacto',
        color='Impacto',
        color_continuous_scale='RdBu',
        title='📊 Impacto das Variáveis no Modelo',
        template="plotly_white",
        text_auto=True
    )
    fig5.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )
    fig5.update_traces(marker_line_color='black', marker_line_width=0.5)
    st.plotly_chart(fig5, use_container_width=True)

    with st.expander("📚 Guia de Interpretação dos Coeficientes"):
        st.markdown("""
        **Coeficientes Positivos:**
        - Aumento na variável → Aumento na produção
        - Coeficientes maiores (em valor absoluto) indicam maior impacto.
        
        **Coeficientes Negativos:**
        - Aumento na variável → Redução na produção
        
        **Comparação:**
        - Observe quais variáveis têm o maior impacto, positivo ou negativo, na produção.
        """)
else:
    st.warning("Não foi possível gerar o gráfico de impacto das variáveis. O modelo pode não ter sido treinado ou não há coeficientes válidos.")


# Rodapé
st.markdown("---")
st.caption("""
🔍 Análise desenvolvida com dados reais do IBGE 2017 | 
📅 Atualizado em Maio 2024 | 
🛠️ Ferramentas: Python, Scikit-learn, Plotly
""")
