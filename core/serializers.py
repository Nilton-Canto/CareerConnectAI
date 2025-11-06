# Em core/serializers.py

from rest_framework import serializers
from .models import Area, Trilha, Etapa, ProgressoUsuario

# Serializer para o modelo mais simples: Etapa
class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        # Define quais campos do modelo serão convertidos para JSON
        fields = ['id', 'titulo', 'descricao', 'ordem']


# Serializer para o modelo Trilha.
# Note que ele usa o EtapaSerializer para aninhar as etapas dentro de cada trilha.
class TrilhaSerializer(serializers.ModelSerializer):
    # 'etapas' é o related_name que definimos no modelo Etapa
    etapas = EtapaSerializer(many=True, read_only=True)

    class Meta:
        model = Trilha
        fields = ['id', 'titulo', 'descricao', 'area', 'etapas']


# Serializer para o modelo Area, que aninha as trilhas relacionadas a ela.
class AreaSerializer(serializers.ModelSerializer):
    # 'trilhas' é o related_name que definimos no modelo Trilha
    trilhas = TrilhaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'nome', 'trilhas']


# Serializer para o progresso do usuário.
# Ele mostra os IDs das etapas concluídas para ser mais eficiente.
class ProgressoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressoUsuario
        fields = ['id', 'usuario', 'trilha_selecionada', 'etapas_concluidas']