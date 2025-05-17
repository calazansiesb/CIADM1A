import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Fatores que Mais Impactam a Lucratividade da Granja")

# Dados obtidos (top 6, mas pode ser até 10)
coefs = {
    "Tecnologia": 0.9,
    "Terra": -0.8,
    "Mão de Obra": 0.5,
    "Marketing": -0.3,
    "Capital": 0.2,
    "Insumos": -0.1,
}
coef_df = pd.DataFrame(list(coefs.items()), columns=["Fator", "Coeficiente"])
coef_df = coef_df.sort_values("Coeficiente", key=abs, ascending=True)

# Gráfico
st.subheader("Importância dos Fatores para a Lucratividade")
fig, ax = plt.subplots(figsize=(7, 4))
colors = coef_df["Coeficiente"].apply(lambda x: "#4caf50" if x > 0 else "#e57373")
ax.barh(coef_df["Fator"], coef_df["Coeficiente"], color=colors)
ax.set_xlabel("Coeficiente (Peso no Modelo)")
ax.set_ylabel("Fator")
ax.set_title("Top Fatores Impactando a Lucratividade")
st.pyplot(fig)

# Tabela
st.write("**Tabela dos Fatores e seus Coeficientes:**")
st.dataframe(coef_df[::-1], use_container_width=True)

# Análise automática
st.markdown("---")
st.markdown(
    f"O fator de **maior impacto positivo** é '**Tecnologia**' com um coeficiente de **0.900**. "
    "Isso indica que **aumentar este fator tende a aumentar a lucratividade**."
)
st.markdown(
    f"O fator de **maior impacto negativo** é '**Terra**' com um coeficiente de **-0.800**. "
    "Isso indica que **aumentar este fator tende a diminuir a lucratividade**."
)
