# app.py - API Principal com integração ao flask-openapi3
from flask import Flask, redirect, request, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
import requests

# Definição das informações da API usando OpenAPI e Info
info = Info(title="API Principal", version="1.0.0", description="API Principal para um sistema de compras online")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição de tags para organização das rotas
home_tag = Tag(name="Documentação", description="Escolha o tipo de documentação: Swagger, Redoc ou RapiDoc")
status_tag = Tag(name="Status", description="Rota para verificar o status da API")
compra_tag = Tag(name="Compras", description="Rotas para gerenciar pedidos de compra")
produto_tag = Tag(name="Produtos", description="Rota para buscar informações de produtos")

# Rota principal para exibir o Swagger UI com a documentação OpenAPI
@app.get('/', tags=[home_tag])
def home():
    """
    Página inicial da API Principal.
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Rota GET para verificar o status
@app.get('/status', tags=[status_tag])
def status():
    """
    Verifica o status da API Principal.
    ---
    responses:
      200:
        description: Status da API
    """
    return jsonify({'status': 'API Principal funcionando!'}), 200

# Rota POST para criar um pedido de compra
@app.post('/comprar', tags=[compra_tag])
def comprar():
    """
    Cria um pedido de compra.
    ---
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              produto_id:
                type: integer
                description: ID do produto a ser comprado
                example: 1
              quantidade:
                type: integer
                description: Quantidade de produtos a serem comprados
                example: 2
    responses:
      200:
        description: Pedido de compra criado com sucesso
      400:
        description: Formato de dados inválido
      500:
        description: Erro interno ao registrar a compra
    """
    data = request.get_json()
    if not data or 'produto_id' not in data or 'quantidade' not in data:
        return jsonify({'error': 'Formato de dados inválido'}), 400

    try:
        response = requests.post("http://127.0.0.1:5002/compras", json=data)
        if response.status_code != 200:
            return jsonify({'error': 'Erro ao registrar compra no Módulo de Compras'}), 500
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota GET para buscar informações de um produto (comunicação com Componente B)
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
        description: Detalhes do produto
      404:
        description: Produto não encontrado
      500:
        description: Erro interno ao buscar o produto
    """
    try:
        response = requests.get(f"http://127.0.0.1:5001/produto/{produto_id}")
        if response.status_code == 404:
            return jsonify({'error': 'Produto não encontrado'}), 404
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota DELETE para excluir um pedido de compra
@app.delete('/pedido/<int:pedido_id>', tags=[compra_tag])
def deletar_pedido(pedido_id):
    """
    Deleta um pedido de compra existente.
    ---
    parameters:
      - name: pedido_id
        in: path
        type: integer
        required: true
        description: ID do pedido a ser deletado
        example: 1
    responses:
      200:
        description: Pedido deletado com sucesso
      404:
        description: Pedido não encontrado
      500:
        description: Erro interno ao deletar o pedido
    """
    try:
        response = requests.delete(f"http://127.0.0.1:5002/compras/{pedido_id}")
        if response.status_code == 404:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota PUT para atualizar um pedido de compra existente
@app.put('/pedido/<int:pedido_id>', tags=[compra_tag])
def atualizar_pedido(pedido_id):
    """
    Atualiza um pedido de compra.
    ---
    parameters:
      - name: pedido_id
        in: path
        type: integer
        required: true
        description: ID do pedido a ser atualizado
        example: 1
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              quantidade:
                type: integer
                description: Nova quantidade de produtos a serem comprados
                example: 5
    responses:
      200:
        description: Pedido atualizado com sucesso
      400:
        description: Formato de dados inválido
      404:
        description: Pedido não encontrado
      500:
        description: Erro interno ao atualizar o pedido
    """
    data = request.get_json()
    if not data or 'quantidade' not in data:
        return jsonify({'error': 'Formato de dados inválido'}), 400

    try:
        response = requests.put(f"http://127.0.0.1:5002/compras/{pedido_id}", json=data)
        if response.status_code == 404:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
