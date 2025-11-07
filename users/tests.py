# Em users/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# Pega o nosso modelo CustomUser
User = get_user_model()

class LoginAPITests(APITestCase):

    def setUp(self):
        """
        Configuração inicial que roda antes de cada teste.
        Cria um usuário de teste no banco de dados.
        """
        self.email = 'testuser@exemplo.com'
        self.password = 'senhaSuperForte123'
        
        self.user = User.objects.create_user(
            username='testuser', 
            email=self.email, 
            password=self.password
        )
        
        # Esta é a URL que configuramos no users/urls.py
        self.login_url = reverse('api_login') 

    def test_login_sucesso(self):
        """
        Testa se o login com credenciais corretas retorna 200 OK e um token.
        """
        data = {
            'email': self.email,
            'password': self.password
        }
        
        # Simula uma chamada de API POST para a nossa view de login
        response = self.client.post(self.login_url, data, format='json')
        
        # Verificação 1: O status da resposta foi 200 OK?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificação 2: A resposta JSON contém a chave 'token'?
        self.assertIn('token', response.json())

    def test_login_senha_incorreta(self):
        """
        Testa se o login com senha errada retorna 401 Unauthorized.
        """
        data = {
            'email': self.email,
            'password': 'senhaErrada'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        # Verificação 1: O status da resposta foi 401?
        # (Nossa view retorna 401 para credenciais inválidas)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verificação 2: A resposta NÃO contém um token?
        self.assertNotIn('token', response.json())
        
    def test_login_metodo_get_nao_permitido(self):
        """
        Testa se uma requisição GET (não permitida) retorna 405.
        """
        response = self.client.get(self.login_url)
        
        # Verificação 1: O status da resposta foi 405?
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)