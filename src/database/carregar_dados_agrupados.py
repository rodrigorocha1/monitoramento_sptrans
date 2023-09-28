from functools import reduce
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import pyspark.sql.types as t
from pyspark.sql import DataFrame


class CarregarDadosAgrupados:
    def __init__(self) -> None:
        self.__diretorio_agrupado = '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/prata/operacao_agrupada/'
        self.__spark_session = SparkSession.builder.master('local[*]') \
            .appName('Métricas') \
            .getOrCreate()

        self.__dataframes = []

    def union_all(self, dfs) -> DataFrame:
        return reduce(DataFrame.unionAll, dfs)

    def __load_database(self) -> DataFrame:
        file_list = os.listdir(self.__diretorio_agrupado)

        for item in file_list:
            if item.endswith('.parquet'):
                caminho_completo = os.path.join(
                    self.__diretorio_agrupado, item
                )
                dataframe = self.__spark_session.read.parquet(caminho_completo)
                self.__dataframes.append(dataframe)

    @staticmethod
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

    def __dataframe_filter(self, dataframe_completo: DataFrame,  data_extracao: str, coluna_agrupamento: str) -> DataFrame:
        print('dataframe_completo')
        print(dataframe_completo.columns)
        dataframes_agrupados_completo = dataframe_completo.withColumn(
            'TURNO', self.turno(F.col('HORA_API'))
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

    # def __stop_spark_session(self):
    #     if self.__spark_session is not None:
    #         self.__spark_session.stop()

    def consultar_dados(self, data_consulta, coluna_agrupamento):
        self.__load_database()
        df_completo = self.union_all(self.__dataframes)
        df_filter = self.__dataframe_filter(
            dataframe_completo=df_completo,
            data_extracao=data_consulta,
            coluna_agrupamento=coluna_agrupamento
        )
        df_filter = df_filter.toPandas()
        self.__spark_session.stop()
        return df_filter
