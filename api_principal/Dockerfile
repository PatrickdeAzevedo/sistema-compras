# Dockerfile para o Componente A
# Usando a imagem base do Python 3.9
FROM python:3.9

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo de dependências para o container
COPY requirements.txt .

# Instalando as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U flask-openapi3-swagger

# Copiando o código-fonte da aplicação para o container
COPY app.py .

# Expondo a porta 5000 para acessar a API Principal
EXPOSE 5000

# Definindo o comando para iniciar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

