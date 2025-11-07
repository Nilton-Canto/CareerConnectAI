from django.contrib import admin
from .models import Area, Trilha, Etapa, ProgressoUsuario

# 1. Define um "Editor Inline" para as Etapas 
# Isso permite que as etapas sejam editadas DENTRO da página da Trilha
class EtapaInline(admin.TabularInline):
    model = Etapa
    extra = 1 # Quantos campos de etapa em branco devem aparecer por padrão

# 2. Cria uma Classe de Admin Customizada para a Trilha 
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'area') # Colunas que aparecem na lista de trilhas
    search_fields = ['titulo', 'descricao'] # Adiciona uma barra de busca
    inlines = [EtapaInline] # <<< CONECTA O EDITOR DE ETAPAS AQUI

# 3. Registra os Modelos (agora usando a classe customizada) 
admin.site.register(Area)
admin.site.register(Trilha, TrilhaAdmin) # Usa a nova classe TrilhaAdmin
admin.site.register(ProgressoUsuario)
admin.site.register(Etapa) # Mantemos o registro da Etapa separado também