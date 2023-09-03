from typing import Any
from airflow.models import BaseOperator
from airflow.utils.context import Context
try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from hook.sptrans_hook import SptransHook


class SptransOperator(BaseOperator):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def execute(self, context: Context) -> Any:
        req = SptransHook().run()
