# Sistema de Compras com Microsserviços

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
