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
from operators.sptrans_operator import SptransOperator
from src.api.api import API


dag = DAG('Extracao_dados_api_sptrans',
          description='Extração de dados',
          schedule_interval='*/2 * * * *',
          catchup=False,
          start_date=pendulum.datetime(2023, 9, 3, tz='UTC'))


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

to = SptransOperator(
    task_id='extrair_dados_sptrans',
    file_path=join(
        'data/datalake/bronze',
        'extract_date={{ ds }}',
        'posicao_{{ ds_nodash }}.json'
    )
)

task_fim_dag = EmptyOperator(
    task_id='task_fim_dag',
    dag=dag,
    trigger_rule='all_done'
)

inicio_dag >> task_check_api >> banch_check_api
banch_check_api >> to >> task_fim_dag
banch_check_api >> task_falha >> task_fim_dag
