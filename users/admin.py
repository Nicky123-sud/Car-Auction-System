from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff")

admin.site.register(User, UserAdmin)
# Register your models here.
