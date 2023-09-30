from functools import reduce
from datetime import datetime
from datetime import date
import os
from typing import List
import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import pyspark.sql.types as t
from pyspark.sql import DataFrame


def iniciar_sessao_spark() -> SparkSession:
    sessao_spark = SparkSession.builder.master('local[*]') \
        .appName('Métricas') \
        .getOrCreate()
    return sessao_spark


def union_all(dfs) -> DataFrame:
    return reduce(DataFrame.unionAll, dfs)


def load_database() -> List[DataFrame]:
    diretorio_agrupado = '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/prata/operacao_agrupada/'
    file_list = os.listdir(diretorio_agrupado)
    lista_dataframe = []
    for item in file_list:
        if item.endswith('.parquet'):
            caminho_completo = os.path.join(
                diretorio_agrupado, item
            )
            dataframe = iniciar_sessao_spark().read.parquet(caminho_completo)
            lista_dataframe.append(dataframe)
    return lista_dataframe


def obter_colunas_tempo() -> List[date]:
    df_original = union_all(load_database())
    colunas_tempo = df_original.select('DATA_EXTRACAO') \
        .distinct() \
        .rdd.flatMap(lambda linha: [linha.DATA_EXTRACAO]) \
        .collect()
    return colunas_tempo


@F.udf(returnType=t.StringType())
def verificar_turno(hora: str) -> str:
    hora_formatada = datetime.strptime(hora, '%H:%M').time()
    if 0 <= hora_formatada.hour < 6:
        turno = 'Madrugada'
    elif 6 <= hora_formatada.hour < 12:
        turno = 'Manhã'
    elif 12 <= hora_formatada.hour < 18:
        turno = 'Tarde'
    else:
        turno = 'Noite'
    return turno


def dataframe_filter(
    dataframe_completo: DataFrame,
    data_extracao: str,
    coluna_agrupamento: List[str],
    ordenacao: str,
    turno
) -> DataFrame:
    dataframes_agrupados_completo = dataframe_completo.withColumn(
        'TURNO', verificar_turno(F.col('HORA_API'))
    )

    df_filter = dataframes_agrupados_completo.select(
        dataframes_agrupados_completo.CODIGO_AREA,
        dataframes_agrupados_completo.CONSOCIO,
        dataframes_agrupados_completo.EMPRESA,
        dataframes_agrupados_completo.TURNO,
        dataframes_agrupados_completo.DATA_EXTRACAO,
        dataframes_agrupados_completo.LETREIRO_ORIGEM,
        dataframes_agrupados_completo.LETREIRO_DESTINO,
        dataframes_agrupados_completo.HORA_API,
        dataframes_agrupados_completo.LETREIRO_COMPLETO,
        dataframes_agrupados_completo.QTDE_VEICULOS_OPERACAO,
        dataframes_agrupados_completo.CODIGO_IDENTIFICADOR,
    ).filter(
        (dataframes_agrupados_completo.DATA_EXTRACAO == data_extracao) &
        (dataframes_agrupados_completo.TURNO == turno)
    ) \
        .groupBy(coluna_agrupamento) \
        .agg(
        F.sum('QTDE_VEICULOS_OPERACAO')
        .alias('QUANTIDADE_VEICULOS_OPERACAO')
    ).orderBy(ordenacao)

    return df_filter


def consultar_dados(coluna_agrupamento, data_consulta, ordenacao, turno):
    if 'data' not in st.session_state:
        df_original = load_database()
        df_original = union_all(df_original)
        st.session_state['data'] = df_original
        print('not session')
    else:
        df_original = st.session_state['data']
        print('sesion')
    df_filter = dataframe_filter(
        dataframe_completo=df_original,
        data_extracao=data_consulta,
        coluna_agrupamento=coluna_agrupamento,
        ordenacao=ordenacao,
        turno=turno
    )
    df_filter = df_filter.toPandas()

    return df_filter, df_original.columns
