from django.contrib import admin
from .models import Category, Bank, PaymentMethod


class BaseAdmin(admin.ModelAdmin):
    """Classe base para configurações comuns do admin"""
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)

    def get_queryset(self, request):
        """Filtra registros por usuário se não for superuser"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Associa o usuário logado ao registro ao salvar"""
        if not change:  # Apenas em criação
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        """Permite edição apenas para superuser ou dono do registro"""
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        """Permite exclusão apenas para superuser ou dono do registro"""
        if not obj or request.user.is_superuser:
            return True
        return obj.user == request.user


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """Admin para o modelo de Categorias"""
    list_display = ('name', 'type', 'user', 'is_active', 'created_at')
    list_filter = BaseAdmin.list_filter + ('type', 'user')
    search_fields = BaseAdmin.search_fields + ('user__email',)
    raw_id_fields = ('user',)  # Melhor performance para seleção de usuário

    def get_queryset(self, request):
        """Otimiza consulta com select_related"""
        return super().get_queryset(request).select_related('user')


@admin.register(Bank)
class BankAdmin(BaseAdmin):
    """Admin para o modelo de Bancos"""
    list_display = ('name', 'code', 'is_active', 'created_at')
    search_fields = BaseAdmin.search_fields + ('code',)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(BaseAdmin):
    """Admin para o modelo de Formas de Pagamento"""
    list_display = ('name', 'is_active', 'created_at')
