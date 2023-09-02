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


task_check_api = PythonOperator(
    task_id='task_check_api',
    python_callable=API.fazer_login_api(),
    dag=dag
)


inicio_dag = EmptyOperator(
    task_id='inicio_dag', dag=dag
)


def checar_status(**context):
    flag = context['task_instance'].xcom_pull(task_ids='task_check_api')
    print(flag)


banch_check_api = BranchPythonOperator(
    task_id='checar_conexao',
    python_callable=checar_status,
    provide_context=True,
    dag=dag
)

inicio_dag >> banch_check_api
