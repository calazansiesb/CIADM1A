import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Exemplo: supondo que você já tenha um DataFrame df
# Alvo (target)
y = df['Q_DZ_PROD']

# Selecione features relevantes (adapte conforme seu contexto)
X = df[['GAL_TOTAL', 'GAL_VEND', 'A_TOTAL', 'N_TRAB_TOTAL', 'SIST_CRIA', 'NIV_TERR', 'E_COMERC', 'E_AGRIFAM']]

# Tratamento de variáveis categóricas
X = pd.get_dummies(X, drop_first=True)

# Split treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliação
y_pred = model.predict(X_test)
print("RMSE:", mean_squared_error(y_test, y_pred, squared=False))
print("R2:", r2_score(y_test, y_pred))

# Importância das variáveis
importances = pd.Series(model.feature_importances_, index=X.columns)
print(importances.sort_values(ascending=False))
