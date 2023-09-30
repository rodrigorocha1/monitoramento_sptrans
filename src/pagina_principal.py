import datetime
import streamlit as st
from database.carregar_dados_agrupados import consultar_dados


st.set_page_config(
    page_title='Monitoramento sptrans',
    layout='wide'
)


def gerar_input_data(key):
    d_time = st.date_input(
        'Selecione a data',
        (
            datetime.date(2023, 9, 15)
        ),

        datetime.date(2023, 9, 15),
        datetime.date(2023, 9, 19),
        format="YYYY-MM-DD",
        key=key,
    )
    selected_date = d_time.strftime("%Y-%m-%d")
    return selected_date


with st.sidebar:
    st.write('SideBarr')
st.write('Bem vindo')

with st.container():
    st.write('2 Tabelas')
    col1, col2 = st.columns([0.4, 0.5])

    with col1:
        st.header('Tabela 1')
        selected_date1 = gerar_input_data(key='selected_date1')
        option = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno1'
        )
        st.write('Selecionou', option)
        with st.spinner('Aguarde'):
            # @st.cache_data
            def cached_load_table1(option):
                df_table1, _ = consultar_dados(
                    data_consulta=selected_date1,
                    coluna_agrupamento=['DATA_EXTRACAO', 'CODIGO_AREA'],
                    ordenacao=['CODIGO_AREA'],
                    turno=option
                )
                return df_table1

        df_tabela1 = cached_load_table1(option)
        st.dataframe(df_tabela1)
        # st.plotly_chart(table_plot(df_tabela1, [df_tabela1.CODIGO_AREA,
        #                 df_tabela1.QUANTIDADE_VEICULOS_OPERACAO]))

    with col2:

        st.header('Tabela 2')
        option2 = st.selectbox(
            'Selecione o turno',
            ('Manhã', 'Tarde', 'Noite'),
            key='Turno2'
        )
        selected_date2 = gerar_input_data(key='selected_date2')
        st.write(selected_date2)
        with st.spinner('Aguarde'):
            # @st.cache_data
            def cached_load_table2(option):
                df_tabela2, _ = consultar_dados(
                    data_consulta=selected_date2,
                    coluna_agrupamento=['EMPRESA'],
                    ordenacao=['EMPRESA'],
                    turno=option

                )
                return df_tabela2

            df_tabela2 = cached_load_table2(option2)
            st.dataframe(df_tabela2)


with st.container():
    st.write('Outras tabelas')
    st.header('Tabela 4')
    option4 = st.selectbox(
        'Selecione o turno',
        ('Manhã', 'Tarde', 'Noite'),
        key='Turno4'
    )
    selected_date3 = gerar_input_data(key='selected_date3')
    st.write(selected_date3)
    with st.spinner('Aguarde'):
        # @st.cache_data
        def cached_load_table4(option):
            df_tabela4, _ = consultar_dados(
                data_consulta=selected_date3,
                coluna_agrupamento=[
                    'LETREIRO_COMPLETO',
                    'LETREIRO_ORIGEM',
                    'LETREIRO_DESTINO'
                ],
                ordenacao=['LETREIRO_COMPLETO'],
                turno=option
            )
            return df_tabela4
        df_tabela4 = cached_load_table4(option4)
        st.markdown(
            '<h1 style="text-align: center;">Visualização da Tabela</h1>', unsafe_allow_html=True)
        st.markdown(
            '<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
        st.dataframe(df_tabela4)
        st.markdown('</div>', unsafe_allow_html=True)
