try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow import DAG
from src.api.api import API


dag = DAG('Extracao_dados_api_sptrans',
          description='Extração de dados',
          schedule_interval=None,
          start_date=datetime(2023, 3, 5))


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
        return 'task_sucesso'
    return 'task_falha'


task_sucesso = EmptyOperator(
    task_id='task_sucesso',
    trigger_rule='none_failed',
    dag=dag
)

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

task_fim_dag = EmptyOperator(
    task_id='task_fim_dag',
    dag=dag,
    trigger_rule='dummy'
)

inicio_dag >> task_check_api >> banch_check_api
banch_check_api >> task_sucesso >> task_fim_dag
banch_check_api >> task_falha >> task_fim_dag
