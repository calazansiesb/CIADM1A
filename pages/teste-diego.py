import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# Configuração da página


st.title("Dashboard de Análise de Galináceos")

# Upload de arquivo
uploaded_file = st.file_uploader("📤 Faça upload do arquivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
    else:
        st.subheader("📄 Pré-visualização dos Dados")
        st.dataframe(df.head())

        # Estatísticas descritivas
        st.subheader("📊 Estatísticas Descritivas")
        st.write(df.describe())

        # Colunas numéricas
        numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

        # Gráfico de dispersão
        if len(numeric_columns) >= 2:
            st.subheader("📈 Gráfico de Dispersão")
            x_axis = st.selectbox("Eixo X", numeric_columns, index=0)
            y_axis = st.selectbox("Eixo Y", numeric_columns, index=1)
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            st.plotly_chart(fig, use_container_width=True)

        # Matriz de correlação
        if len(numeric_columns) >= 2:
            st.subheader("🔗 Matriz de Correlação")
            corr = df[numeric_columns].corr()
            fig_corr, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig_corr)

        # Regressão linear
        if len(numeric_columns) >= 2:
            st.subheader("📉 Regressão Linear")
            x_col = st.selectbox("Variável Independente (X)", numeric_columns, key="reg_x")
            y_col = st.selectbox("Variável Dependente (Y)", numeric_columns, key="reg_y")

            # Alinhar X e Y com dados válidos
            data = df[[x_col, y_col]].dropna()
            if not data.empty:
                X = data[[x_col]]
                Y = data[y_col]

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

                st.markdown(f"**Coeficiente Angular (Slope):** `{model.coef_[0]:.4f}`")
                st.markdown(f"**Intercepto:** `{model.intercept_:.4f}`")
            else:
                st.warning("❗ Não há dados suficientes para regressão linear.")
        else:
            st.warning("❗ Dados insuficientes para regressão.")

else:
    st.info("👈 Envie um arquivo CSV para iniciar a análise.")
