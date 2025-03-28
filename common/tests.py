from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from users.models import CustomUser
from .models import Category, Bank, PaymentMethod


class BaseTestCase(TestCase):
    """Classe base para testes"""
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            email='user1@test.com',
            password='testpass123'
        )
        self.user2 = CustomUser.objects.create_user(
            email='user2@test.com',
            password='testpass123'
        )


class CategoryTests(BaseTestCase):
    """Testes para o modelo Category"""
    def test_create_category(self):
        """Testa criação básica de categoria"""
        category = Category.objects.create(
            name='Casa',
            type='EXPENSE',
            user=self.user1
        )
        self.assertEqual(category.name, 'Casa')
        self.assertEqual(category.type, 'EXPENSE')
        self.assertEqual(category.slug, 'casa-expense')  # Atualizado

    def test_duplicate_category_different_users(self):
        """Testa que permite mesma categoria para usuários diferentes"""
        cat1 = Category.objects.create(
            name='Casa',
            type='EXPENSE',
            user=self.user1
        )
        cat2 = Category.objects.create(
            name='Casa',
            type='EXPENSE',
            user=self.user2
        )
        self.assertEqual(cat1.name, cat2.name)
        self.assertEqual(cat1.type, cat2.type)
        self.assertNotEqual(cat1.user, cat2.user)
        self.assertEqual(cat1.slug, 'casa-expense')  # Atualizado
        self.assertEqual(cat2.slug, 'casa-expense-1')  # Atualizado

    def test_slug_generation(self):
        """Testa geração de slugs únicos"""
        # Primeira categoria
        cat1 = Category.objects.create(
            name='Casa',
            type='EXPENSE',
            user=self.user1
        )
        self.assertEqual(cat1.slug, 'casa-expense')  # Atualizado

        # Segunda categoria - mesmo nome, tipo diferente
        cat2 = Category.objects.create(
            name='Casa',
            type='REVENUE',
            user=self.user1
        )
        self.assertEqual(cat2.slug, 'casa-revenue')  # Atualizado

        # Terceira categoria - mesmo nome e tipo
        cat3 = Category.objects.create(
            name='Casa',
            type='EXPENSE',
            user=self.user2
        )
        self.assertEqual(cat3.slug, 'casa-expense-1')  # Atualizado

    def test_category_uniqueness(self):
        """Testa regras de unicidade para categorias"""
        from django.db import transaction

        # Primeira categoria
        cat1 = Category.objects.create(
            name='Casa',
            type='EXPENSE',
            user=self.user1
        )
        self.assertEqual(cat1.slug, 'casa-expense')

        # Tenta criar categoria duplicada (deve falhar)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(
                name='Casa',
                type='EXPENSE',
                user=self.user1
            )

        # Pode criar com mesmo nome mas tipo diferente
        cat2 = Category.objects.create(
            name='Casa',
            type='REVENUE',
            user=self.user1
        )
        self.assertEqual(cat2.slug, 'casa-revenue')


class BankTests(BaseTestCase):
    """Testes para o modelo Bank"""
    def test_create_bank(self):
        """Testa criação básica de banco"""
        bank = Bank.objects.create(
            name='Banco do Brasil',
            code='001',
            user=self.user1
        )
        self.assertEqual(bank.name, 'Banco Do Brasil')
        self.assertEqual(bank.code, '001')

    def test_duplicate_bank_code(self):
        """Testa que não permite códigos duplicados para mesmo usuário"""
        Bank.objects.create(
            name='Banco do Brasil',
            code='001',
            user=self.user1
        )
        with self.assertRaises(IntegrityError):
            Bank.objects.create(
                name='BB',
                code='001',
                user=self.user1
            )


class PaymentMethodTests(BaseTestCase):
    """Testes para o modelo PaymentMethod"""
    def test_create_payment_method(self):
        """Testa criação básica de método de pagamento"""
        payment = PaymentMethod.objects.create(
            name='Cartão de Crédito',
            user=self.user1
        )
        self.assertEqual(payment.name, 'Cartão De Crédito')

    def test_active_filter(self):
        """Testa filtro de métodos ativos"""
        PaymentMethod.objects.create(
            name='Ativo',
            user=self.user1,
            is_active=True
        )
        PaymentMethod.objects.create(
            name='Inativo',
            user=self.user1,
            is_active=False
        )
        active = PaymentMethod.objects.active_for_user(self.user1)
        self.assertEqual(active.count(), 1)
        self.assertEqual(active[0].name, 'Ativo')


class UserSpecificManagerTests(BaseTestCase):
    """Testes para o UserSpecificManager"""
    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(
            name='User1 Category',
            type='EXPENSE',
            user=self.user1
        )
        self.category2 = Category.objects.create(
            name='User2 Category',
            type='EXPENSE',
            user=self.user2
        )

    def test_for_user_filter(self):
        """Testa filtro por usuário"""
        user1_categories = Category.objects.for_user(self.user1)
        self.assertEqual(user1_categories.count(), 1)
        self.assertEqual(user1_categories[0], self.category1)

    def test_active_for_user_filter(self):
        """Testa filtro de ativos por usuário"""
        self.category1.is_active = False
        self.category1.save()

        active_categories = Category.objects.active_for_user(self.user1)
        self.assertEqual(active_categories.count(), 0)
