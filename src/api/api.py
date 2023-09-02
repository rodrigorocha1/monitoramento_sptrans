from typing import Tuple
import requests
from bs4 import BeautifulSoup


class API():

    @classmethod
    def ober_dados_linha(cls, codigo_linha: str) -> Tuple[str, str, str, str]:
        """Método para retornar os dados pertecentes a linha

        Args:
            codigo_linha (str): código da linha Ex: 1012-10

        Returns:
            Tuple[str, str, str, str]: Um tupla com os dados co código da linha, área de operação, consocio e empresa
        """
        url = 'https://sistemas.sptrans.com.br/PlanOperWeb/detalheLinha.asp'
        params = {
            'TpDiaID': '0',
            'project': 'OV',
            'lincod': codigo_linha
        }
        res = requests.get(url, params=params, timeout=10)
        html_page = res.text
        principal = BeautifulSoup(html_page, 'html.parser')
        area_codigo = principal.find(id='areCod').attrs['value']
        consocio = principal.find(id='consorcio').attrs['value']
        empresa = principal.find(id='empresa').attrs['value']
        return codigo_linha, area_codigo, consocio, empresa


if __name__ == '__main__':
    a = API.ober_dados_linha('1012-10')
    print(a)
