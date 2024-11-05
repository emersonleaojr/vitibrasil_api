import requests
from bs4 import BeautifulSoup
from api.scraping.scraping import Scraping

class Exportacao(Scraping):

    def get_data(self):
        """
        Obter dados de Exportação

        :return: Retorna json de dados referente à exportação do ano informado na API
        """

        data_ingest = {}

        url_complements = [
                            f"ano={self.year}&opcao=opt_05&subopcao=subopt_01",
                            f"ano={self.year}&opcao=opt_05&subopcao=subopt_02",
                            f"ano={self.year}&opcao=opt_05&subopcao=subopt_03",
                            f"ano={self.year}&opcao=opt_05&subopcao=subopt_04"
                          ]

        data = []
        for complement in url_complements:
            url_export = self.url_base + complement
            response = requests.get(url_export)
            soup = BeautifulSoup(response.text, 'html.parser')
            tipo = soup.find('button', {'class': 'btn_sopt',
                                                    'name': "subopcao",
                                                    'type': "submit",
                                                    'value': url_export[-9:]})

            table = soup.find('table', {'class': 'tb_base tb_dados'})
            rows = table.find_all('tr')

            data_row, headers = self.extract_rows_headers(rows, table)

            list_dicts_data = []
            for row in data_row[1:-1]:
                list_dicts_data.append({
                                    headers[0]: row[0],
                                    headers[1]: row[1],
                                    headers[2]: row[2]
                                 })

            data.append({tipo.text: list_dicts_data})
        data_ingest['ano'] = self.year
        data_ingest['exportacao'] = data

        return data_ingest