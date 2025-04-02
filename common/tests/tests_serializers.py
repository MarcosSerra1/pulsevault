from django.test import TestCase
from rest_framework.exceptions import ValidationError
from common.serializers import CategoryModelSerializer, CategoryListModelSerializer
from common.models import Category
from users.models import CustomUser


class CategoryModelSerializerTests(TestCase):
    """Testes para o serializador de categorias."""

    def setUp(self):
        """Configura dados iniciais para os testes."""
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            name='Test User'
        )

        self.valid_data = {
            'name': 'Alimentação',
            'type': 'EXPENSE',
            'description': 'Gastos com alimentação',
            'user': self.user.id
        }

    def test_valid_category_serialization(self):
        """Testa serialização com dados válidos."""
        serializer = CategoryModelSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_category_type(self):
        """Testa tipo inválido de categoria."""
        invalid_data = self.valid_data.copy()
        invalid_data['type'] = 'INVALID'

        serializer = CategoryModelSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('type', serializer.errors)

    def test_missing_required_fields(self):
        """Testa campos obrigatórios ausentes."""
        invalid_data = {}
        serializer = CategoryModelSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('type', serializer.errors)

    def test_read_only_fields(self):
        """Testa campos somente leitura."""
        category = Category.objects.create(
            name=self.valid_data['name'],
            type=self.valid_data['type'],
            description=self.valid_data['description'],
            user=self.user
        )
        serializer = CategoryModelSerializer(category)

        self.assertIn('created_at', serializer.data)
        self.assertIn('updated_at', serializer.data)

    def test_optional_description(self):
        """Testa campo opcional de descrição."""
        data = {
            'name': 'Alimentação',
            'type': 'EXPENSE',
            'user': self.user.id  # Alterado para usar o ID
        }

        serializer = CategoryModelSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_name_max_length(self):
        """Testa tamanho máximo do nome."""
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'A' * 256  # max_length é 255

        serializer = CategoryModelSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_update_category(self):
        """Testa atualização de categoria."""
        category = Category.objects.create(
            name=self.valid_data['name'],
            type=self.valid_data['type'],
            description=self.valid_data['description'],
            user=self.user
        )

        update_data = {
            'name': 'Alimentação Atualizada',
            'description': 'Nova descrição'
        }

        serializer = CategoryModelSerializer(
            category,
            data=update_data,
            partial=True
        )

        self.assertTrue(serializer.is_valid())
        updated_category = serializer.save()
        self.assertEqual(updated_category.name, update_data['name'])
        self.assertEqual(updated_category.description, update_data['description'])


class CategoryListModelSerializerTests(TestCase):
    """Testes para o serializador de listagem de categorias."""

    def setUp(self):
        """
        Configura o ambiente para cada teste.
        - Cria um usuário de teste
        - Cria algumas categorias para testar
        """
        # Cria usuário para os testes
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='StrongPass123!',
            name='Test User'
        )

        # Cria categorias de teste
        self.categories = [
            Category.objects.create(
                name='Alimentação',
                type='EXPENSE',
                user=self.user
            ),
            Category.objects.create(
                name='Salário',
                type='REVENUE',
                user=self.user
            )
        ]

    def test_list_serializer_fields(self):
        """
        Testa se o serializer retorna apenas os campos esperados:
        - id
        - name
        - type
        """
        serializer = CategoryListModelSerializer(self.categories[0])
        data = serializer.data

        # Verifica campos que devem estar presentes
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('type', data)

        # Verifica campos que NÃO devem estar presentes
        self.assertNotIn('description', data)
        self.assertNotIn('user', data)
        self.assertNotIn('created_at', data)
        self.assertNotIn('updated_at', data)
        self.assertNotIn('is_active', data)

    def test_list_multiple_categories(self):
        """
        Testa serialização de múltiplas categorias.
        Verifica se a lista retornada mantém a estrutura correta.
        """
        serializer = CategoryListModelSerializer(self.categories, many=True)
        data = serializer.data

        # Verifica se retornou o número correto de categorias
        self.assertEqual(len(data), 2)

        # Verifica a estrutura de cada item
        for item in data:
            self.assertIn('id', item)
            self.assertIn('name', item)
            self.assertIn('type', item)

    def test_category_types(self):
        """
        Testa se os tipos de categoria são serializados corretamente.
        Verifica tanto REVENUE quanto EXPENSE.
        """
        serializer = CategoryListModelSerializer(self.categories, many=True)
        data = serializer.data

        # Encontra e verifica categoria do tipo EXPENSE
        expense_category = next(
            item for item in data
            if item['name'] == 'Alimentação'
        )
        self.assertEqual(expense_category['type'], 'EXPENSE')

        # Encontra e verifica categoria do tipo REVENUE
        revenue_category = next(
            item for item in data
            if item['name'] == 'Salário'
        )
        self.assertEqual(revenue_category['type'], 'REVENUE')
