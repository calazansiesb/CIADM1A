import pandas as pd
import streamlit as st # Se você estiver usando no Streamlit

# =============================================
# 5. Distribuição por Porte dos Estabelecimentos
# =============================================
st.header('🏭 Distribuição por Porte dos Estabelecimentos')

if 'NOM_CL_GAL' in df.columns:
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
    st.warning("A coluna 'NOM_CL_GAL' não foi encontrada no dataset.")
