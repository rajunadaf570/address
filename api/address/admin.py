from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'last_name', 'full_name',]

admin.site.register(User, CustomUserAdmin)