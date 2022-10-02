from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


@admin.register(User)
class UserAdminConfig(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'mobile', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('date_joined',)
    readonly_fields = ['date_joined', 'date_modified', 'last_login']
    search_fields = ('username', 'first_name', 'last_name', 'mobile', 'email')
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'mobile', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Others', {
            'fields': ('date_joined', 'date_modified', 'last_login'),
        }),
    )
    add_fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'mobile', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
