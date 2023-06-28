from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from simpconnect_api.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "first_name", "last_name", "gender", "profile_picture")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "gender", "profile_picture")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
