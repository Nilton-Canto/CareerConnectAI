from django.db import models

class Area(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome
