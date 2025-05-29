import streamlit as st
import pandas as pd
import plotly.express as px # Adicione esta importação se ainda não tiver

# =============================================
# Carregar os dados
# =============================================
# Função para carregar os dados do CSV
@st.cache_data # Usar cache para otimizar o carregamento do DataFrame
def load_data(file_path):
    try:
        # AQUI ESTÁ A PARTE CRUCIAL: carregando o CSV e especificando o separador
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')

        # Limpeza e conversão de colunas que podem ser úteis para outros gráficos
        if 'NOM_TERR' in df.columns:
            df['NOM_TERR'] = df['NOM_TERR'].astype(str).str.strip().str.title()

        numeric_cols = ['GAL_MATR', 'GAL_TOTAL', 'N_TRAB_TOTAL'] # Exemplo de colunas numéricas
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                #st.warning(f"Coluna '{col}' não encontrada durante o pré-processamento.")
                df[col] = 0 # Define como 0 para evitar erros se a coluna não existir

        # Mapeamento de SIST_CRIA (se existir e for necessário)
        if 'SIST_CRIA' in df.columns:
            df['SIST_CRIA'] = df['SIST_CRIA'].astype(str).str.strip()
            mapeamento_sistemas = {
                '1-SIST_POC': 'Produtores de ovos para consumo',
                '2-SIST_POI': 'Produtores de ovos para incubação',
                '3-SIST_PFC': 'Produtores de frangos de corte',
                '4-Outro': 'Outros produtores'
            }
            df['SIST_CRIA'] = df['SIST_CRIA'].replace(mapeamento_sistemas)
        return df
    except FileNotFoundError:
        st.error("Erro: Arquivo 'GALINACEOS.csv' não encontrado. Por favor, certifique-se de que o arquivo está no mesmo diretório da aplicação.")
        st.stop() # Interrompe a execução do script
    except Exception as e:
        st.error(f"Erro ao carregar ou processar o arquivo CSV: {e}. Verifique o formato do arquivo e o separador.")
        st.stop() # Interrompe a execução do script

# Chama a função para carregar o DataFrame
df = load_data("GALINACEOS.csv")

# =============================================
# 5. Distribuição por Porte dos Estabelecimentos
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

# O restante do seu código para o gráfico de porte
if not df.empty and 'NOM_CL_GAL' in df.columns:
    freq_portes = df['NOM_CL_GAL'].value_counts().sort_index()
    fig4 = px.bar(
        x=freq_portes.index,
        y=freq_portes.values,
        title='Distribuição de Estabelecimentos por Porte (Faixas IBGE)',
        labels={'x': 'Porte do Estabelecimento', 'y': 'Quantidade'},
        color_discrete_sequence=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
    )
    st.plotly_chart(fig4, use_container_width=True)

    with st.expander("💡 Interpretação do Gráfico de Distribuição por Porte dos Estabelecimentos"):
        st.info("""
        **🏭 Análise da Distribuição por Porte dos Estabelecimentos**

        O gráfico mostra a quantidade de estabelecimentos distribuídos por diferentes faixas de porte (definidas pelo IBGE):

        - As faixas intermediárias, especialmente entre **201 e 5.000 aves**, concentram os maiores números de estabelecimentos, sugerindo predominância de produtores de médio porte no setor.
        - Pequenos produtores ("De 1 a 100" e "De 101 a 200") também são numerosos, mas em menor quantidade que as faixas intermediárias.
        - Faixas extremas ("De 100.001 e mais" e "Sem galináceos em 30.09.2017") apresentam participação reduzida, indicando que grandes produtores e estabelecimentos temporariamente inativos são minoria.
        - A categoria "Total" pode representar registros agregados ou casos não classificados nas demais faixas, devendo ser analisada com cautela.
        - A presença de estabelecimentos "Sem galináceos" reforça a importância de considerar sazonalidade ou inatividade temporária.

        **Conclusão:**
        - O perfil da produção avícola brasileira é fortemente marcado pela presença de estabelecimentos de porte intermediário, com pequena participação de grandes produtores e um contingente relevante de pequenos estabelecimentos. Isso tem implicações para políticas públicas, estratégias de mercado e apoio ao setor.
        """)
else:
    st.warning("A coluna 'NOM_CL_GAL' não foi encontrada no dataset ou o dataset está vazio. Verifique o arquivo CSV.")
