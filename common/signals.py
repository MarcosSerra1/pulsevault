from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.core.exceptions import ValidationError
from threading import local

_thread_locals = local()


def set_current_user(user):
    """Armazena o usuário atual no thread local"""
    _thread_locals.user = user


def get_current_user():
    """Recupera o usuário atual do thread local"""
    return getattr(_thread_locals, 'user', None)


@receiver(pre_save)
def set_user_on_save(sender, instance, **kwargs):
    """
    Signal que associa automaticamente o usuário logado ao objeto sendo salvo.

    Attributes:
        sender: Modelo que está sendo salvo
        instance: Instância do objeto sendo salvo
        **kwargs: Argumentos adicionais
    """
    # Verifica se o modelo herda de BaseModel e não tem usuário definido
    from .models import BaseModel
    if isinstance(instance, BaseModel) and not instance.user_id:
        user = get_current_user()
        if user:
            instance.user = user
        else:
            raise ValidationError('Nenhum usuário logado encontrado')
