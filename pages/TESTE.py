import streamlit as st
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import requests
import io

# URL do GitHub (substitua pelo seu link direto para CSV)
github_url = 'https://raw.githubusercontent.com/seu_usuario/seu_repositorio/main/dados.csv'

# Carregar os dados do GitHub
@st.cache_data
def load_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text), delimiter=';')
        return df
    else:
        st.error("Erro ao carregar dados do GitHub.")
        return None

df = load_data(github_url)

if df is not None:
    st.title("Predição de Aves por Redes Neurais")

    # Selecionar variáveis
    X = df[['GAL_TOTAL']]  # Número de granjas
    y = df[['GAL_GALOS', 'GAL_POED', 'GAL_MATR']].sum(axis=1)  # Soma total de aves

    # Normalização dos dados
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))

    # Dividir dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

    # Criar modelo de rede neural
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    # Treinar modelo
    model.fit(X_train, y_train, epochs=100, verbose=0)

    # Fazer predição
    predicao = model.predict(X_test)

    # Exibir resultados no Streamlit
    st.write(f"🔎 Predições de Aves: {predicao.flatten()[:5]}")
    st.write(f"📊 Erro médio quadrático: {model.evaluate(X_test, y_test, verbose=0)}")
    
    # Adicionar interatividade
    granjas = st.slider("Número de Granjas", int(X.min()), int(X.max()), int(X.mean()))
    granjas_scaled = scaler.transform([[granjas]])
    aves_preditas = model.predict(granjas_scaled)[0][0]

    st.write(f"🐔 Para {granjas} granjas, o modelo prevê aproximadamente {int(scaler.inverse_transform([[aves_preditas]])[0][0])} aves.")

else:
    st.error("Não foi possível carregar os dados.")
