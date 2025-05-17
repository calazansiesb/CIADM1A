import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 1. Carregue seus dados (certifique-se de que GALINACEOS.csv está no mesmo diretório)
df = pd.read_csv('GALINACEOS.csv')

# 2. Defina a variável alvo (produção de ovos em dúzias)
y = df['Q_DZ_PROD']

# 3. Selecione variáveis preditoras relevantes (adapte conforme necessário)
features = [
    'GAL_TOTAL', 'GAL_VEND', 'A_TOTAL', 'N_TRAB_TOTAL', 'SIST_CRIA',
    'NIV_TERR', 'E_COMERC', 'E_AGRIFAM'
]
X = df[features]

# 4. Transforme variáveis categóricas em dummies
X = pd.get_dummies(X, drop_first=True)

# 5. Divida em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Treine o modelo Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Faça previsões
y_pred = model.predict(X_test)

# 8. Avalie o modelo
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)
print(f"RMSE: {rmse:.2f}")
print(f"R2: {r2:.3f}")

# 9. Veja a importância das variáveis
importances = pd.Series(model.feature_importances_, index=X.columns)
print("Importância das variáveis:")
print(importances.sort_values(ascending=False))
