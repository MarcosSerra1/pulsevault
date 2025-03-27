from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name', 'is_active',
                  'is_staff', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
