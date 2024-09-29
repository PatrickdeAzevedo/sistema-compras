# Sistema de Compras com Microsserviços
* **MVP da Disciplina Desenvolvimento Back-End Avançado da PUC-Rio**
* Projeto desenvolvido por **Patrick de Azevedo**, [patrickdezevedo@gmail.com](mailto:patrickdeazevedo@gmail.com)
* **OBS.: Trata-se de um README.md que engloba a documentação completa de todos os Componentes A, B e C**

## Visão Geral do Projeto

Este projeto é uma aplicação de compras baseada em uma arquitetura de microsserviços que utiliza comunicação via REST API entre três componentes principais:

1. **API Principal (Componente A)**: Serve como ponto central da aplicação, responsável por gerenciar as operações de compra e consultar informações de produtos usando um serviço externo.
2. **API Externa (Componente B)**: Interage com a [FakeStore API](https://fakestoreapi.com/) para buscar detalhes de produtos e repassar informações ao Componente A.
3. **API de Dados (Componente C)**: Gerencia um banco de dados SQLite para registrar, consultar e modificar informações de pedidos de compras.

A arquitetura segue um padrão modular e é containerizada usando Docker, facilitando a implantação e a escalabilidade dos serviços.

![Arquitetura do Sistema](MVP%20BACKEND%20-%20PATRICK%20-%20PUCRIO.png)

## Componentes

### API Principal (Componente A)

- **Descrição**: Gerencia a criação e atualização de pedidos de compra.
- **Rotas Implementadas**:
  - `GET /status`: Retorna o status do serviço.
  - `POST /comprar`: Cria um novo pedido de compra.
  - `GET /produto/<produto_id>`: Busca detalhes de um produto pelo ID.
  - `DELETE /pedido/<pedido_id>`: Remove um pedido de compra.
  - `PUT /pedido/<pedido_id>`: Atualiza a quantidade de produtos em um pedido.

### API Externa (Componente B)

- **Descrição**: Interage com a FakeStore API para obter informações de produtos.
- **API Utilizada**: [FakeStore API](https://fakestoreapi.com/)
- **Rotas Usadas**:
  - `GET /products`: Retorna todos os produtos disponíveis.
  - `GET /products/<id>`: Retorna os detalhes de um produto específico pelo ID.
- **Licença de Uso**: A FakeStore API é de uso livre, não requer cadastro para acessar os dados.

### API de Dados (Componente C)

- **Descrição**: Gerencia um banco de dados SQLite para registrar pedidos de compra.
- **Rotas Implementadas**:
  - `POST /compras`: Cria um novo registro de compra.
  - `GET /compras`: Retorna todas as compras registradas.
  - `DELETE /compras/<compra_id>`: Remove um pedido do banco de dados.
  - `PUT /compras/<compra_id>`: Atualiza a quantidade de um pedido no banco.

## Pré-requisitos

Para executar este projeto localmente, você precisará ter instalado:

- [Python 3.8+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- `venv` para gerenciamento de ambiente virtual Python.

## Configuração do Ambiente Local

### 1. Clonar o Repositório

```bash
git clone https://github.com/PatrickdeAzevedo/sistema-compras.git
cd sistema-compras
```

### 2. Configurar e Ativar o Ambiente Virtual para cada Componente
Mover-se pelas pastas através do comando `cd` e em cada pasta criar um ambiente virtual:
```bash
cd api_principal
cd ..\componente_b
cd ..\componente_c
```

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Windows)
venv\Scripts\activate

# Ativar o ambiente virtual (Linux/Mac)
source venv/bin/activate
```
**OBS.: No Windows, se der erro, tem que ser executado no PowerShell como administrador o comando: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned**

### 3. Instalar Dependências
Entre em cada pasta de componente (`api_principal`, `componente_b`, `componente_c`) e instale as dependências:

```bash
cd api_principal
pip install -r requirements.txt

cd ../componente_b
pip install -r requirements.txt

cd ../componente_c
pip install -r requirements.txt
```

Conteúdo recomendado para o arquivo `requirements.txt` de cada um dos componentes, com as bibliotecas necessárias para que os serviços funcionem corretamente:
**OBS.: se não funcionar, retirar as versões das bibliotecas e rodar de novo o pip install.**

`api_principal/requirements.txt` (Componente A)
```bash
flask==2.2.2
flask-openapi3==1.0.2
flask-cors=5.0.0
requests==2.32.3
```

`componente_b/requirements.txt` (Componente B)
```bash
flask==2.2.2
flask-openapi3==1.0.2
flask-cors==5.0.0
requests==2.32.3
```

`componente_c/requirements.txt` (Componente C)
```bash
flask==2.2.2
flask-openapi3==1.0.2
flask-cors==5.0.0
requests==2.32.3
```

### 4. Executar Localmente com Flask
Execute cada componente em um terminal separado:

**API Principal (Componente A)**
```bash
cd api_principal
flask run --host=0.0.0.0 --port=5000
```

**API Externa (Componente B)**
```bash
cd componente_b
flask run --host=0.0.0.0 --port=5001
```

**API de Dados (Componente C)**
```bash
cd componente_c
flask run --host=0.0.0.0 --port=5002
```

Após iniciar todos os componentes, a API estará disponível nos seguintes endpoints:

- **API Principal**: http://localhost:5000
- **API Externa**: http://localhost:5001
- **API de Dados**: http://localhost:5002

### 5. Executar com Docker
**Construir e Iniciar os Containers**
No diretório raiz, onde está o `docker-compose.yml`, execute:
```bash
docker-compose up --build
```

**Parar e Remover os Containers**
```bash
docker-compose down
```

### 6. Estrutura de Diretórios
A estrutura dos diretórios do projeto segue a organização:
```bash
sistema-compras/
├── api_principal/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── componente_b/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── componente_c/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml
```

### Testando a API
Após iniciar os componentes, você pode testar as rotas usando o `Swagger UI` (para a API Principal) ou ferramentas como o `Postman` para verificar a comunicação entre os serviços.