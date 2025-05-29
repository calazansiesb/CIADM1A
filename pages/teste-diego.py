import pandas as pd

# Carregar os dados
df = pd.read_csv("seus_dados.csv")  # Substitua pelo seu conjunto de dados

# Calcular a matriz de correlação
matriz_correlacao = df.corr(method='pearson')  # Pode usar 'spearman' ou 'kendall' dependendo do caso

# Exibir a matriz
print(matriz_correlacao)
