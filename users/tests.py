from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTests(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        """Testa a criação de um usuário normal"""
        user = self.User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.created_at)
        self.assertTrue(user.updated_at)

    def test_create_user_without_email(self):
        """Testa se criar usuário sem email levanta erro"""
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                password='testpass123',
                name='Test User'
            )

    def test_create_superuser(self):
        """Testa a criação de um superusuário"""
        admin_user = self.User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
            name='Admin User'
        )

        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.name, 'Admin User')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.created_at)
        self.assertTrue(admin_user.updated_at)

    def test_email_normalized(self):
        """Testa se o email é normalizado corretamente"""
        email = 'test@EXAMPLE.com'
        user = self.User.objects.create_user(
            email=email,
            password='testpass123',
            name='Test User'
        )

        self.assertEqual(user.email, email.lower())

    def test_user_str_method(self):
        """Testa o método __str__ do usuário"""
        user = self.User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

        self.assertEqual(str(user), 'test@example.com')
