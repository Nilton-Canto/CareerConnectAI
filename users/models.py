from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Faz o campo email ser obrigatório e único para cada usuário
    email = models.EmailField(unique=True)

    # Define que o campo de LOGIN será o 'email'
    USERNAME_FIELD = 'email'

    # Remove 'email' dos campos requeridos ao criar um superusuário,
    # pois ele já é o USERNAME_FIELD
    REQUIRED_FIELDS = ['username'] # Você pode até remover o username se quiser

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set", # Nome único para o acesso reverso
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set", # Nome único para o acesso reverso
        related_query_name="user",
    )
    
    def __str__(self):
        return self.email