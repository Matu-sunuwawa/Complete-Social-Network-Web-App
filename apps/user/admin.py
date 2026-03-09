from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Follow

class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'username', 'is_staff', 'is_active')
    search_fields = ('email', 'username')

    fieldsets = UserAdmin.fieldsets

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Follow)
