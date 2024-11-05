# encoding: utf-8

import requests
from bs4 import BeautifulSoup
from scraping.scraping import Scraping


class Processamento(Scraping):

    def data_formatation(self, data_row, headers):
        """
        Função ajustada para atender as necessidades da informação de processamento

        :param data_row: Matriz de dados extraídos de cada  tabela de dados
        :param headers: Nome dos campos de cada tabela
        :return: Retorna um json hierarquizado por classe, item e subitem, quando aplicável
        """

        data = []
        item_key = None
        for row in data_row[1:-1]:
            if row[0] in ["TINTAS", "BRANCAS E ROSADAS", "BRANCAS", "Sem classificação"]:
                if item_key != None:
                    data.append({item_key: list_subitem, headers[1]: item_value})

                item_key = row[0]
                item_value = row[1]
                list_subitem = []

            else:
                list_subitem.append({
                                        headers[0]: row[0],
                                        headers[1]: row[1]
                                    })

        data.append({headers[0]: item_key, headers[1]: item_value})

        return data

    def get_data(self):
        """
        Obter dados de Processamento

        :return: Retorna json de dados referente ao processamento do ano informado na API
        """

        data_ingest = {}
        url_complements = [
                            f"ano={self.year}&opcao=opt_03&subopcao=subopt_01",
                            f"ano={self.year}&opcao=opt_03&subopcao=subopt_02",
                            f"ano={self.year}&opcao=opt_03&subopcao=subopt_03",
                            f"ano={self.year}&opcao=opt_03&subopcao=subopt_04"
                        ]

        data = []
        for complement in url_complements:
            url_viniferas = self.url_base + complement
            response = requests.get(url_viniferas)
            soup = BeautifulSoup(response.text, 'html.parser')

            tipo = soup.find('button', {
                                                    'class': 'btn_sopt',
                                                    'name':"subopcao",
                                                    'type':"submit",
                                                    'value':url_viniferas[-9:]})

            table = soup.find('table', {'class': 'tb_base tb_dados'})
            rows = table.find_all('tr')

            data_row, headers = self.extract_rows_headers(rows, table)

            data_list = self.data_formatation(data_row, headers)

            data.append({tipo.text:data_list})

        data_ingest['ano'] = self.year
        data_ingest['processamento'] = data

        return data_ingest