from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from .models import Area, Trilha, ProgressoUsuario, Etapa
from .serializers import AreaSerializer, TrilhaSerializer, ProgressoUsuarioSerializer
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
class ProgressoUsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que o progresso dos usuários seja visualizado e modificado.
    """
    queryset = ProgressoUsuario.objects.all()
    serializer_class = ProgressoUsuarioSerializer
    
    # Define que esta view requer autenticação por token
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Garante que os usuários só possam ver seu próprio progresso.
        """
        return ProgressoUsuario.objects.filter(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_etapa_concluida(self, request, pk=None):
        """
        Ação customizada para marcar uma etapa como concluída.
        O front-end enviará: {"etapa_id": 123}
        """
        progresso = self.get_object() # Pega o progresso do usuário logado
        etapa_id = request.data.get('etapa_id')

        if not etapa_id:
            return Response({'erro': 'ID da etapa não fornecido.'}, status=400)

        try:
            etapa = Etapa.objects.get(id=etapa_id)
            progresso.etapas_concluidas.add(etapa)
            progresso.save()
            return Response({'status': f'Etapa {etapa.titulo} marcada como concluída.'}, status=200)
        except Etapa.DoesNotExist:
            return Response({'erro': 'Etapa não encontrada.'}, status=404)
        except Exception as e:
            return Response({'erro': str(e)}, status=500)

# Nova view para a página inicial/de acesso
def index_view(request):
    return render(request, 'index.html')


