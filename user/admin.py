from django.contrib import admin
from  .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(User)
class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'first_name')
    list_filter = ('email', 'first_name')
    ordering = ("-created_at",)
    list_display = ('email', 'first_name')
    # update user
    fieldsets = (
        (None, {'fields': ('email', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('is_deleted', 'deleted_at')})
    )
    # Add new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'password1', 'password2')}),
        
    )
    
    
