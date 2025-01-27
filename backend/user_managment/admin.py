from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *



class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'photo',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Use exact model field names
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Status', {'fields': ('enabled', 'status')}),  # Use 'enabled' and 'status' as per the model fields
        ('Other info', {'fields': ('created', 'isLoggedIn')}),  # Match 'created' and 'isLoggedIn' field names from model
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'phone', 'photo', 'enabled', 'status', ),  # Ensure field names match the model fields
        }),
    )
    
    list_display = ('email', 'first_name', 'last_name', 'enabled', 'is_staff')  # Match 'enabled' from model
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    search_fields = ('user__username', 'role__name')
    list_filter = ('role',)
    raw_id_fields = ('user',)
    
@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp', 'user')    