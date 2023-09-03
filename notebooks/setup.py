try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
    from src.api.api import API
except ModuleNotFoundError:
    pass
import os
import pandas as pd

os.system('clear')

obter_dados_linha = API.ober_dados_linha('1012-10')
print(obter_dados_linha)

caminho = os.getcwd() + '/data/datalake/bronze/arquivos_gtfs/routes.txt'
print(caminho)

base_linha = pd.read_csv(caminho)
for indice, valor in base_linha.iterrows():
    dados_linha = API.ober_dados_linha(valor['route_id'])
    print(indice + 1, valor['route_id'], dados_linha)
    print()
