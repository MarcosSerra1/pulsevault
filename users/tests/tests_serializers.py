from django.test import TestCase
from rest_framework.exceptions import ValidationError
from users.serializers import CustomUserSerializer, ListUserSerializer
from users.models import CustomUser


class CustomUserSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "email": "usuario.teste1@exemplo.com",
            "name": "João Silva",
            "password": "ValidPass@123"
        }
        self.invalid_password_data = {
            "email": "usuario.teste@exemplo.com",
            "name": "João Silva",
            # Senha sem letra maiúscula e com menos de 8 caracteres
            "password": "invalid"
        }
        # Cria um usuário para testar operações de update
        self.user = CustomUser.objects.create_user(**self.valid_data)

    def test_create_valid_user(self):
        """Testa criação de usuário com dados válidos."""
        data = self.valid_data.copy()
        data["email"] = "novo.usuario@exemplo.com"  # Email único para este teste
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.name, data["name"])
        # Verifica se a senha foi processada (hash diferente do valor puro)
        self.assertNotEqual(user.password, data["password"])

    def test_create_invalid_password(self):
        """Testa que a criação falha se a senha não cumprir os requisitos básicos."""
        serializer = CustomUserSerializer(data=self.invalid_password_data)
        self.assertFalse(serializer.is_valid())
        # A validação de senha pode estar em errors ou em non_field_errors
        self.assertIn('password', serializer.errors)

    def test_create_password_with_email_part(self):
        """Testa que a criação falha se a senha contiver parte do email."""
        data = self.valid_data.copy()
        # Senha que contém parte do email: "usuario" aparece na senha
        data["password"] = "Usuario@123"
        serializer = CustomUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # A mensagem de erro deve mencionar que a senha não pode conter partes do email
        errors = serializer.errors.get('non_field_errors') or serializer.errors
        self.assertTrue(any("email" in str(err) for err in errors))

    def test_update_user_with_new_password(self):
        """Testa atualização de usuário com mudança de senha."""
        old_hash = self.user.password  # Salva o hash atual antes da atualização
        update_data = {"password": "NewValid@123"}
        serializer = CustomUserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        # Verifica se a senha foi alterada
        self.assertNotEqual(updated_user.password, old_hash)
        # Verifica se o hash anterior foi salvo
        self.assertEqual(updated_user.previous_password_hash, old_hash)

    def test_update_user_without_password_field(self):
        """Testa atualização parcial sem alterar a senha."""
        update_data = {"name": "João da Silva"}
        serializer = CustomUserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertEqual(updated_user.name, "João da Silva")
        # O email deve permanecer inalterado
        self.assertEqual(updated_user.email, self.user.email)


class ListUserSerializerTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="usuario.teste@exemplo.com",
            name="João Silva",
            password="ValidPass@123"
        )

    def test_list_user_serializer_fields(self):
        """Testa se o serializer de listagem retorna apenas os campos permitidos."""
        serializer = ListUserSerializer(instance=self.user)
        data = serializer.data
        self.assertIn("email", data)
        self.assertIn("name", data)
        self.assertIn("is_active", data)
        # Campos que não devem aparecer:
        self.assertNotIn("password", data)
        self.assertNotIn("is_staff", data)
        self.assertNotIn("created_at", data)
        self.assertNotIn("updated_at", data)
