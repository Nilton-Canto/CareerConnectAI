from django.urls import path
from . import views

urlpatterns = [
    # Path para a API que recebe os dados do formulário (POST)
    path('api/login', views.login_view, name='api_login'),
    path('api/cadastro', views.cadastro_view, name='api_cadastro'),

    # Path para a PÁGINA de login que o usuário vê (GET)
    path('login/', views.login_page_view, name='login_page'),
    
    # Path para a PÁGINA de cadastro
    path('cadastro/', views.cadastro_page_view, name='cadastro_page'),

    # Path para a PÁGINA de dashboard (GET)
    path('dashboard/', views.dashboard_view, name='dashboard'),
]