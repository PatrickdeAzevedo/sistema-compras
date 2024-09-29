# app.py - Serviço Externo para Consumir a FakeStore com flask-openapi3
from flask import Flask, redirect, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
import requests

# Definição das informações da API usando OpenAPI e Info
info = Info(title="API Externa - FakeStore", version="1.0.0", description="Serviço para consultar produtos da FakeStore")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição de tags para organização das rotas
home_tag = Tag(name="Documentação", description="Escolha o tipo de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produtos", description="Rotas para gerenciar informações de produtos")

# Rota principal para exibir o Swagger UI com a documentação OpenAPI
@app.get('/', tags=[home_tag])
def home():
    """
    Página inicial do Serviço Exerno para consumir a FakeStoreAPI.
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Rota para buscar todos os produtos disponíveis na FakeStore API
@app.get('/produtos', tags=[produto_tag])
def get_all_produtos():
    """
    Retorna todos os produtos disponíveis na FakeStore.
    ---
    responses:
      200:
        description: Lista de produtos recuperada com sucesso
      500:
        description: Erro interno ao buscar produtos
    """
    try:
        response = requests.get('https://fakestoreapi.com/products')
        if response.status_code != 200:
            return jsonify({'error': 'Erro ao buscar lista de produtos'}), 500
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para buscar detalhes de um produto específico
@app.get('/produto/<int:produto_id>', tags=[produto_tag])
def get_produto(produto_id):
    """
    Busca informações de um produto específico.
    ---
    parameters:
      - name: produto_id
        in: path
        type: integer
        required: true
        description: ID do produto a ser buscado
        example: 1
    responses:
      200:
        description: Detalhes do produto recuperado com sucesso
      404:
        description: Produto não encontrado
      500:
        description: Erro interno ao buscar o produto
    """
    try:
        response = requests.get(f'https://fakestoreapi.com/products/{produto_id}')
        if response.status_code == 404:
            return jsonify({'error': 'Produto não encontrado'}), 404
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
