from django.db import models
from django.utils.text import slugify
from users.models import CustomUser

TYPE_CHOICES = [
    ('REVENUE', 'Receita'),
    ('EXPENSE', 'Despesa'),
]


class UserSpecificManager(models.Manager):
    """
    Gerenciador personalizado para modelos específicos por usuário.

    Fornece métodos auxiliares para filtrar objetos por usuário e status.

    Methods:
        for_user(user): Retorna objetos específicos do usuário
        active_for_user(user): Retorna objetos ativos do usuário
        get_queryset(): Retorna queryset ordenado por nome
    """
    def for_user(self, user):
        """
        Retorna objetos específicos do usuário.

        Args:
            user (CustomUser): Usuário para filtrar

        Returns:
            QuerySet: Objetos pertencentes ao usuário
        """
        return self.filter(user=user)

    def active_for_user(self, user):
        """Retorna objetos ativos do usuário"""
        return self.for_user(user).filter(is_active=True)

    def get_queryset(self):
        """Garante que sempre retornamos um queryset ordenado"""
        return super().get_queryset().order_by('name')


class BaseModel(models.Model):
    """
    Modelo base abstrato com campos e comportamentos comuns.

    Fornece campos básicos e funcionalidades compartilhadas por todos os modelos
    do sistema que precisam ser específicos por usuário.

    Attributes:
        name (str): Nome do registro
        description (str): Descrição opcional
        is_active (bool): Status de ativo/inativo
        created_at (datetime): Data de criação
        updated_at (datetime): Data da última atualização
        user (FK): Usuário proprietário

    Meta:
        abstract: True (não gera tabela)
        unique_together: Garante unicidade de (name, user)
    """
    name = models.CharField(max_length=255, verbose_name='Nome')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Descrição')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    objects = UserSpecificManager()

    class Meta:
        abstract = True
        # Garante unicidade por usuário
        unique_together = ['name', 'user']

    def save(self, *args, **kwargs):
        """Normaliza o nome para capitalizado antes de salvar"""
        if self.name:
            self.name = self.name.title()
        if hasattr(self, 'description') and self.description:
            self.description = self.description.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(BaseModel):
    """
    Modelo para categorias de transações.

    Attributes:
        name (str): Nome da categoria (herdado de BaseModel)
        type (str): Tipo da categoria (REVENUE/EXPENSE)
        slug (str): Identificador único gerado automaticamente
        user (FK): Usuário proprietário (herdado de BaseModel)

    Meta:
        unique_together: Garante unicidade de (name, type, user)
    """
    type = models.CharField(
        max_length=100,
        choices=TYPE_CHOICES,
        verbose_name='Tipo'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = [['name', 'type', 'user']]

    def save(self, *args, **kwargs):
        """Normaliza o nome e gera o slug"""
        # Gera o slug apenas se não existir
        if not self.slug:
            base_slug = f'{slugify(self.name)}-{self.type.lower()}'
            self.slug = base_slug

            # Verifica se já existe um slug igual
            counter = 1
            while Category.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f'{base_slug}-{counter}'
                counter += 1

        # Chama o save do modelo base
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.get_type_display()}'


class Bank(BaseModel):
    """
    Modelo para bancos.

    Attributes:
        name (str): Nome do banco (herdado de BaseModel)
        code (str): Código oficial do banco (3 dígitos)
        description (str): Descrição opcional (herdado de BaseModel)
        is_active (bool): Status de ativo/inativo (herdado de BaseModel)
        user (FK): Usuário proprietário (herdado de BaseModel)
        created_at (datetime): Data de criação (herdado de BaseModel)
        updated_at (datetime): Data da última atualização (herdado de BaseModel)

    Meta:
        verbose_name: Banco
        verbose_name_plural: Bancos
        ordering: Ordenado por nome
        unique_together: Garante unicidade de (code, user)
    """
    code = models.CharField(
        max_length=3,
        verbose_name='Código do Banco'
    )

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['name']
        unique_together = ['code', 'user']  # Adiciona unicidade por usuário


class PaymentMethod(BaseModel):
    """
    Modelo para métodos de pagamento.

    Attributes:
        name (str): Nome do método (herdado de BaseModel)
        description (str): Descrição opcional (herdado de BaseModel)
        is_active (bool): Status de ativo/inativo (herdado de BaseModel)
        user (FK): Usuário proprietário (herdado de BaseModel)
        created_at (datetime): Data de criação (herdado de BaseModel)
        updated_at (datetime): Data da última atualização (herdado de BaseModel)

    Meta:
        verbose_name: Forma de Pagamento
        verbose_name_plural: Formas de Pagamento
        ordering: Ordenado por nome
    """
    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['name']
