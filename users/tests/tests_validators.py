from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from users.validators import (
    normalize_string,
    validate_basic_requirements,
    validate_email_parts,
    validate_name_parts,
    validate_previous_passwords
)
from users.models import CustomUser


class NormalizeStringTests(TestCase):
    """Testes para normalização de strings"""

    def test_normalize_empty_string(self):
        """Testa normalização de string vazia"""
        self.assertEqual(normalize_string(''), '')

    def test_normalize_accents(self):
        """Testa remoção de acentos"""
        test_cases = [
            ('João', 'joao'),
            ('José María', 'jose maria'),
            ('áéíóú', 'aeiou')
        ]
        for input_text, expected in test_cases:
            self.assertEqual(normalize_string(input_text), expected)


class BasicRequirementsTests(TestCase):
    """Testes para requisitos básicos de senha"""

    def test_min_length(self):
        """Testa comprimento mínimo"""
        with self.assertRaises(ValidationError) as cm:
            validate_basic_requirements('Abc@123')
        self.assertIn('8 caracteres', str(cm.exception))

    def test_uppercase(self):
        """Testa presença de maiúsculas"""
        with self.assertRaises(ValidationError) as cm:
            validate_basic_requirements('abc@123456')
        self.assertIn('maiúscula', str(cm.exception))

    def test_special_chars(self):
        """Testa caracteres especiais"""
        test_cases = '!@#$%^&*()-_=+[]{}|;:,.<>?/'
        for char in test_cases:
            password = f'Abcd123{char}'
            try:
                validate_basic_requirements(password)
            except ValidationError:
                self.fail(f'Caractere especial válido rejeitado: {char}')


class EmailPartsTests(TestCase):
    """Testes para validação de partes do email"""

    def setUp(self):
        """Configura usuário para testes"""
        self.user = CustomUser.objects.create_user(
            email='usuario.teste@exemplo.com',
            password='Teste@123',
            name='João Silva'
        )

    def test_email_parts_in_password(self):
        """Testa partes do email na senha"""
        invalid_passwords = [
            'Usuario123@',    # parte antes do @
            'Teste123@',      # parte do username
            'Exemplo123@'     # domínio
        ]
        for password in invalid_passwords:
            password_normalized = normalize_string(password)
            with self.assertRaises(ValidationError) as cm:
                validate_email_parts(password_normalized, self.user)
            self.assertIn('email', str(cm.exception))

    def test_short_email_parts(self):
        """Testa partes curtas do email"""
        self.user.email = 'ab.cd@test.com'
        self.user.save()

        # Partes com 2 caracteres ou menos devem ser permitidas
        validate_email_parts(normalize_string('Ab123@'), self.user)
        validate_email_parts(normalize_string('Cd123@'), self.user)


class NamePartsTests(TestCase):
    """Testes para validação de partes do nome"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            password='Test@123',
            name='João Carlos Silva'
        )

    def test_name_parts_in_password(self):
        """Testa partes do nome na senha"""
        test_cases = [
            ('João Silva', 'Joao123@'),
            ('Maria Santos', 'Santos123@'),
            ('José Carlos', 'Carlos123@')
        ]
        for name, password in test_cases:
            self.user.name = name
            self.user.save()
            with self.assertRaises(ValidationError) as cm:
                validate_name_parts(normalize_string(password), self.user)
            self.assertIn('nome', str(cm.exception))


class PreviousPasswordsTests(TestCase):
    """Testes para validação de senhas anteriores"""

    def setUp(self):
        """Configura usuário com senha anterior diferente da atual"""
        self.user = CustomUser.objects.create_user(
            email='test@test.com',
            password='CurrentPass@123',  # senha atual
            name='Test User'
        )
        # Define a senha anterior como "OldPass@123"
        self.user.previous_password_hash = make_password('OldPass@123')
        self.user.save()

    def test_previous_password(self):
        """Testa rejeição da senha anterior"""
        with self.assertRaises(ValidationError) as cm:
            validate_previous_passwords('OldPass@123', self.user)
        self.assertIn('anterior', str(cm.exception))
