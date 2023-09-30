from typing import List
import os
import math
import folium
import pandas as pd
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import DoubleType, FloatType
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
    ).orderBy('PREFIXO_ONIBUS')\
        .distinct().rdd.flatMap(lambda linha: [linha.PREFIXO_ONIBUS]).collect()
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


def obter_posicao_onibus(df_posicao: DataFrame) -> List[List]:
    posicao_onibus = df_posicao.rdd.flatMap(
        lambda linha: [[(linha.HORA_API), [linha.LATITUDE, linha.LONGITUDE]]]
    ).collect()
    return posicao_onibus


def gerar_mapa(posicao_onibus: List[List], tracado_linha: List[List], cor_linha: str, prefixo_onibus: str):
    mapa_linhas = folium.Map(location=posicao_onibus[0][1],
                             zoom_start=12,
                             control_scale=True)

    for posicao in posicao_onibus:
        folium.Marker(
            location=posicao[1],
            popup=f'Prefixo ônibus {prefixo_onibus} - Hora : {posicao[0]}',
            icon=folium.Icon(color='blue')
        ).add_to(mapa_linhas)

    for i in range(len(tracado_linha)-1):
        folium.PolyLine(
            locations=[
                [tracado_linha[i][0], tracado_linha[i][1]],
                [tracado_linha[i+1][0], tracado_linha[i+1][1]]
            ],
            color=f'#{cor_linha}').add_to(mapa_linhas)

    mapa_linhas.add_child(folium.LatLngPopup())

    return mapa_linhas


def obter_id_tracado_linha(spark_session: SparkSession, rota_id: str):
    df_selecao_linha = spark_session.read \
        .options(delimiter=',', header=True, inferSchema='True') \
        .csv('/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/bronze/arquivos_gtfs/trips.txt', )
    df_selecao_linha = df_selecao_linha.select(
        df_selecao_linha.shape_id
    ).filter(
        df_selecao_linha.route_id == rota_id
    )
    shape_id = df_selecao_linha.rdd.flatMap(
        lambda linha: [linha.shape_id]).collect()
    return shape_id


def obter_tracado_linha(spark_session: SparkSession, shape_id: List):
    df_trajeto_linhas = spark_session.read.options(delimiter=',', header=True).csv(
        '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/bronze/arquivos_gtfs/shapes.txt', )
    df_linha_filter = df_trajeto_linhas.filter(
        df_trajeto_linhas.shape_id.isin(shape_id))
    df_linha_filter = df_linha_filter.withColumn(
        'shape_pt_lat', F.col('shape_pt_lat').cast(FloatType()))
    df_linha_filter = df_linha_filter.withColumn(
        'shape_pt_lon', F.col('shape_pt_lon').cast(FloatType()))
    posicao = df_linha_filter.rdd.flatMap(
        lambda linha: [[linha.shape_pt_lat, linha.shape_pt_lon]]).collect()
    return posicao
