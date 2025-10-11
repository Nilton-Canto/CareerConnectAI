from rest_framework import viewsets
from .models import Area, Trilha, ProgressoUsuario
from .serializers import AreaSerializer, TrilhaSerializer, ProgressoUsuarioSerializer

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