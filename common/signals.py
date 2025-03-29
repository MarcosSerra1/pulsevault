from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from core.middleware import CURRENT_USER


@receiver(pre_save)
def set_user_on_save(sender, instance, **kwargs):
    """
    Signal thread-safe para associar usuário automaticamente.

    Usa contextvars para garantir isolamento entre requisições.
    """
    from .models import BaseModel
    if isinstance(instance, BaseModel) and not instance.user_id:
        user = CURRENT_USER.get()
        if user and user.is_authenticated:
            instance.user = user
        else:
            raise ValidationError('Usuário não encontrado no contexto atual')
