import uuid
from django.core.validators import MinValueValidator
from django.db import models
from transactions.validators import validate_revenue_category, validate_expense_category
from common.models import Bank, Category, PaymentMethod
from users.models import CustomUser

STATUS_CHOICES = [
    ('LATE', 'Atrasado'),
    ('PENDING', 'Em Aberto'),
    ('PAID', 'Pago'),
    ('OVERDUE', 'Vencido'),
    ('RECEIVED', 'Recebido'),
]


class FinancialBaseModel(models.Model):
    """
    Modelo base para transações financeiras.

    Attributes:
        payment_date (date): Data do pagamento/recebimento
        description (str): Descrição da transação
        value (decimal): Valor em reais
        status (str): Status da transação
        bank (FK): Banco relacionado
        observation (str): Observações adicionais
        user (FK): Usuário proprietário
        created_at (datetime): Data de criação
        updated_at (datetime): Data de atualização
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    payment_date = models.DateField(verbose_name='Data de pagamento')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Descrição')
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name='Valor (R$)')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='PENDING', verbose_name='Status')
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, verbose_name='Banco')
    observation = models.TextField(max_length=500, blank=True, null=True, verbose_name='Observação')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, verbose_name='Usuário')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class Revenue(FinancialBaseModel):
    """
    Modelo para receitas.

    Attributes:
        category (FK): Categoria do tipo receita
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        limit_choices_to={'type': 'REVENUE'},
        validators=[validate_revenue_category],
        verbose_name='Categoria'
    )

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
        ordering = ['-payment_date']

    def __str__(self):
        return f'{self.description or "Receita"} - R$ {self.value}'


class Expense(FinancialBaseModel):
    """
    Modelo para despesas.

    Attributes:
        category (FK): Categoria do tipo despesa
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        limit_choices_to={'type': 'EXPENSE'},
        validators=[validate_expense_category],
        verbose_name='Categoria'
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        verbose_name='Forma de pagamento'
    )

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
        ordering = ['-payment_date']

    def __str__(self):
        return f'{self.description or "Despesa"} - R$ {self.value}'
