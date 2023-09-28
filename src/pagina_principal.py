import streamlit as st


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
        option = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite')
        )
        st.write('Selecionou', option)
        st.header('Tabela 1')

    with col2:
        st.header('Tabela 2')


with st.container():
    st.write('Outras tabelas')

    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.header('Tabela 3')

    with col2:
        st.header('Tabela 4')
