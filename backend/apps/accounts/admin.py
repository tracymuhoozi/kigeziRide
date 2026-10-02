from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["-created_at"]
    list_display = ["full_name", "phone", "role", "is_verified", "is_active", "created_at"]
    list_filter = ["role", "is_verified", "is_active"]
    search_fields = ["full_name", "phone", "email"]
    readonly_fields = ["user_id", "created_at", "updated_at", "last_login"]

    fieldsets = (
        (None, {"fields": ("user_id", "phone", "password")}),
        ("Profile", {"fields": ("full_name", "email", "profile_photo", "role")}),
        ("Status", {"fields": ("is_active", "is_verified", "is_staff", "is_superuser")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("phone", "full_name", "role", "password1", "password2")}),
    )