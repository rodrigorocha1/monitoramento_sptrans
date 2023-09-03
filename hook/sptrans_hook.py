try:
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.curdir))
except ModuleNotFoundError:
    pass
from airflow.providers.http.hooks.http import HttpHook
from airflow.models import Variable
import requests
from src.api.api import API



class SptransHook(HttpHook):
    def __init__(self,  conn_id=None) -> None:
        self.conn_id = conn_id
        super().__init__(http_conn_id=self.conn_id)

    def create_url(self):
        url = Variable.get('URL_SPTRANS') + '/v2.1/Posicao'
        return url

    def conectar_api(self, session):
        cookies = API.fazer_login_api()
        request = requests.Request('GET', self.create_url(), cookies={
            "apiCredentials": cookies[0]})
        prep = session.prepare_request(request)
        self.log.info(f'URL: {self.create_url()}')
        return self.run_and_check(session, prep, {})

    def obter_requisicao(self, session):
        response = self.conectar_api(session)
        json_response = response.json()
        return json_response

    def run(self):
        session = self.get_conn()
        return self.obter_requisicao(session)


if __name__ == '__main__':
    req = SptransHook().run()
    print(req)
