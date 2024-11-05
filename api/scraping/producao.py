import requests
from bs4 import BeautifulSoup
from api.scraping.scraping import Scraping


class Producao(Scraping):

    def get_data(self):
        """
        Obter dados de Produção

        :return: Retorna json de dados referente à produção do ano informado na API
        """
        url_producao = self.url_base + f"ano={self.year}&opcao=opt_02"
        response = requests.get(url_producao)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'tb_base tb_dados'})
        rows = table.find_all('tr')

        data_row, headers = self.extract_rows_headers(rows, table)

        data = self.data_formatation(data_row, headers)

        data_ingest = {}

        data_ingest['ano'] = self.year
        data_ingest['producao'] = data

        return data_ingest
