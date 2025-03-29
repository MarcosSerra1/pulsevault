#!/bin/bash

# Função para verificar falhas em comandos
check_command() {
    if [ $? -ne 0 ]; then
        echo "Erro na execução do comando: $1"
        exit 1
    fi
}

# Criar migrações
echo "🟡 Criando migrações..."
python manage.py makemigrations
check_command "makemigrations"

# Rodar migrações
echo "🟡 Rodando migrações..."
python manage.py migrate
check_command "migrações"

# Coletar Arquivos Staticos
echo "🟡 Coletando arquivos estaticos..."
python manage.py collectstatic --noinput

# Verificar e criar superusuário se necessário
echo "🟡 Verificando e criando superusuário se necessário..."
if [ -z "${DJANGO_SUPERUSER_EMAIL}" ] || [ -z "${DJANGO_SUPERUSER_PASSWORD}" ]; then
    echo "Erro: variáveis de ambiente do superusuário não estão definidas."
    exit 1
fi

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="${DJANGO_SUPERUSER_EMAIL}").exists():
    User.objects.create_superuser(
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
EOF
check_command "criação de superusuário"
echo "🟢 Superuser criado com sucesso"

# Iniciando o servidor gunicorn
echo "🟢 Iniciando servidor Gunicorn..."
gunicorn core.wsgi:application --bind 0.0.0.0:8000
check_command "início do servidor Gunicorn"
