from rest_framework import viewsets, permissions
from .models import Area
from .serializers import AreaSerializer

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all().order_by("id")
    serializer_class = AreaSerializer

    def get_permissions(self):
        # leitura pública; escrita exige autenticação
        if self.request.method in ["GET", "HEAD", "OPTIONS"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
