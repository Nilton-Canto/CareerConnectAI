import os
import django
from django.contrib.auth import get_user_model

# Configura o ambiente do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerconnectai.settings")
django.setup()

User = get_user_model()

def create_superuser():
    # Pega os dados das variáveis de ambiente do Render
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if username and password:
        if not User.objects.filter(username=username).exists():
            print(f"Criando superusuário: {username}...")
            User.objects.create_superuser(username=username, email=email, password=password)
            print("Superusuário criado com sucesso!")
        else:
            print("Superusuário já existe. Nenhuma ação necessária.")
    else:
        print("Variáveis de ambiente de superusuário não encontradas. Pular criação.")

if __name__ == "__main__":
    create_superuser()