#!/usr/bin/env bash
# Sai se der erro
set -o errexit

# Instala as bibliotecas
pip install -r requirements.txt

# Prepara o CSS para produção
python manage.py collectstatic --no-input

# Aplica migrações no banco de dados
python manage.py migrate

# Cria o superusuário automaticamente (se configurado)
python create_superuser.py