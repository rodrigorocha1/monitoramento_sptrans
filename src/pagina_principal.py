import streamlit as st
from database.carregar_dados_agrupados import consultar_dados
st.set_page_config(
    page_title='Monitoramento sptrans'
)


with st.sidebar:
    st.write('SideBarr')
st.write('Bem vindo')

with st.container():
    st.write('2 Tabelas')
    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.header('Tabela 1')
        option = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno1'
        )
        st.write('Selecionou', option)
        with st.spinner('Aguarde'):
            @st.cache_data
            def cached_load_table1(option):
                df_table1, _ = consultar_dados(
                    data_consulta='2023-09-15',
                    coluna_agrupamento=['CODIGO_AREA'],
                    ordenacao=['CODIGO_AREA']
                )
                return df_table1

        df_tabela1 = cached_load_table1(option)
        st.dataframe(df_tabela1)

    with col2:

        st.header('Tabela 2')
        option2 = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno2'
        )
        with st.spinner('Aguarde'):
            @st.cache_data
            def cached_load_table2(option):
                df_tabela2, _ = consultar_dados(
                    data_consulta='2023-09-15',
                    coluna_agrupamento=['EMPRESA'],
                    ordenacao=['EMPRESA']

                )
                return df_tabela2

            df_tabela2 = cached_load_table2(option)
            st.dataframe(df_tabela2)


with st.container():
    st.write('Outras tabelas')

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.header('Tabela 3')
        option3 = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno3'
        )
        with st.spinner('Aguarde'):
            @st.cache_data
            def cached_load_table3(option):
                df_tabela3, _ = consultar_dados(
                    data_consulta='2023-09-15',
                    coluna_agrupamento=['TURNO', 'EMPRESA'],
                    ordenacao=['TURNO']
                )
                return df_tabela3
            df_tabela3 = cached_load_table3(option)
            st.dataframe(df_tabela3)

    with col2:
        st.header('Tabela 4')
        option4 = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno4'
        )
        with st.spinner('Aguarde'):
            @st.cache_data
            def cached_load_table4(option):
                df_tabela4, _ = consultar_dados(
                    data_consulta='2023-09-15',
                    coluna_agrupamento=[
                        'LETREIRO_COMPLETO',
                        'LETREIRO_ORIGEM',
                        'LETREIRO_DESTINO'
                    ],
                    ordenacao=['LETREIRO_COMPLETO']
                )
                return df_tabela4
            df_tabela4 = cached_load_table4(option)
            st.dataframe(df_tabela4)
