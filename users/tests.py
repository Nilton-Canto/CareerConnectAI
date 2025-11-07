from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginAPITests(APITestCase):
    def setUp(self):
        self.email = 'testuser@exemplo.com'
        self.password = 'senhaSuperForte123'
        self.user = User.objects.create_user(username='testuser', email=self.email, password=self.password)
        self.login_url = reverse('api_login') 

    def test_login_sucesso(self):
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    def test_login_senha_incorreta(self):
        data = {'email': self.email, 'password': 'senhaErrada'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.json())
        
    def test_login_metodo_get_nao_permitido(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# testes novos para criação do usuário

class CadastroAPITests(APITestCase):
    
    def setUp(self):
        self.cadastro_url = reverse('api_cadastro')
        # Dados válidos para usar nos testes
        self.valid_payload = {
            'email': 'novousuario@teste.com',
            'password': 'SenhaForte123!',
            'password_confirm': 'SenhaForte123!'
        }

    def test_cadastro_sucesso(self):
        """Testa se é possível cadastrar um novo usuário com dados válidos"""
        response = self.client.post(self.cadastro_url, self.valid_payload, format='json')
        
        # Espera 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verifica se o usuário foi realmente criado no banco de dados
        self.assertTrue(User.objects.filter(email='novousuario@teste.com').exists())

    def test_cadastro_senhas_nao_conferem(self):
        """Testa se o cadastro falha quando as senhas são diferentes"""
        payload = self.valid_payload.copy()
        payload['password_confirm'] = 'SenhaDiferente!'
        
        response = self.client.post(self.cadastro_url, payload, format='json')
        
        # Espera 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('As senhas não coincidem', response.json()['message'])

    def test_cadastro_email_ja_existente(self):
        """Testa se o cadastro falha ao tentar usar um email já cadastrado"""
        # Primeiro, cria um usuário
        User.objects.create_user(username='antigo', email='novousuario@teste.com', password='pwd')
        
        # Tenta criar outro com o mesmo email
        response = self.client.post(self.cadastro_url, self.valid_payload, format='json')
        
        # Espera 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Este email já está cadastrado', response.json()['message'])