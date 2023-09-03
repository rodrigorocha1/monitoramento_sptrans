from airflow.models import BaseOperator


class SptransOperator(BaseOperator):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
