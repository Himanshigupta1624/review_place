from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Place, Review


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("phone_number",)
    list_display = ("id", "name", "phone_number", "is_staff", "is_active")
    search_fields = ("name", "phone_number")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("name",)}),
        ("Permissions", {
            "fields": (
                "is_staff",
                "is_superuser",
                "is_active",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("name", "phone_number", "password1", "password2"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")


admin.site.register(Place)
admin.site.register(Review)
