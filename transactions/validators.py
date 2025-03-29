from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from common.models import Category


def validate_revenue_category(category_id):
    """
    Valida se a categoria é do tipo receita.

    Args:
        category_id: ID da categoria selecionada

    Raises:
        ValidationError: Se a categoria não for do tipo receita
    """
    try:
        category = Category.objects.get(id=category_id)
        if category.type != 'REVENUE':
            raise ValidationError(
                _('%(category)s não é uma categoria de receita válida'),
                params={'category': category.name},
            )
    except Category.DoesNotExist:
        raise ValidationError(_('Categoria não encontrada'))


def validate_expense_category(category_id):
    """
    Valida se a categoria é do tipo despesa.

    Args:
        category_id: ID da categoria selecionada

    Raises:
        ValidationError: Se a categoria não for do tipo despesa
    """
    try:
        category = Category.objects.get(id=category_id)
        if category.type != 'EXPENSE':
            raise ValidationError(
                _('%(category)s não é uma categoria de despesa válida'),
                params={'category': category.name},
            )
    except Category.DoesNotExist:
        raise ValidationError(_('Categoria não encontrada'))
