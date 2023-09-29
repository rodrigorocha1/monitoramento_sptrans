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
        df_tabela1, _ = consultar_dados(
            data_consulta='2023-09-15',
            coluna_agrupamento=['CODIGO_AREA'],
            ordenacao=['CODIGO_AREA']
        )
        st.dataframe(df_tabela1)

    with col2:

        st.header('Tabela 2')
        option2 = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno2'
        )
        df_tabela2, _ = consultar_dados(
            data_consulta='2023-09-15',
            coluna_agrupamento=['EMPRESA'],
            ordenacao=['EMPRESA']

        )
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
        df_tabela3, _ = consultar_dados(
            data_consulta='2023-09-15',
            coluna_agrupamento=['TURNO', 'EMPRESA'],
            ordenacao=['TURNO']
        )
        st.dataframe(df_tabela3)

    with col2:
        st.header('Tabela 4')
        option4 = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno4'
        )
        df_tabela4, _ = consultar_dados(
            data_consulta='2023-09-15',
            coluna_agrupamento=[
                'LETREIRO_COMPLETO',
                'LETREIRO_ORIGEM',
                'LETREIRO_DESTINO'
            ],
            ordenacao=['LETREIRO_COMPLETO']
        )
        st.dataframe(df_tabela4)
