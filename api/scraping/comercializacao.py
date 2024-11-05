import requests
from bs4 import BeautifulSoup
from scraping.scraping import Scraping

class Comercializacao(Scraping):

    def get_data(self):
        """
        Obter dados de Comercialização

        :return: Retorna json de dados referente à comercialização do ano informado na API
        """

        data_ingest = {}

        url_comercial = self.url_base + f"ano={self.year}&opcao=opt_04"
        response = requests.get(url_comercial)

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'tb_base tb_dados'})
        rows = table.find_all('tr')

        data_row, headers = self.extract_rows_headers(rows, table)

        data = self.data_formatation(data_row, headers)

        data_ingest['ano'] = self.year
        data_ingest['comercializacao'] = data

        return data_ingest