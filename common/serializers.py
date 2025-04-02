from rest_framework import serializers
from .models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    """
    Serializador para operações de CRUD.
    """
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'user': {'required': False},
            'description': {'required': False}
        }


class CategoryListModelSerializer(serializers.ModelSerializer):
    """
    Seralizador para listagem.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'type')
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'user': {'required': False},
            'description': {'required': False}
        }
