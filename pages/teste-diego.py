import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# Configuração da página
st.set_page_config(layout="wide", page_title="Análise de Galináceos", icon="🐓")

st.title("Dashboard de Análise de Galináceos")

# Upload de arquivo
uploaded_file = st.file_uploader("Faça upload do arquivo CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Pré-visualização dos Dados")
    st.dataframe(df.head())

    # Mostrar estatísticas descritivas
    st.subheader("Estatísticas Descritivas")
    st.write(df.describe())

    # Gráfico de dispersão interativo
    st.subheader("Gráfico de Dispersão")
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    if len(numeric_columns) >= 2:
        x_axis = st.selectbox("Eixo X", numeric_columns, index=0)
        y_axis = st.selectbox("Eixo Y", numeric_columns, index=1)
        fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)

    # Correlação
    st.subheader("Matriz de Correlação")
    corr = df.corr(numeric_only=True)
    fig_corr, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig_corr)

    # Regressão linear simples (opcional)
    st.subheader("Regressão Linear")
    if len(numeric_columns) >= 2:
        x_col = st.selectbox("Variável Independente (X)", numeric_columns, key="reg_x")
        y_col = st.selectbox("Variável Dependente (Y)", numeric_columns, key="reg_y")

        X = df[[x_col]].dropna()
        Y = df[y_col].dropna()
        X, Y = X.align(Y, join='inner', axis=0)

        if len(X) > 0:
            model = LinearRegression()
            model.fit(X, Y)
            Y_pred = model.predict(X)

            fig_lr, ax_lr = plt.subplots()
            ax_lr.scatter(X, Y, label="Dados reais")
            ax_lr.plot(X, Y_pred, color="red", label="Regressão linear")
            ax_lr.set_xlabel(x_col)
            ax_lr.set_ylabel(y_col)
            ax_lr.legend()
            st.pyplot(fig_lr)

            st.markdown(f"**Coeficiente Angular (Slope):** {model.coef_[0]:.4f}")
            st.markdown(f"**Intercepto:** {model.intercept_:.4f}")
        else:
            st.warning("Não há dados suficientes para regressão.")

else:
    st.info("Por favor, envie um arquivo CSV para iniciar a análise.")
