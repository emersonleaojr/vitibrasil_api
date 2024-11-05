from flask import Flask,jsonify
from flasgger import Swagger
from scraping.producao import Producao
from scraping.processamento import Processamento
from scraping.comercializacao import Comercializacao
from scraping.importacao import Importacao
from scraping.exportacao import Exportacao

url_home = "http://vitibrasil.cnpuv.embrapa.br/index.php?"

app = Flask("__name__")

app.json.sort_keys = False
swagger = Swagger(app, template= {
    "swagger": "3.0",
    "openapi": "3.0.0",
    "info": {
        "title": "Vitivinicultura",
        "version": "0.0.1",
    }
})

@app.route("/", methods=["GET"])
def home():
    """
       Homepage da API
       ---
       description: Homepage da API
       tags:
         - homepage
       """
    return """
                <h1>API de Vitinicultura</h1>
                
                <p>Essa API visa retornar dados anuais do Rio Grande do Sul sobre produção, processamento, comercialização, importação e exportação de derivados da vitivinicultura a partir de 1970 até 2023.</p>
                
                <p>Para obter dados de produção: incluir /producao/{ano desejado} ao fim do link da API.</p>
                <p>Para obter dados de processamento: incluir /processamento/{ano desejado} ao fim do link da API.</p>
                <p>Para obter dados de comercializacao: incluir /comercializacao/{ano desejado} ao fim do link da API.</p>
                <p>Para obter dados de importação: incluir /importacao/{ano desejado} ao fim do link da API.</p>
                <p>Para obter dados de exportação: incluir /exportacao/{ano desejado} ao fim do link da API.</p>
                <h2>Exemplo de Preenchimento:</h2>
                <p>Preenchimento para ter dados de produção do ano de 1970, digite: http://127.0.0.1:5000/producao/1970.</p>
            """

@app.route("/producao/<int:year>", methods=["GET"])
def producaoano(year):
    """
    Obter dados de producao
    ---
    description: Obter dados de producao
    tags:
      - producao
    parameters:
      - name: year
        in: path
        description: ano da consulta [ex. 1980]
        required: true
        schema:
          type: int
    """
    prod = Producao(url_home, year)
    return jsonify(prod.get_data())

@app.route("/processamento/<int:year>", methods=["GET"])
def processamentoano(year):
    """
    Obter dados de processamento
    ---
    description: Obter dados de processamento
    tags:
      - processamento
    parameters:
      - name: year
        in: path
        description: ano da consulta [ex. 1980]
        required: true
        schema:
          type: int
    """
    proc = Processamento(url_home, year)
    return jsonify(proc.get_data()),200

@app.route("/comercializacao/<int:year>", methods=["GET"])
def comercializacao(year):
    """
    Obter dados de comercializacao
    ---
    description: Obter dados de comercializacao
    tags:
      - comercializacao
    parameters:
      - name: year
        in: path
        description: ano da consulta [ex. 1980]
        required: true
        schema:
          type: int
    """
    comerc = Comercializacao(url_home, year)
    return jsonify(comerc.get_data())

@app.route("/importacao/<int:year>", methods=["GET"])
def importacao(year):
    """
    Obter dados de importacao
    ---
    description: Obter dados de importacao
    tags:
      - importacao
    parameters:
      - name: year
        in: path
        description: ano da consulta [ex. 1980]
        required: true
        schema:
          type: int
    """
    importa = Importacao(url_home, year)
    return jsonify(importa.get_data())

@app.route("/exportacao/<int:year>", methods=["GET"])
def exportacao(year):
    """
    Obter dados de exportacao
    ---
    description: Obter dados de exportacao
    tags:
      - exportacao
    parameters:
      - name: year
        in: path
        description: ano da consulta [ex. 1980]
        required: true
        schema:
          type: int
    """
    exporta = Exportacao(url_home, year)
    return jsonify(exporta.get_data())