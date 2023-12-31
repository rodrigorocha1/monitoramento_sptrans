from typing import Any
from pathlib import Path
from airflow.models import BaseOperator
from airflow.utils.context import Context
try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from src.database.infra import gravar_json
from hook.sptrans_hook import SptransHook


class SptransOperator(BaseOperator):
    """_summary_

    Args:
        BaseOperator (_type_): _description_
    """
    template_fields = ['file_path']

    def __init__(self, file_path, **kwargs):
        """Método de Init para a classe

        Args:
            file_path (_type_): caminho da
        """
        self.file_path = file_path
        super().__init__(**kwargs)

    def create_parent_folder(self):
        """Método para criar pastas
        """
        (Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)

    def execute(self, context: Context) -> Any:
        """Método para gravar o json

        Args:
            context (Context): _description_

        Returns:
            Any: _description_
        """
        req = SptransHook().run()
        self.create_parent_folder()
        gravar_json(req=req, path=self.file_path)
