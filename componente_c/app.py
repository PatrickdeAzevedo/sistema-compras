# app.py - Módulo de Compras com integração ao flask-openapi3
from flask import Flask, redirect, request, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

# Definição das informações da API usando OpenAPI e Info
home_tag = Tag(name="Documentação", description="Escolha o tipo de documentação: Swagger, Redoc ou RapiDoc")
info = Info(title="Módulo de Compras", version="1.0.0", description="API para gerenciamento de compras")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definição de tags para organização das rotas
compra_tag = Tag(name="Compras", description="Rotas para gerenciar as compras")

# Definir o caminho do banco de dados SQLite dentro do container
db_filename = "compras.db"
db_path = os.path.join(os.getcwd(), db_filename)

# Função para inicializar o banco de dados SQLite
def init_db():
    # Verifique se o arquivo já existe para evitar recriação
    if not os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS compras (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER,
                    quantidade INTEGER
                )
            ''')
            conn.commit()
            conn.close()
            print(f"Banco de dados criado com sucesso no caminho: {db_path}")
        except sqlite3.Error as e:
            print(f"Erro ao criar o banco de dados: {e}")
    else:
        print(f"Banco de dados já existente no caminho: {db_path}")

# Rota principal para exibir o Swagger UI com a documentação OpenAPI
@app.get('/', tags=[home_tag])
def home():
    """
    Página inicial do Módulo de Compras.
    Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Rota para criar uma compra (POST)
@app.post('/compras', tags=[compra_tag])
def criar_compra():
    """
    Cria um registro de compra.
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
                description: Quantidade do produto a ser comprado
                example: 3
    responses:
      200:
        description: Compra criada com sucesso
      400:
        description: Erro no formato dos dados enviados
      500:
        description: Erro interno ao registrar a compra
    """
    data = request.get_json()
    if not data or 'produto_id' not in data or 'quantidade' not in data:
        return jsonify({'error': 'Formato de dados inválido'}), 400
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO compras (produto_id, quantidade) VALUES (?, ?)
        ''', (data['produto_id'], data['quantidade']))
        conn.commit()
        conn.close()
        return jsonify({'status': 'Compra registrada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para buscar todas as compras (GET)
@app.get('/compras', tags=[compra_tag])
def get_compras():
    """
    Busca todas as compras registradas.
    ---
    responses:
      200:
        description: Lista de compras encontrada com sucesso
      500:
        description: Erro interno ao buscar as compras
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM compras')
        compras = cursor.fetchall()
        conn.close()
        return jsonify(compras), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para deletar uma compra (DELETE)
@app.delete('/compras/<int:compra_id>', tags=[compra_tag])
def deletar_compra(compra_id):
    """
    Deleta uma compra registrada.
    ---
    parameters:
      - name: compra_id
        in: path
        type: integer
        required: true
        description: ID da compra a ser deletada
        example: 1
    responses:
      200:
        description: Compra deletada com sucesso
      404:
        description: Compra não encontrada
      500:
        description: Erro interno ao deletar a compra
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM compras WHERE id=?', (compra_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Compra não encontrada'}), 404
        conn.commit()
        conn.close()
        return jsonify({'status': 'Compra deletada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para atualizar uma compra (PUT)
@app.put('/compras/<int:compra_id>', tags=[compra_tag])
def atualizar_compra(compra_id):
    """
    Atualiza a quantidade de uma compra.
    ---
    parameters:
      - name: compra_id
        in: path
        type: integer
        required: true
        description: ID da compra a ser atualizada
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
                description: Nova quantidade para o produto
                example: 10
    responses:
      200:
        description: Compra atualizada com sucesso
      400:
        description: Erro no formato dos dados enviados
      404:
        description: Compra não encontrada
      500:
        description: Erro interno ao atualizar a compra
    """
    data = request.get_json()
    if not data or 'quantidade' not in data:
        return jsonify({'error': 'Formato de dados inválido'}), 400
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE compras SET quantidade=? WHERE id=?
        ''', (data['quantidade'], compra_id))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Compra não encontrada'}), 404
        conn.commit()
        conn.close()
        return jsonify({'status': 'Compra atualizada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002)