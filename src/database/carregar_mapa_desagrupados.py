from typing import List
import os
import math
import pandas as pd
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import DoubleType
import pyspark.sql.functions as F
from carregar_dados_agrupados import union_all, verificar_turno


def load_dataframe_desagrupados(spark: SparkSession) -> DataFrame:
    directory_path = "/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/prata/operacao_desagrupada"
    file_list = os.listdir(directory_path)
    dataframes_desagrupados = []
    for item in file_list:
        if item.endswith('.parquet'):
            caminho_completo = os.path.join(directory_path, item)

            df_agrupados = spark.read.parquet(caminho_completo)
            dataframes_desagrupados.append(df_agrupados)
    dataframe = union_all(dataframes_desagrupados)
    dataframe = dataframe.drop('LINHA')
    dataframe = dataframe.withColumn(
        'TURNO', verificar_turno(F.col('HORA_API')))
    return dataframe


def obter_prefixo_onibus(dataframes_desagrupados_completo: DataFrame) -> List[int]:
    df_prefixo_onibus = dataframes_desagrupados_completo.select(
        dataframes_desagrupados_completo.PREFIXO_ONIBUS,
    ).distinct().rdd.flatMap(lambda linha: [linha.PREFIXO_ONIBUS]).collect()
    return df_prefixo_onibus


def dataframe_filter_desagrupados(
        dataframes_desagrupados_completo: DataFrame,
        prefixo_onibus: int,
        turno: str,
        data_extracao: str
):
    dataframe_prefixo_onibus = dataframes_desagrupados_completo \
        .select(
            dataframes_desagrupados_completo.HORA_API,
            dataframes_desagrupados_completo.PREFIXO_ONIBUS,
            dataframes_desagrupados_completo.CODIGO_IDENTIFICADOR_LINHA,
            dataframes_desagrupados_completo.LETREIRO_COMPLETO,
            dataframes_desagrupados_completo.LATITUDE,
            dataframes_desagrupados_completo.LONGITUDE,
        ) \
        .filter(
            (dataframes_desagrupados_completo.PREFIXO_ONIBUS == prefixo_onibus) &
            (dataframes_desagrupados_completo.TURNO == turno) &
            (dataframes_desagrupados_completo.DATA_EXTRACAO == data_extracao)
        )
    return dataframe_prefixo_onibus


def obter_letreiro_onibus(dataframe_prefixo_onibus: DataFrame) -> str:
    prefixo_onibus = dataframe_prefixo_onibus.select(
        dataframe_prefixo_onibus.LETREIRO_COMPLETO
    ) \
        .distinct().collect()[0][0]
    return prefixo_onibus


def obter_rota_linha(letreiro_onibus: str) -> List[str]:
    df_selecao_rota_linha = pd.read_csv(
        '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/bronze/arquivos_gtfs/routes.txt',)
    df_selecao_rota_linha['route_id'] = df_selecao_rota_linha['route_id'].astype(
        'string')
    df_selecao_rota_linha['route_short_name'] = df_selecao_rota_linha['route_short_name'].astype(
        'string')
    df_selecao_rota_linha['route_long_name'] = df_selecao_rota_linha['route_long_name'].astype(
        'string')
    df_selecao_rota_linha['route_color'] = df_selecao_rota_linha['route_color'].astype(
        'string')
    df_selecao_rota_linha['route_text_color'] = df_selecao_rota_linha['route_text_color'].astype(
        'string')
    df_selecao_rota_linha = df_selecao_rota_linha.query(
        f'route_id == "{letreiro_onibus}"')
    lista_onibus = df_selecao_rota_linha[[
        'route_id', 'route_long_name', 'route_color']].values.tolist()
    return lista_onibus


def haversine(lat1, lon1, lat2, lon2):

    RAIO_TERRA = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    aaaa = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2)**2
    cccc = 2 * math.atan2(math.sqrt(aaaa), math.sqrt(1 - aaaa))

    distance = RAIO_TERRA * cccc

    return distance


@F.pandas_udf(DoubleType())
def haversine_udf(lat, lon):
    distances = []
    for i in range(len(lat)):

        if i == 0:
            distances.append(0.0)
        else:
            distance = haversine(lat[i], lon[i], lat[i - 1], lon[i - 1])
            distances.append(distance)
    return pd.Series(distances)


def obter_posicao_onibus(df_posicao: DataFrame):
    posicao_onibus = df_posicao.rdd.flatMap(
        lambda linha: [[linha.LATITUDE, linha.LONGITUDE]]
    ).collect()

    return posicao_onibus
