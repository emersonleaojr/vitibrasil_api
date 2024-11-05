class Scraping:
    def __init__(self, url_base, year):
        """
        Inicializa o objeto Scraping que possui dados e funções que são herdadas pelos demais módulos

        :param url_base: Link da tela inicial do projeto VitiBrasil do Embrapa
        :param year: Ano específicado para aquisição do dado
        """

        self.url_base = url_base
        self.year = year

    def extract_rows_headers(self, rows, table):
        """
        Função para retornar linhas e os nomes dos campos das tabelas, retirando as marcações de html dessas.

        :param rows: Lista de linhas da tabela, ainda com marcações html
        :param table: Lista de nomes dos campos da tabela, ainda com marcações html
        :return: Listas de linhas e os nomes dos campos das tabelas, retirando as marcações de html dessas.
        """

        data_row = []
        for row in rows:
            cells = row.find_all('td')
            cells_text = [cell.get_text(strip=True) for cell in cells]
            data_row.append(cells_text)

        table_headers = table.find_all("th")
        headers = [table_header.get_text(strip=True) for table_header in table_headers]

        return data_row, headers

    def data_formatation(self, data_row, headers):
        """
        Formatação final do dicionário de saída dos módulos de scraping

        :param data_row: Matriz de dados extraídos de cada  tabela de dados
        :param headers: Nome dos campos de cada tabela
        :return: Retorna um json hierarquizado por classe, item e subitem, quando aplicável
        """
        data = []
        item_key = None
        for row in data_row[1:-1]:
            if row[0].isupper() or row[0] == "Sem classificação":
                if item_key != None:
                    data.append({item_key: list_subitem, headers[1]: item_value})

                item_key = row[0]
                item_value = row[1]
                list_subitem = []

                if item_key == "Sem classificação":
                    list_subitem.append({
                                            headers[0]: row[0],
                                            headers[1]: row[1]
                                        })
            else:
                list_subitem.append({
                                        headers[0]: row[0],
                                        headers[1]: row[1]
                                    })

        data.append({item_key: list_subitem, headers[1]: item_value})

        return data