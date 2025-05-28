import streamlit as st
import pandas as pd
import plotly.express as px

# Simulação do DataFrame 'df' (substitua pelo seu carregamento de dados real)
# Certifique-se de que seu DataFrame real tenha uma coluna 'NOM_TERR'
# Adicione mais dados e variação para ver o efeito no gráfico
data = {
    'NOM_TERR': [
        'São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Bahia', 'Paraná',
        'Rio Grande do Sul', 'Santa Catarina', 'Pernambuco', 'Ceará', 'Goiás',
        'Distrito Federal', 'Amazonas', 'Pará', 'Maranhão', 'Espírito Santo',
        'Mato Grosso', 'Mato Grosso do Sul', 'Rondônia', 'Tocantins', 'Acre',
        'Amapá', 'Roraima', 'Paraíba', 'Alagoas', 'Sergipe',
        'Rio Grande do Norte', 'Piauí', 'São Paulo', 'Minas Gerais', 'Bahia',
        'São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Pará', 'Pará',
        'Amazonas', 'Amazonas', 'Tocantins', 'Acre', 'Rondônia', 'Rondônia',
        'Pará', 'Amazonas', 'São Paulo', 'Minas Gerais', 'Ceará', 'Bahia',
        'Rio de Janeiro', 'São Paulo', 'Distrito Federal', 'Amapá', 'Roraima',
        'Rio Grande do Sul', 'Santa Catarina', 'Pernambuco', 'Ceará', 'Goiás',
        'Mato Grosso', 'Mato Grosso do Sul', 'Rondônia', 'Tocantins', 'Acre',
        'Amapá', 'Roraima', 'Paraíba', 'Alagoas', 'Sergipe',
        'Rio Grande do Norte', 'Piauí', 'São Paulo', 'Minas Gerais', 'Bahia'
    ]
}
df = pd.DataFrame(data)

st.header('🌎 Distribuição por Unidade Federativa')

if 'NOM_TERR' in df.columns:
    # Lista oficial dos 26 estados + DF
    estados_brasil = [
        'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás',
        'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco',
        'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina',
        'São Paulo', 'Sergipe', 'Tocantins'
    ]

    # Mapeamento de estados para regiões
    regioes_estados = {
        'Norte': ['Acre', 'Amapá', 'Amazonas', 'Pará', 'Rondônia', 'Roraima', 'Tocantins'],
        'Nordeste': ['Alagoas', 'Bahia', 'Ceará', 'Maranhão', 'Paraíba', 'Pernambuco', 'Piauí', 'Rio Grande do Norte', 'Sergipe'],
        'Centro-Oeste': ['Distrito Federal', 'Goiás', 'Mato Grosso', 'Mato Grosso do Sul'],
        'Sudeste': ['Espírito Santo', 'Minas Gerais', 'Rio de Janeiro', 'São Paulo'],
        'Sul': ['Paraná', 'Rio Grande do Sul', 'Santa Catarina']
    }

    # Inverter o dicionário para mapear estado -> região
    estado_para_regiao = {estado: regiao for regiao, estados in regioes_estados.items() for estado in estados}

    # Adicionar 'Região' ao DataFrame principal para uso posterior, se necessário
    df['Regiao'] = df['NOM_TERR'].map(estado_para_regiao)

    # Filtrar apenas estados do Brasil
    df_uf = df[df['NOM_TERR'].isin(estados_brasil)].copy() # Use .copy() para evitar SettingWithCopyWarning

    # Calcular a frequência de estabelecimentos por UF (para o Brasil inteiro)
    # df_plot_total será usado para os gráficos dos 3 maiores/menores/meio
    freq_estab_por_uf_total = df_uf['NOM_TERR'].value_counts().sort_values(ascending=False)
    df_plot_total = freq_estab_por_uf_total.rename_axis('Unidade Federativa').reset_index(name='Quantidade')


    # === Seletor de Região para o Gráfico Dinâmico ===
    st.subheader('Selecione a Região para Exibir no Gráfico:')
    regioes_disponiveis = ['Todas as Regiões'] + list(regioes_estados.keys())
    selected_region = st.selectbox('Escolha uma região', regioes_disponiveis)

    # Filtragem e cálculo da frequência com base na seleção
    df_filtered_by_region = df_uf.copy() # Começa com todos os estados do Brasil

    title_sufix = ''
    if selected_region != 'Todas as Regiões':
        estados_da_regiao = regioes_estados[selected_region]
        df_filtered_by_region = df_filtered_by_region[df_filtered_by_region['NOM_TERR'].isin(estados_da_regiao)]
        title_sufix = f' na Região {selected_region}'

    # Calcular a frequência APENAS para os estados filtrados
    if not df_filtered_by_region.empty:
        freq_estab_por_uf_filtered = df_filtered_by_region['NOM_TERR'].value_counts().sort_values(ascending=False)
        df_plot_filtered = freq_estab_por_uf_filtered.rename_axis('Unidade Federativa').reset_index(name='Quantidade')
    else:
        df_plot_filtered = pd.DataFrame(columns=['Unidade Federativa', 'Quantidade']) # DataFrame vazio se não houver dados


    # === Gráfico Dinâmico de Distribuição por UF ===
    st.subheader(f'Número de Estabelecimentos por Estado{title_sufix}')
    if not df_plot_filtered.empty:
        fig2 = px.bar(
            df_plot_filtered,
            x='Unidade Federativa',
            y='Quantidade',
            title=f'Distribuição por Unidade Federativa{title_sufix}',
            labels={'Unidade Federativa': 'Estado', 'Quantidade': 'Quantidade'},
            color='Unidade Federativa',  # Cor única para cada estado!
            color_discrete_sequence=px.colors.qualitative.Set2  # Paleta amigável
        )
        fig2.update_layout(
            xaxis_tickangle=-35,
            showlegend=False,
            bargap=0.15,
            plot_bgcolor='white',
            font=dict(size=14)
        )
        # Adicionar o valor exato no topo de cada barra
        fig2.update_traces(texttemplate='%{y}', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info(f"Não há dados para a região '{selected_region}' com os estados filtrados.")

    st.markdown('---')

    # Restante do código para os gráficos dos 3 maiores, 3 do meio e 3 menores (sem alterações)
    st.header('Análise Detalhada dos Estabelecimentos por Estado (Brasil)')

    # Garantir que temos dados suficientes para essas análises
    if len(df_plot_total) >= 3:
        # Top 3 Maiores
        top_3 = df_plot_total.head(3)
        fig_top_3 = px.bar(
            top_3,
            x='Unidade Federativa',
            y='Quantidade',
            title='Top 3 Maiores Estados em Número de Estabelecimentos',
            labels={'Unidade Federativa': 'Estado', 'Quantidade': 'Quantidade'},
            color='Unidade Federativa',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
        fig_top_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
        fig_top_3.update_traces(texttemplate='%{y}', textposition='outside') # Adiciona o valor
        st.plotly_chart(fig_top_3, use_container_width=True)

        # 3 do Meio
        if len(df_plot_total) >= 6: # Precisamos de pelo menos 6 estados para ter 3 do meio razoavelmente definidos
            middle_start = len(df_plot_total) // 2 - 1 # Ajuste para pegar 3 do meio
            if middle_start < 0: middle_start = 0 # Garante que não seja negativo
            middle_3 = df_plot_total.iloc[middle_start : middle_start + 3]

            fig_middle_3 = px.bar(
                middle_3,
                x='Unidade Federativa',
                y='Quantidade',
                title='3 Estados do Meio em Número de Estabelecimentos',
                labels={'Unidade Federativa': 'Estado', 'Quantidade': 'Quantidade'},
                color='Unidade Federativa',
                color_discrete_sequence=px.colors.qualitative.D3
            )
            fig_middle_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
            fig_middle_3.update_traces(texttemplate='%{y}', textposition='outside') # Adiciona o valor
            st.plotly_chart(fig_middle_3, use_container_width=True)
        else:
            st.info("Não há estados suficientes para exibir os '3 do meio'. São necessários pelo menos 6 estados.")


        # 3 Menores
        bottom_3 = df_plot_total.tail(3)
        fig_bottom_3 = px.bar(
            bottom_3,
            x='Unidade Federativa',
            y='Quantidade',
            title='Top 3 Menores Estados em Número de Estabelecimentos',
            labels={'Unidade Federativa': 'Estado', 'Quantidade': 'Quantidade'},
            color='Unidade Federativa',
            color_discrete_sequence=px.colors.qualitative.G10
        )
        fig_bottom_3.update_layout(xaxis_tickangle=-35, showlegend=False, plot_bgcolor='white', font=dict(size=14))
        fig_bottom_3.update_traces(texttemplate='%{y}', textposition='outside') # Adiciona o valor
        st.plotly_chart(fig_bottom_3, use_container_width=True)

    else:
        st.warning("Não há dados suficientes para gerar os gráficos dos 3 maiores, 3 do meio e 3 menores estados.")
