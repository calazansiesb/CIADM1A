import pandas as pd
import matplotlib.pyplot as plt

def gerar_grafico_pizza_matrizes(df):
    """
    Gera um gráfico de pizza da distribuição do total de matrizes por unidade territorial,
    considerando apenas as regiões do país.
    Args:
        df (pd.DataFrame): DataFrame contendo os dados.
    """
    regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']

    # Filtrar apenas linhas das regiões
    df_regioes = df[df['NOM_TERR'].isin(regioes)].copy()

    print("\n--- Geração de Gráfico de Pizza: Distribuição de Matrizes por Região ---")

    # 1. Agrupar os dados por 'NOM_TERR' e somar o total de 'GAL_MATR'
    total_matrizes_por_regiao = df_regioes.groupby('NOM_TERR')['GAL_MATR'].sum().reset_index()

    print("\nDados Agrupados:\n", total_matrizes_por_regiao)

    # 2. Calcular a proporção de matrizes para cada região
    total_matrizes = total_matrizes_por_regiao['GAL_MATR'].sum()
    total_matrizes_por_regiao['Proporcao'] = total_matrizes_por_regiao['GAL_MATR'] / total_matrizes

    # 3. Criar o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(
        total_matrizes_por_regiao['Proporcao'],
        labels=total_matrizes_por_regiao['NOM_TERR'],
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    plt.title('Distribuição de Matrizes por Região')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Exemplo de DataFrame
    data = {
        'NOM_TERR': ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste', 'Brasil', 'SP', 'MG'],
        'GAL_MATR': [1000, 1500, 1200, 800, 900, 5500, 300, 200]
    }
    df = pd.DataFrame(data)

    gerar_grafico_pizza_matrizes(df)
