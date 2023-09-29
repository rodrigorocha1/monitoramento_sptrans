from functools import reduce
from datetime import datetime
import os
from typing import List
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


def load_database(_spark_sessao: SparkSession) -> List[DataFrame]:
    diretorio_agrupado = '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/prata/operacao_agrupada/'
    file_list = os.listdir(diretorio_agrupado)
    lista_dataframe = []
    for item in file_list:
        if item.endswith('.parquet'):
            caminho_completo = os.path.join(
                diretorio_agrupado, item
            )
            dataframe = _spark_sessao.read.parquet(caminho_completo)
            lista_dataframe.append(dataframe)
    return lista_dataframe


@F.udf(returnType=t.StringType())
def turno(hora: str) -> str:
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


def dataframe_filter(dataframe_completo: DataFrame,
                     data_extracao: str,
                     coluna_agrupamento: str
                     ) -> DataFrame:
    dataframes_agrupados_completo = dataframe_completo.withColumn(
        'TURNO', turno(F.col('HORA_API'))
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
    ) \
        .filter(
        (dataframes_agrupados_completo.DATA_EXTRACAO == data_extracao)
    )\
        .groupBy(['DATA_EXTRACAO', 'CODIGO_AREA']) \
        .agg(
        F.sum('QTDE_VEICULOS_OPERACAO')
        .alias('QUANTIDADE_VEICULOS_OPERACAO')
    ).orderBy(coluna_agrupamento)

    return df_filter


def consultar_dados(data_consulta, coluna_agrupamento):
    sessao_spark = iniciar_sessao_spark()

    df_original = load_database(sessao_spark)
    df_original = union_all(df_original)
    df_filter = dataframe_filter(
        dataframe_completo=df_original,
        data_extracao=data_consulta,
        coluna_agrupamento=coluna_agrupamento
    )
    df_filter = df_filter.toPandas()

    return df_filter
