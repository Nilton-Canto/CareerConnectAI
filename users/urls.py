from django.urls import path
from . import views

urlpatterns = [
    # Path para a API que recebe os dados do formulário (POST)
    path('api/login', views.login_view, name='api_login'),

    # Path para a PÁGINA de login que o usuário vê (GET)  <-- ADICIONE ESTA LINHA
    path('login/', views.login_page_view, name='login_page'),
]