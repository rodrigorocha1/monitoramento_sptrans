from typing import Any
import json
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
    """_summary_

    Args:
        BaseOperator (_type_): _description_
    """

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)

    def execute(self, context: Context) -> Any:
        """_summary_

        Args:
            context (Context): _description_

        Returns:
            Any: _description_
        """
        req = SptransHook().run()
        with open('extracao_operacao.json', 'w') as output_file:
            json.dump(req, output_file, ensure_ascii=False)
            output_file.write('\n')
