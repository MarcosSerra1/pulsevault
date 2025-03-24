# Imagem base do Python 3.12 (slim)
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema operacional 
RUN apt-get update && apt-get install -y curl

# Copia o script wait-for-it.sh para o container
COPY /scripts/wait-for-it.sh /app/
COPY /scripts/entrypoint.sh /app/

# Atribui permissão de execução para o wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/entrypoint.sh

# Copia o arquivo requirements.txt com as dependências do projeto
COPY requirements.txt /app/

# Instala as dependências Python do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o container
COPY . /app/

# Expõe a porta 8000
EXPOSE 8000
