import argparse
from pyspark.sql import functions as f
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import SparkSession


def operacao_agrupada(df_param: DataFrame) -> DataFrame:
    """Função para gerar o dataframe de operação agrupado

    Args:
        df_param (DataFrame): dataframe

    Returns:
        DataFrame: dataframe com a operação agrupada
    """
    df_operacao = df_param.select(df_param.hr, df_param.data_extracao, f.explode('l').alias('DADOS_LINHA')) \
        .withColumnRenamed('hr', 'HORA_API') \
        .select('HORA_API',
                'DATA_EXTRACAO',
                f.col('DADOS_LINHA.c').alias('LETREIRO_COMPLETO'),
                f.col('DADOS_LINHA.cl').alias('CODIGO_IDENTIFICADOR'),
                f.col('DADOS_LINHA.lt0').alias('LETREIRO_ORIGEM'),
                f.col('DADOS_LINHA.lt1').alias('LETREIRO_DESTINO'),
                f.col('DADOS_LINHA.qv').alias('QTDE_VEICULOS_OPERACAO'),
                )
    return df_operacao


def juncao_dataframe(df_um: DataFrame,
                     df_dois: DataFrame,
                     coluna_um: str,
                     coluna_dois: str,
                     tipo_juncao: str = 'inner') -> DataFrame:
    """Finção para gerar a junção entre dois dataframes

    Args:
        df_um (DataFrame): dataframe das operações dos ônibus agrupadas / desagrupadas
        df_dois (DataFrame): dataframe com a lista das operações
        coluna_um (str): coluna de junção dos ônibus
        coluna_dois (str): ccoluna do dataframe das operações dos ônibus agrupadas / desagrupadas
        tipo_juncao (str, optional): tipo de junção Defaults to 'inner'.

    Returns:
        DataFrame: _description_
    """
    df_dados_completos_operacao = df_um.join(
        df_dois, f.col(coluna_um) == f.col(coluna_dois), tipo_juncao)
    df_dados_completos_operacao = df_dados_completos_operacao.withColumn(
        'DATA_EXTRACAO', f.to_date('DATA_EXTRACAO'))
    colunas = ('_c0', '_c1')
    df_dados_completos_operacao = df_dados_completos_operacao.withColumn(
        'DATA_EXTRACAO_API', f.to_date('DATA_EXTRACAO'))
    df_dados_completos_operacao = df_dados_completos_operacao.drop(*colunas)
    return df_dados_completos_operacao


def export_json(df_param: DataFrame,
                coluna_particao: str,
                path_exportacao: str,
                mode: str = 'overwrite') -> None:
    """Função para gravar o json do datalake

    Args:
        df_param (DataFrame): dataframe tratada
        coluna_particao (str): coluna para fazer a partição
        path_exportacao (str): caminho para gravar o dataframe
        mode (str, optional): tipo de gravação. Defaults to 'overwrite'.
    """
    df_param.coalesce(1) \
        .write \
        .partitionBy(coluna_particao) \
        .mode(mode)\
        .json(path_exportacao)


def operacao_desagrupada(df_param: DataFrame) -> DataFrame:
    """Função para fazer tratamento do dataframe base

    Args:
        df_param (DataFrame): dataframe base

    Returns:
        DataFrame: Dataframe com as operações desagrupadas
    """
    df_p = df_param.select(
        df_param.data_extracao,
        df_param.hr,
        f.explode(df_param.l).alias('lista')
    )
    df_p = df_p.select(df_p.data_extracao, df_p.lista, df_p.hr)

    df_amostra_um = df_p.select(
        df_p.data_extracao,
        df_p.hr,
        df_p.lista.c.alias('LETREIRO_COMPLETO'),
        df_p.lista.sl.alias('SENTIDO_OPERACAO'),
        df_p.lista.cl.alias('CODIGO_IDENTIFICADOR_LINHA'),
        f.explode(df_p.lista.vs).alias('expansao')) \
        .select(f.col('data_extracao').alias('DATA_EXTRACAO'),
                f.col('hr').alias('HORA_API'),
                'LETREIRO_COMPLETO',
                'SENTIDO_OPERACAO',
                'CODIGO_IDENTIFICADOR_LINHA',
                f.col('expansao.p').alias('PREFIXO_ONIBUS'),
                f.col('expansao.ta').alias('DATA_HORA_CAPTURA_LOCALIZACAO'),
                f.col('expansao.py').alias('LATITUDE'),
                f.col('expansao.px').alias('LONGITUDE'),

                ) \
        .sort(df_p.data_extracao.desc(), df_p.lista.c.asc())

    return df_amostra_um


def sptrans_tranform(spark_session: SparkSession,
                     src_operacao_dia: str,
                     src_dados_completos_onibus: str
                     ):
    """Método para transformação

    Args:
        spark_session (SparkSession): sessão dia
        src_operacao_dia (str): caminho do datalake
        src_dados_completos_onibus (str): caminho do csv com a listagem de empresas
    """
    df_operacao_dia = spark_session.read.json(src_operacao_dia)
    df_operacao_agrupada = operacao_agrupada(df_operacao_dia)
    df_operacao_desagrupada = operacao_desagrupada(df_operacao_dia)
    df_lista_consocio = spark.read \
        .options(header=True) \
        .csv(src_dados_completos_onibus)

    df_dados_completos_operacao_desagrupada = juncao_dataframe(
        df_lista_consocio,
        df_operacao_desagrupada,
        'LINHA',
        'LETREIRO_COMPLETO',

    )

    df_dados_completos_operacao_agrupada = juncao_dataframe(
        df_lista_consocio,
        df_operacao_agrupada,
        'LINHA',
        'LETREIRO_COMPLETO'
    )

    export_json(
        df_dados_completos_operacao_desagrupada,
        'DATA_EXTRACAO_API',
        '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/prata/operacao_desagrupada'
    )

    export_json(
        df_dados_completos_operacao_agrupada,
        'DATA_EXTRACAO_API',
        '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/prata/operacao_agrupada'
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='teste Extracao'
    )

    parser.add_argument('--src_operacao_dia', required=True)
    parser.add_argument('--src_dados_completos_onibus', required=True)
    args = parser.parse_args()
    spark = SparkSession\
        .builder\
        .appName("sptrans_transformation")\
        .getOrCreate()

    sptrans_tranform(
        spark,
        args.src_operacao_dia,
        args.src_dados_completos_onibus
    )
