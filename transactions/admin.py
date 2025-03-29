from django.contrib import admin
from common.admin import BaseAdmin
from .models import Revenue, Expense


class FinancialBaseAdmin(BaseAdmin):
    """
    Configuração base para admin de transações financeiras.

    Estende BaseAdmin com campos e filtros específicos para transações.
    """
    list_display = ('payment_date', 'description', 'category', 'value', 'status', 'bank', 'user')
    list_filter = ('status', 'payment_date', 'bank', 'category')
    search_fields = ('description', 'observation', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-payment_date',)
    raw_id_fields = ('user', 'bank', 'category')

    def get_queryset(self, request):
        """Otimiza consulta com select_related"""
        return super().get_queryset(request).select_related(
            'user',
            'bank',
            'category'
        )


@admin.register(Revenue)
class RevenueAdmin(FinancialBaseAdmin):
    """Admin para o modelo de Receitas"""
    list_display = FinancialBaseAdmin.list_display + ('created_at',)
    list_filter = FinancialBaseAdmin.list_filter + ('created_at',)
    fieldsets = (
        ('Informações Principais', {
            'fields': ('payment_date', 'description', 'value', 'category')
        }),
        ('Detalhes', {
            'fields': ('status', 'bank', 'observation')
        }),
        ('Sistema', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Expense)
class ExpenseAdmin(FinancialBaseAdmin):
    """Admin para o modelo de Despesas"""
    list_display = FinancialBaseAdmin.list_display + ('payment_method', 'created_at')
    list_filter = FinancialBaseAdmin.list_filter + ('payment_method', 'created_at')
    raw_id_fields = FinancialBaseAdmin.raw_id_fields + ('payment_method',)
    fieldsets = (
        ('Informações Principais', {
            'fields': ('payment_date', 'description', 'value', 'category')
        }),
        ('Detalhes', {
            'fields': ('status', 'bank', 'payment_method', 'observation')
        }),
        ('Sistema', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        """Otimiza consulta incluindo payment_method"""
        return super().get_queryset(request).select_related('payment_method')
