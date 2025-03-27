from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'created_at', 'updated_at']
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('name',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    ordering = ('email',)
    search_fields = ('email', 'name')
    list_filter = ('is_staff', 'is_active', 'created_at')


admin.site.register(CustomUser, CustomUserAdmin)
