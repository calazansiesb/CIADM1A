import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # Importar para controle mais fino se necessário

# Configuração da página
st.set_page_config(
    page_title="Impacto na Lucratividade",
    page_icon="📊",
    layout="centered", # Usar layout centered para este tipo de dashboard
)

# Título principal
st.title("💰 Fatores que Mais Impactam a Lucratividade da Granja")

# Dados dos coeficientes
coefs = {
    "Tecnologia": 0.9,
    "Terra": -0.8,
    "Mão de Obra": 0.5,
    "Marketing": -0.3,
    "Capital": 0.2,
    "Insumos": -0.1,
}

# Preparação dos dados
coef_df = pd.DataFrame(list(coefs.items()), columns=["Fator", "Coeficiente"])
coef_df["Categoria"] = coef_df["Coeficiente"].apply(lambda x: "Positivo" if x > 0 else "Negativo")
# Criar uma coluna para a magnitude absoluta para escala de cor
coef_df["Magnitude"] = coef_df["Coeficiente"].abs()
coef_df = coef_df.sort_values("Coeficiente", key=abs, ascending=True)

# Gráfico de barras elegante (não 3D literal, mas com profundidade visual)
st.subheader("📈 Importância dos Fatores para a Lucratividade")

# Definir escalas de cores personalizadas e mais vivas
# Para positivo, um gradiente verde-claro a verde-escuro
positive_colors = ['#C8E6C9', '#4CAF50', '#2E7D32'] # Light green to dark green
# Para negativo, um gradiente vermelho-claro a vermelho-escuro
negative_colors = ['#FFCDD2', '#F44336', '#B71C1C'] # Light red to dark red


# Usar a Magnitude para a intensidade da cor
fig = px.bar(
    coef_df,
    x="Coeficiente",
    y="Fator",
    color="Coeficiente", # Colorir pelo coeficiente para um gradiente
    color_continuous_scale=[(0, 'red'), (0.5, 'white'), (1, 'green')], # Escala de cor que transiciona de vermelho para verde
    # Ou usar uma escala baseada na categoria para ter dois gradientes distintos:
    # color_continuous_scale=px.colors.sequential.RdYlGn, # Um gradiente que vai de vermelho a verde
    # color_continuous_scale=px.colors.diverging.RdYlGn, # Outra opção divergente
    
    orientation='h',
    text_auto=True,
    labels={"Coeficiente": "Impacto no Modelo", "Fator": ""},
    height=450, # Aumentar um pouco a altura para melhor visualização
    template="plotly_white" # Um tema mais limpo
)

# Se quiser escalas de cores separadas por categoria (Positivo/Negativo)
# Isso requer um pouco mais de manipulação com go.Bar, ou criar dois traces
# Para simplificar e manter a elegância com px.bar: usar uma escala contínua divergente
# Ou usar o 'color' pelo Coeficiente e ajustar range_color

# Ajustar o range de cor para que o "branco" ou neutro fique no 0
# A escala de cor irá de min(Coeficiente) a max(Coeficiente)
min_val = coef_df["Coeficiente"].min()
max_val = coef_df["Coeficiente"].max()
# Ajustar range_color para que o ponto central (0) fique no meio do gradiente
fig.update_layout(coloraxis_colorbar=dict(title="Impacto"))
fig.update_traces(marker_line_color='darkgray', marker_line_width=1) # Adiciona borda nas barras


# Layout elegante
fig.update_layout(
    hovermode="y unified",
    showlegend=False,
    yaxis={'categoryorder':'total ascending'},
    margin=dict(l=0, r=0, t=50, b=0), # Ajustar margens
    title_x=0.5, # Centralizar título
    plot_bgcolor='rgba(0,0,0,0)', # Fundo transparente
    paper_bgcolor='rgba(0,0,0,0)', # Fundo do papel transparente
    xaxis=dict(showgrid=True, gridcolor='lightgray'), # Mostrar grid no eixo X
    yaxis=dict(showgrid=False) # Remover grid no eixo Y
)

# Destaques no gráfico (manter, são úteis)
fig.add_annotation(
    x=0.85, y="Tecnologia",
    text="Maior impacto positivo",
    showarrow=True,
    arrowhead=1,
    ax=50,
    ay=0,
    font=dict(color="darkgreen", size=12),
    bgcolor="rgba(255,255,255,0.7)"
)

fig.add_annotation(
    x=-0.75, y="Terra",
    text="Maior impacto negativo",
    showarrow=True,
    arrowhead=1,
    ax=-50,
    ay=0,
    font=dict(color="darkred", size=12),
    bgcolor="rgba(255,255,255,0.7)"
)

st.plotly_chart(fig, use_container_width=True)

# Tabela de dados
st.subheader("📋 Detalhes dos Coeficientes")
st.dataframe(
    coef_df.sort_values("Coeficiente", ascending=False),
    column_config={
        "Fator": "Fator Analisado",
        "Coeficiente": st.column_config.NumberColumn(
            "Impacto",
            format="%.2f",
            help="Coeficiente padronizado do modelo"
        ),
        "Categoria": "Tipo de Impacto"
    },
    hide_index=True,
    use_container_width=True
)

# Análise automática
st.markdown("---")
st.subheader("🔎 Principais Insights")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Fator Mais Positivo",
        value="Tecnologia",
        delta="Coef: +0.90"
    )
    st.markdown("""
    **Recomendações:**
    - Investir em automação
    - Adotar sistemas de monitoramento
    - Implementar tecnologias de precisão
    """)

with col2:
    st.metric(
        label="Fator Mais Negativo",
        value="Terra",
        delta="Coef: -0.80"
    )
    st.markdown("""
    **Recomendações:**
    - Otimizar uso do espaço
    - Considerar sistemas verticais
    - Reduzir expansões desnecessárias
    """)

# Rodapé
st.markdown("---")
st.caption("Análise desenvolvida com base em modelo de regressão linear multivariada | Dados simulados")
