import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Variação Temporal da Produção Avícola")

def analisar_variacao_temporal(df):
    """
    Analisa e exibe gráficos da variação temporal da produção avícola.
    Args:
        df (pd.DataFrame): DataFrame com os dados.
    """

    st.header("Análise da Variação Temporal da Produção Avícola")

    # Verificar se a coluna 'ANO' existe
    if 'ANO' not in df.columns:
        st.error("Erro: A coluna 'ANO' não está presente no DataFrame.")
        return

    anos = df['ANO'].unique()
    st.write(f"Anos disponíveis: {anos}")

    # Preparar os Dados para Análise Temporal
    dados_por_ano = {}
    for ano in anos:
        df_ano = df[df['ANO'] == ano]
        total_estabelecimentos = df_ano['E_TEM_GAL'].sum() if 'E_TEM_GAL' in df_ano.columns else 0
        total_aves = df_ano['GAL_TOTAL'].sum() if 'GAL_TOTAL' in df_ano.columns else 0
        proporcoes_sist_cria = df_ano['SIST_CRIA'].value_counts(normalize=True) * 100 if 'SIST_CRIA' in df_ano.columns else pd.Series()

        dados_por_ano[ano] = {
            'Total Estabelecimentos': total_estabelecimentos,
            'Total Aves': total_aves,
            'Proporcoes SIST_CRIA': proporcoes_sist_cria
        }

    # Criar um DataFrame para facilitar a visualização
    df_temporal = pd.DataFrame(dados_por_ano).T
    df_temporal['ANO'] = df_temporal.index
    df_temporal = df_temporal.reset_index(drop=True)
    df_temporal[['Total Aves', 'Total Estabelecimentos']] = df_temporal[['Total Aves', 'Total Estabelecimentos']].apply(pd.to_numeric)

    st.subheader("Dados Agregados por Ano")
    st.dataframe(df_temporal[['ANO', 'Total Estabelecimentos', 'Total Aves']])

    # Gráfico de linha para Total de Estabelecimentos
    st.subheader("Evolução do Número de Estabelecimentos ao Longo do Tempo")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='ANO', y='Total Estabelecimentos', data=df_temporal, marker='o', ax=ax1)
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Total de Estabelecimentos')
    ax1.set_title('Evolução do Número de Estabelecimentos ao Longo do Tempo')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # Gráfico de linha para Total de Aves
    st.subheader("Evolução do Número de Aves ao Longo do Tempo")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='ANO', y='Total Aves', data=df_temporal, marker='o', ax=ax2)
    ax2.set_xlabel('Ano')
    ax2.set_ylabel('Total de Aves')
    ax2.set_title('Evolução do Número de Aves ao Longo do Tempo')
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Visualizar a Variação Temporal dos Tipos de Exploração
    st.subheader("Proporção dos Tipos de Exploração ao Longo do Tempo")
    if 'SIST_CRIA' in df.columns:
        df_sist_cria = df.groupby(['ANO', 'SIST_CRIA']).size().unstack(fill_value=0)
        df_sist_cria_prop = df_sist_cria.div(df_sist_cria.sum(axis=1), axis=0) * 100

        fig3, ax3 = plt.subplots(figsize=(12, 6))
        df_sist_cria_prop.plot(kind='bar', stacked=True, ax=ax3)
        ax3.set_title('Proporção dos Tipos de Exploração ao Longo do Tempo')
        ax3.set_xlabel('Ano')
        ax3.set_ylabel('Proporção (%)')
        plt.xticks(rotation=45)
        ax3.legend(title='Tipo de Exploração', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig3)
    else:
        st.warning("Coluna 'SIST_CRIA' não encontrada para análise de tipos de exploração.")

# Exemplo de uso: 
# No seu app principal, importe pagina2 e chame analisar_variacao_temporal(df) passando o DataFrame real.

if __name__ == '__main__':
    # Exemplo de DataFrame para teste local
    data = {'ANO': [2010, 2010, 2010, 2015, 2015, 2015, 2020, 2020, 2020, 2010, 2015, 2020],
            'E_TEM_GAL': [1000, 1200, 1100, 1500, 1600, 1400, 1800, 2000, 1900, 1300, 1700, 2100],
            'GAL_TOTAL': [100000, 110000, 105000, 140000, 150000, 130000, 180000, 210000, 200000, 120000, 160000, 190000],
            'SIST_CRIA': ['Ovos para Consumo', 'Frangos de Corte', 'Outros', 'Ovos para Consumo',
                          'Frangos de Corte', 'Outros', 'Ovos para Consumo', 'Frangos de Corte', 'Outros',
                          'Ovos para Incubação', 'Ovos para Incubação', 'Ovos para Incubação']}
    df = pd.DataFrame(data)
    analisar_variacao_temporal(df)
