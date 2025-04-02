import unicodedata
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _

# Constantes
MIN_LENGTH = 8
SPECIAL_CHARACTERS = '!@#$%^&*()-_=+[]{}|;:,.<>?/'
MIN_PART_LENGTH = 2

# Mensagens de erro
MESSAGES = {
    'length': _('A senha deve ter pelo menos 8 caracteres.'),
    'uppercase': _('A senha deve conter pelo menos uma letra maiúscula.'),
    'lowercase': _('A senha deve conter pelo menos uma letra minúscula.'),
    'number': _('A senha deve conter pelo menos um número.'),
    'special': _('A senha deve conter ao menos um caractere especial.'),
    'email': _('A senha não pode conter partes do seu email.'),
    'name': _('A senha não pode conter partes do seu nome.'),
    'current': _('A senha não deve ser igual à senha atual.'),
    'previous': _('A senha não deve ser igual à senha anterior.')
}


def normalize_string(text):
    """
    Remove acentos e converte para minúsculo.

    Args:
        text (str): Texto a ser normalizado

    Returns:
        str: Texto normalizado, sem acentos e em minúsculo
    """
    if not text:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()


def validate_basic_requirements(password):
    """
    Valida requisitos básicos da senha.

    Args:
        password (str): Senha a ser validada

    Raises:
        ValidationError: Se a senha não atender aos requisitos básicos
    """
    if len(password) < MIN_LENGTH:
        raise ValidationError(MESSAGES['length'])

    if not any(c.isupper() for c in password):
        raise ValidationError(MESSAGES['uppercase'])

    if not any(c.islower() for c in password):
        raise ValidationError(MESSAGES['lowercase'])

    if not any(c.isdigit() for c in password):
        raise ValidationError(MESSAGES['number'])

    if not any(c in SPECIAL_CHARACTERS for c in password):
        raise ValidationError(MESSAGES['special'])


def validate_email_parts(password_normalized, user):
    """
    Valida se a senha contém partes do email.

    Args:
        password_normalized (str): Senha normalizada.
        user: Usuário com o email a ser verificado.

    Raises:
        ValidationError: Se a senha contiver partes do email.
    """
    if not user.email:
        return

    email_normalized = normalize_string(user.email)
    # Extrai as partes do username (antes do @)
    username = email_normalized.split('@')[0]
    email_parts = [part for part in username.split('.') if len(part) > MIN_PART_LENGTH] + [username]

    # Extrai as partes do domínio (depois do @)
    if '@' in email_normalized:
        domain = email_normalized.split('@')[1]
        email_parts += [part for part in domain.split('.') if len(part) > MIN_PART_LENGTH]

    for part in email_parts:
        if len(part) > MIN_PART_LENGTH and part in password_normalized:
            raise ValidationError(MESSAGES['email'])


def validate_name_parts(password_normalized, user):
    """
    Valida se a senha contém partes do nome.

    Args:
        password_normalized (str): Senha normalizada
        user: Usuário com o nome a ser verificado

    Raises:
        ValidationError: Se a senha contiver partes do nome
    """
    if not user.name:
        return

    name_parts = [
        normalize_string(part)
        for part in user.name.split()
        if len(part) > MIN_PART_LENGTH
    ]

    for part in name_parts:
        if part in password_normalized:
            raise ValidationError(MESSAGES['name'])


def validate_previous_passwords(password, user):
    """
    Valida se a senha é igual à atual ou anterior.

    Args:
        password (str): Senha a ser validada
        user: Usuário com as senhas a serem verificadas

    Raises:
        ValidationError: Se a senha for igual à atual ou anterior
    """
    if not user or not user.pk:
        return

    if user.check_password(password):
        raise ValidationError(MESSAGES['current'])

    if (user.previous_password_hash and check_password(password, user.previous_password_hash)):
        raise ValidationError(MESSAGES['previous'])


def validate_password(password, user=None):
    """
    Valida a força da senha.

    Args:
        password (str): Senha a ser validada
        user: Usuário associado à senha (opcional)

    Raises:
        ValidationError: Se a senha não atender aos critérios de força
    """
    # Validações básicas primeiro
    validate_basic_requirements(password)

    # Validações que dependem do usuário
    if user:
        password_normalized = normalize_string(password)

        # Valida senhas anteriores primeiro
        validate_previous_passwords(password, user)

        # Valida partes do email e nome
        validate_email_parts(password_normalized, user)
        validate_name_parts(password_normalized, user)
