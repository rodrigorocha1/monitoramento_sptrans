from typing import Dict
import json


def gravar_json(req: Dict, path: str):
    with open(path, 'a') as output_file:
        if output_file is not None:
            json.dump(req, output_file, ensure_ascii=False)
            output_file.write('\n')
