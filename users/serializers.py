from rest_framework import serializers
from .models import CustomUser
from .validators import validate_basic_requirements, validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name', 'is_active',
                  'is_staff', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate_password(self, value):
        """
        Validação a nível de campo para senha
        """
        # Validações básicas primeiro
        validate_basic_requirements(value)
        return value

    def validate(self, data):
        """
        Validação a nível de objeto para regras complexas
        """
        password = data.get('password')
        email = data.get('email') or (self.instance.email if self.instance else None)
        name = data.get('name') or (self.instance.name if self.instance else None)

        if password:
            # Cria usuário temporário para validação
            temp_user = CustomUser(
                email=email,
                name=name,
                pk=self.instance.pk if self.instance else None
            )

            # Se for atualização, configura senha anterior
            if self.instance:
                temp_user.password = self.instance.password
                temp_user.previous_password_hash = self.instance.previous_password_hash

            # Validação completa
            validate_password(password, temp_user)

        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            new_password = validated_data.pop('password')

            # Salvar a senha atual antes de atualizar
            instance.previous_password_hash = instance.password
            instance.set_password(new_password)

        updated_user = super().update(instance, validated_data)
        updated_user.save()
        return updated_user


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'is_active')
