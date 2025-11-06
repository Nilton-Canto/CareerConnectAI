from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import CustomUser
import json
from rest_framework.authtoken.models import Token

@csrf_exempt # Use para desenvolvimento, para produção pesquise sobre autenticação por token
def login_view(request):
    # Garante que a requisição é do tipo POST
    if request.method == 'POST':
        try:
            # Carrega os dados JSON do corpo da requisição
            data = json.loads(request.body)
            email = data.get('email') # O frontend envia 'email'
            password = data.get('password')

            # O sistema de autenticação do Django usa 'username'.
            # Vamos usar o email como username aqui.
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Se o usuário for autenticado com sucesso, cria a sessão
                login(request, user)
                # Encontre ou crie um token para este usuário
                token, created = Token.objects.get_or_create(user=user)
                # Retorne o token no JSON
                return JsonResponse({'message': 'Login realizado com sucesso!', 'token': token.key}, status=200)
            else:
                # Se as credenciais forem inválidas
                return JsonResponse({'message': 'Email ou senha inválidos.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Dados inválidos.'}, status=400)

    # Se a requisição não for POST
    return JsonResponse({'message': 'Método não permitido.'}, status=405)


# Nova view para exibir a página de login HTML
def login_page_view(request):
    # Esta função simplesmente renderiza e retorna o template login.html
    return render(request, 'login.html')

# Nova view para exibir a página de dashboard
def dashboard_view(request):
    # Esta função renderiza e retorna o template dashboard.html
    return render(request, 'dashboard.html')


@csrf_exempt
def cadastro_view(request):
    """API para cadastro de novos usuários"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            username = data.get('username', email.split('@')[0])  # Se não fornecer username, usa parte do email
            password = data.get('password')
            password_confirm = data.get('password_confirm')
            
            # Validações básicas
            if not email or not password:
                return JsonResponse({'message': 'Email e senha são obrigatórios.'}, status=400)
            
            if password != password_confirm:
                return JsonResponse({'message': 'As senhas não coincidem.'}, status=400)
            
            # Verifica se o usuário já existe
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Este email já está cadastrado.'}, status=400)
            
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Este nome de usuário já está em uso.'}, status=400)
            
            # Valida a senha
            try:
                validate_password(password)
            except ValidationError as e:
                return JsonResponse({'message': 'Senha inválida: ' + ', '.join(e.messages)}, status=400)
            
            # Cria o usuário
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({'message': 'Usuário cadastrado com sucesso!'}, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Dados inválidos.'}, status=400)
    
    return JsonResponse({'message': 'Método não permitido.'}, status=405)


def cadastro_page_view(request):
    """Renderiza a página HTML de cadastro"""
    return render(request, 'cadastro.html')