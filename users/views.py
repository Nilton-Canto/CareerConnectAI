from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

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
                return JsonResponse({'message': 'Login realizado com sucesso!'}, status=200)
            else:
                # Se as credenciais forem inválidas
                return JsonResponse({'message': 'Email ou senha inválidos.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Dados inválidos.'}, status=400)

    # Se a requisição não for POST
    return JsonResponse({'message': 'Método não permitido.'}, status=405)