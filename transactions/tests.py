from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import CustomUser
from common.models import Bank, Category, PaymentMethod
from .models import Revenue, Expense


class TransactionsBaseTestCase(TestCase):
    """Classe base para testes de transações"""

    def setUp(self):
        """Configura dados iniciais para os testes"""
        # Cria usuários
        self.user1 = CustomUser.objects.create_user(
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = CustomUser.objects.create_user(
            email='user2@test.com',
            password='testpass123'
        )

        # Cria bancos
        self.bank1 = Bank.objects.create(
            name='Banco 1',
            code='001',
            user=self.user1
        )
        self.bank2 = Bank.objects.create(
            name='Banco 2',
            code='002',
            user=self.user2
        )

        # Cria categorias
        self.revenue_category = Category.objects.create(
            name='Salário',
            type='REVENUE',
            user=self.user1
        )
        self.expense_category = Category.objects.create(
            name='Alimentação',
            type='EXPENSE',
            user=self.user1
        )

        # Cria forma de pagamento
        self.payment_method = PaymentMethod.objects.create(
            name='Cartão de Crédito',
            user=self.user1
        )

        # Data padrão para testes
        self.today = timezone.now().date()


class RevenueModelTests(TransactionsBaseTestCase):
    """Testes para o modelo Revenue"""

    def test_create_revenue(self):
        """Testa criação básica de receita"""
        revenue = Revenue.objects.create(
            payment_date=self.today,
            description='Salário Mensal',
            value=Decimal('5000.00'),
            status='RECEIVED',
            bank=self.bank1,
            category=self.revenue_category,
            user=self.user1
        )
        self.assertEqual(revenue.value, Decimal('5000.00'))
        self.assertEqual(revenue.status, 'RECEIVED')

    def test_invalid_value(self):
        """Testa validação de valor negativo"""
        revenue = Revenue(
            payment_date=self.today,
            value=Decimal('-100.00'),
            bank=self.bank1,
            category=self.revenue_category,
            user=self.user1
        )
        with self.assertRaises(ValidationError):
            revenue.full_clean()

    def test_invalid_category(self):
        """Testa validação de categoria incorreta"""
        revenue = Revenue(
            payment_date=self.today,
            value=Decimal('100.00'),
            bank=self.bank1,
            category=self.expense_category,  # Categoria de despesa
            user=self.user1
        )
        with self.assertRaises(ValidationError):
            revenue.full_clean()

    def test_str_representation(self):
        """Testa representação string do modelo"""
        revenue = Revenue.objects.create(
            payment_date=self.today,
            description='Freelance',
            value=Decimal('1000.00'),
            bank=self.bank1,
            category=self.revenue_category,
            user=self.user1
        )
        self.assertEqual(str(revenue), 'Freelance - R$ 1000.00')

        # Testa sem descrição
        revenue = Revenue.objects.create(
            payment_date=self.today,
            value=Decimal('1000.00'),
            bank=self.bank1,
            category=self.revenue_category,
            user=self.user1
        )
        self.assertEqual(str(revenue), 'Receita - R$ 1000.00')


class ExpenseModelTests(TransactionsBaseTestCase):
    """Testes para o modelo Expense"""

    def test_create_expense(self):
        """Testa criação básica de despesa"""
        expense = Expense.objects.create(
            payment_date=self.today,
            description='Supermercado',
            value=Decimal('500.00'),
            status='PAID',
            bank=self.bank1,
            category=self.expense_category,
            payment_method=self.payment_method,
            user=self.user1
        )
        self.assertEqual(expense.value, Decimal('500.00'))
        self.assertEqual(expense.status, 'PAID')

    def test_invalid_value(self):
        """Testa validação de valor negativo"""
        expense = Expense(
            payment_date=self.today,
            value=Decimal('-50.00'),
            bank=self.bank1,
            category=self.expense_category,
            payment_method=self.payment_method,
            user=self.user1
        )
        with self.assertRaises(ValidationError):
            expense.full_clean()

    def test_invalid_category(self):
        """Testa validação de categoria incorreta"""
        expense = Expense(
            payment_date=self.today,
            value=Decimal('50.00'),
            bank=self.bank1,
            category=self.revenue_category,  # Categoria de receita
            payment_method=self.payment_method,
            user=self.user1
        )
        with self.assertRaises(ValidationError):
            expense.full_clean()

    def test_str_representation(self):
        """Testa representação string do modelo"""
        expense = Expense.objects.create(
            payment_date=self.today,
            description='Internet',
            value=Decimal('100.00'),
            bank=self.bank1,
            category=self.expense_category,
            payment_method=self.payment_method,
            user=self.user1
        )
        self.assertEqual(str(expense), 'Internet - R$ 100.00')

        # Testa sem descrição
        expense = Expense.objects.create(
            payment_date=self.today,
            value=Decimal('100.00'),
            bank=self.bank1,
            category=self.expense_category,
            payment_method=self.payment_method,
            user=self.user1
        )
        self.assertEqual(str(expense), 'Despesa - R$ 100.00')


class FinancialBaseModelTests(TransactionsBaseTestCase):
    """Testes para campos e validações comuns"""

    def test_required_fields(self):
        """Testa campos obrigatórios"""
        with self.assertRaises(ValidationError):
            revenue = Revenue(
                description='Teste',  # Sem data e valor
                bank=self.bank1,
                category=self.revenue_category,
                user=self.user1
            )
            revenue.full_clean()

    def test_status_choices(self):
        """Testa escolhas de status válidas"""
        revenue = Revenue.objects.create(
            payment_date=self.today,
            value=Decimal('100.00'),
            status='PENDING',
            bank=self.bank1,
            category=self.revenue_category,
            user=self.user1
        )
        self.assertEqual(revenue.status, 'PENDING')

        with self.assertRaises(ValidationError):
            revenue.status = 'INVALID'
            revenue.full_clean()
