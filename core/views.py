from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Area, Trilha, ProgressoUsuario
from .serializers import AreaSerializer, TrilhaSerializer, ProgressoUsuarioSerializer
from .llm_service import LLMService
from django.views.decorators.csrf import csrf_exempt
import json

# ViewSet para o modelo Area.
# ReadOnlyModelViewSet cria automaticamente as ações de "apenas leitura":
# - `list`: para listar todas as áreas.
# - `retrieve`: para ver os detalhes de uma única área.
class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite que as áreas sejam visualizadas.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


# ViewSet para o modelo Trilha.
class TrilhaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite que as trilhas sejam visualizadas.
    """
    queryset = Trilha.objects.all()
    serializer_class = TrilhaSerializer


# ViewSet para o modelo ProgressoUsuario
class ProgressoUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite que o progresso dos usuários seja visualizado.
    """
    queryset = ProgressoUsuario.objects.all()
    serializer_class = ProgressoUsuarioSerializer

# Nova view para a página inicial/de acesso
def index_view(request):
    return render(request, 'index.html')


@csrf_exempt
@api_view(['POST'])
def gerar_trilha_llm(request):
    """
    API para gerar trilha personalizada usando LLM
    
    Recebe:
    {
        "area_interesse": "Desenvolvimento Web",
        "objetivos_usuario": "Trabalhar como desenvolvedor frontend",
        "experiencia_anterior": "Basico"
    }
    
    Retorna:
    {
        "titulo": "...",
        "descricao": "...",
        "etapas": [...]
    }
    """
    try:
        data = json.loads(request.body)
        area = data.get('area_interesse')
        objetivos = data.get('objetivos_usuario')
        experiencia = data.get('experiencia_anterior')
        
        if not area or not objetivos:
            return JsonResponse(
                {'erro': 'area_interesse e objetivos_usuario são obrigatórios'},
                status=400
            )
        
        llm_service = LLMService()
        trilha = llm_service.gerar_trilha_personalizada(area, objetivos, experiencia)
        
        return JsonResponse(trilha, safe=False)
    
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    except ValueError as e:
        return JsonResponse({'erro': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'erro': f'Erro ao gerar trilha: {str(e)}'}, status=500)