try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
    from src.api.api import API
except:
    pass


obter_dados_linha = API.ober_dados_linha('1012-10')
print(obter_dados_linha)
