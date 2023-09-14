from typing import Dict
import json


def gravar_json(req: Dict, path: str):
    """Função para gravar json na camada bronze

    Args:
        req (Dict): Dicionario com a requisção feita pela api da sptrans
        path (str): Caminho da camada bronze
    """
    with open(path, 'a') as output_file:
        if output_file is not None:
            json.dump(req, output_file, ensure_ascii=False)
            output_file.write('\n')
