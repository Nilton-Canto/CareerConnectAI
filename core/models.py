from django.db import models
from django.conf import settings # Para referenciar nosso CustomUser

# Modelo para as áreas de carreira, como "Desenvolvimento Web", "Ciência de Dados", etc.
class Area(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

# Modelo para uma trilha de carreira específica.
class Trilha(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='trilhas')

    def __str__(self):
        return self.titulo

# Modelo para cada etapa/passo dentro de uma trilha.
class Etapa(models.Model):
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE, related_name='etapas')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ordem = models.PositiveIntegerField() # Para definir a sequência das etapas

    class Meta:
        # Garante que a ordem seja única para cada trilha
        ordering = ['ordem']

    def __str__(self):
        return f'{self.trilha.titulo} - Etapa {self.ordem}: {self.titulo}'

# Modelo para rastrear o progresso de cada usuário.
class ProgressoUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trilha_selecionada = models.ForeignKey(Trilha, on_delete=models.SET_NULL, null=True, blank=True)
    etapas_concluidas = models.ManyToManyField(Etapa, blank=True)

    def __str__(self):
        return f'Progresso de {self.usuario.email}'