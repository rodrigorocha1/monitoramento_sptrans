from typing import Tuple
import requests
from bs4 import BeautifulSoup
from airflow.models import Variable


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
        res = requests.get(url, params=params, timeout=20)
        html_page = res.text
        principal = BeautifulSoup(html_page, 'html.parser')
        area_codigo = principal.find(id='areCod').attrs['value']
        consocio = principal.find(id='consorcio').attrs['value']
        empresa = principal.find(id='empresa').attrs['value']
        return codigo_linha, area_codigo, consocio, empresa

    @classmethod
    def fazer_login_api(cls) -> Tuple[str, bool]:
        try:
            auth = requests.post(
                Variable.get('URL_SPTRANS') + '/v2.1/Login/Autenticar?token=' + Variable.get('TOKEN_SPTRANS'))
            credenciais = auth.headers["Set-Cookie"].split(";")[
                0].split("=")[-1]
            return credenciais, True
        except requests.exceptions.ConnectTimeout:
            return 'Timeout no login', False
        except requests.exceptions.ConnectionError:
            return 'Erro na conexão', False

    @classmethod
    def pos(cls):
        api_chave = cls.fazer_login_api()
        pos = requests.get(
            'http://api.olhovivo.sptrans.com.br/v2.1/Posicao', cookies={"apiCredentials": api_chave[0]}
        )
        return pos.json()


if __name__ == '__main__':
    print(API.pos())
