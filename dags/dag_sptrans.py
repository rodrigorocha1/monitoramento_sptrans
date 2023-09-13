try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from os.path import join
import pendulum
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.models import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from operators.sptrans_operator import SptransOperator
from src.api.api import API
today = pendulum.now('America/Sao_Paulo').format('YYYY_MM_DD')


dag = DAG('Extracao_dados_api_sptrans',
          description='Extração de dados',
          schedule_interval='*/4 * * * *',
          catchup=False,
          start_date=pendulum.datetime(2023, 9, 8, tz='America/Sao_Paulo'))


inicio_dag = EmptyOperator(
    task_id='inicio_dag', dag=dag
)

task_check_api = PythonOperator(
    task_id='task_check_api',
    python_callable=API.fazer_login_api,
    dag=dag
)


def checar_status(**context):
    flag = context['task_instance'].xcom_pull(task_ids='task_check_api')
    print('FLAG DA FLAG', flag)
    if flag:
        return 'extrair_dados_sptrans'
    return 'task_falha'


task_falha = EmptyOperator(
    task_id='task_falha',
    dag=dag,
    trigger_rule='one_failed'
)


banch_check_api = BranchPythonOperator(
    task_id='checar_conexao',
    python_callable=checar_status,
    provide_context=True,
    dag=dag
)

sptrans_operator = SptransOperator(
    task_id='extrair_dados_sptrans',
    file_path=join(
        'data/datalake/bronze',
        f'extract_date={today}',
        f'posicao_{today}.json'
    )
)


sptrans_transformacao = SparkSubmitOperator(
    task_id='id_sptrans_transformacao',
    conn_id='id_spark',
    application='/home/rodrigo/projetos/monitoramento_sptrans/src/data_transform/tranformacao_dataframe.py',
    name='sptrans_tranform',
    application_args=[
        '--src_operacao_dia',
        f'/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/bronze/extract_date={today}/*.json',
        '--src_dados_completos_onibus',
         '/home/rodrigo/projetos/monitoramento_sptrans/data/datalake/bronze/relacao_empresas_linha/dados_linhas_completo.csv'
    ]

)


task_fim_dag = EmptyOperator(
    task_id='task_fim_dag',
    dag=dag,
    trigger_rule='all_done'
)


inicio_dag >> task_check_api >> banch_check_api
banch_check_api >> sptrans_operator >> sptrans_transformacao >> task_fim_dag
banch_check_api >> task_falha >> task_fim_dag
