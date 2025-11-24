from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Cria um roteador
router = DefaultRouter()

# Registra nossas ViewSets com o roteador
router.register(r'areas', views.AreaViewSet, basename='area')
router.register(r'trilhas', views.TrilhaViewSet, basename='trilha')
router.register(r'progressos', views.ProgressoUsuarioViewSet, basename='progresso')

# As URLs da API são determinadas automaticamente pelo roteador
urlpatterns = [
    path('', include(router.urls)),
    path('llm/gerar-trilha/', views.gerar_trilha_llm, name='gerar_trilha_llm'),
]