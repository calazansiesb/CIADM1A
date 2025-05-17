import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

st.title("Modelos de Regressão: Receita Total Agropecuária (RECT_AGRO)")

# Exemplo: Carregue/importe seu DataFrame aqui
np.random.seed(0)
df = pd.DataFrame({
    'RECT_AGRO': np.random.randint(10000, 100000, 100),
    'GAL_TOTAL': np.random.randint(1000, 15000, 100),
    'A_TOTAL': np.random.uniform(1, 50, 100),
    'N_TRAB_TOTAL': np.random.randint(1, 20, 100),
    'GAL_VEND': np.random.randint(500, 12000, 100),
    'Q_DZ_PROD': np.random.randint(100, 10000, 100),
    'E_COMERC': np.random.randint(0, 2, 100),
    'E_AGRIFAM': np.random.randint(0, 2, 100),
    'SIST_CRIA': np.random.choice(['Convencional', 'Caipira', 'Orgânico'], 100),
    'NIV_TERR': np.random.choice(['Municipal', 'Estadual', 'Regional'], 100),
})

target = 'RECT_AGRO'
features = [
    'GAL_TOTAL', 'A_TOTAL', 'N_TRAB_TOTAL', 'GAL_VEND', 'Q_DZ_PROD',
    'E_COMERC', 'E_AGRIFAM', 'SIST_CRIA', 'NIV_TERR'
]

# Seleção de variáveis explicativas (features)
st.sidebar.header("Selecione as variáveis para o modelo")
selected_features = st.sidebar.multiselect(
    "Variáveis explicativas:",
    features,
    default=features
)

# Pré-processamento
categorical = [col for col in selected_features if df[col].dtype == 'object' or df[col].dtype.name == 'category']
df_model = df[[target] + selected_features].copy()
if categorical:
    df_model = pd.get_dummies(df_model, columns=categorical, drop_first=True)

X = df_model.drop(columns=[target])
y = df_model[target]

# Divisão treino-teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

st.success(f"Métricas do Modelo de Regressão Linear:")
st.write(f"**RMSE:** {rmse:.2f}")
st.write(f"**R²:** {r2:.3f}")

coef_df = pd.DataFrame({
    'Variável': X.columns,
    'Coeficiente': model.coef_
}).sort_values(by='Coeficiente', key=abs, ascending=False)

st.subheader("Importância das Variáveis (Coeficientes)")
st.dataframe(coef_df)

# GRÁFICO DE IMPORTÂNCIA DAS VARIÁVEIS
st.subheader("Fatores que Mais Impactam a Lucratividade")
fig, ax = plt.subplots(figsize=(8, 5))
coef_df_plot = coef_df.copy()
coef_df_plot['Sinal'] = coef_df_plot['Coeficiente'].apply(lambda x: 'Positivo' if x > 0 else 'Negativo')
coef_df_plot = coef_df_plot.sort_values('Coeficiente', key=abs, ascending=True)
bars = ax.barh(coef_df_plot['Variável'], coef_df_plot['Coeficiente'], 
        color=coef_df_plot['Sinal'].map({'Positivo':'#4caf50', 'Negativo':'#e57373'}))
ax.set_xlabel('Peso no Modelo (Coeficiente)')
ax.set_title('Importância dos Fatores para a Receita Total')
st.pyplot(fig)

# ANÁLISE AUTOMÁTICA DE OTIMIZAÇÃO
st.markdown("**Sugestão Automática de Otimização:**")
top_var = coef_df.iloc[0]
if top_var['Coeficiente'] > 0:
    sinal = "aumentar"
else:
    sinal = "reduzir"
st.write(
    f"O fator que mais impacta positivamente a receita é **{top_var['Variável']}**. "
    f"Para maximizar a receita, recomenda-se {sinal} esse fator na granja, considerando custos e viabilidade."
)
st.caption(
    "Nota: As recomendações são baseadas no ajuste linear do modelo, utilize sempre em conjunto com análise técnica/financeira."
)

# Gráfico observados vs. preditos
fig2, ax2 = plt.subplots(figsize=(6,4))
ax2.scatter(y_test, y_pred, alpha=0.7)
ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
ax2.set_xlabel("Valores Observados")
ax2.set_ylabel("Valores Preditos")
ax2.set_title("Valores Observados vs. Preditos")
st.pyplot(fig2)
