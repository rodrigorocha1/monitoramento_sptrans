import streamlit as st
from database.carregar_dados_agrupados import consultar_dados

st.set_page_config(
    page_title='Monitoramento sptrans'
)


df = consultar_dados('2023-09-15', 'DATA_EXTRACAO')


options = st.multiselect(
    'cor',
    df.columns

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
            ('Manhã', 'Tarde', 'Noite')
        )
        st.write('Selecionou', option)
        st.dataframe(df)

    with col2:

        st.header('Tabela 2')
        st.dataframe(df)


with st.container():
    st.write('Outras tabelas')

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.header('Tabela 3')
        st.dataframe(df)

    with col2:
        st.header('Tabela 4')
        st.dataframe(df)
