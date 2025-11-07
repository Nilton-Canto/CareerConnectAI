from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch # Importe a ferramenta de simulação 'patch'

class LLM_APITests(APITestCase):

    def setUp(self):
        # O endereço da nossa API
        self.url = reverse('gerar_trilha_llm') 

    # 1. O Decorador Mágico
    # Esta linha intercepta qualquer tentativa de usar o 'LLMService'
    # e o substitui por um "dublê" (mock_llm_service).
    @patch('core.views.LLMService')
    def test_gerar_trilha_sucesso(self, mock_llm_service_constructor):
        """
        Testa se a API retorna 200 OK e os dados simulados
        quando a chamada é bem-sucedida.
        """
        
        # 2. Configurando o Dublê
        # Criamos os dados falsos que queremos que a IA "retorne"
        fake_trilha = {
            "titulo": "Trilha Falsa de Teste",
            "descricao": "Esta trilha foi gerada por um mock.",
            "etapas": [{"titulo": "Etapa Mock 1", "descricao": "..."}]
        }
        
        # Configuramos o "dublê" para retornar nossos dados falsos
        # .return_value é usado duas vezes para simular:
        # 1º: A criação da instância (LLMService())
        # 2º: A chamada do método (gerar_trilha_personalizada(...))
        mock_llm_service_constructor.return_value.gerar_trilha_personalizada.return_value = fake_trilha

        # 3. Os Dados da Requisição
        data = {
            "area_interesse": "Teste",
            "objetivos_usuario": "Passar no teste"
        }

        # 4. A Chamada da API
        # A view vai rodar, mas em vez de chamar o Gemini,
        # ela vai chamar nosso "dublê" e obter a 'fake_trilha'.
        response = self.client.post(self.url, data, format='json')

        # 5. As Verificações
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['titulo'], "Trilha Falsa de Teste")
        self.assertEqual(len(response.json()['etapas']), 1)

    def test_gerar_trilha_bad_request(self):
        """
        Testa se a API falha corretamente (400) se os dados
        obrigatórios não forem enviados.
        """
        
        # Dados inválidos (sem 'area_interesse' e 'objetivos_usuario')
        data = {
            "experiencia_anterior": "Nenhuma"
        }
        
        # Este teste NÃO usa mock, pois a falha deve acontecer
        # na validação da view, antes mesmo de chamar o LLMService.
        response = self.client.post(self.url, data, format='json')
        
        # Verifica se o servidor retornou um erro 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('erro', response.json())