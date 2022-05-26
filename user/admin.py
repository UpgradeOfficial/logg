from django.contrib import admin
from  .models import User, School, Administrator, Teacher, Guardian, Student, Staff
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from email.policy import default
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.



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
        ('Personal', {'fields': ('is_deleted', 'deleted_at', "image", 'user_type')})
    )
    # Add new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','image', 'password1', 'password2')}),
        
    )
    
    
models = [School, Administrator, Teacher, Guardian, Student, Staff]
for model in models:
    admin.site.register(model)