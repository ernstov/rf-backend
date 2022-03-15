from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    readonly_fields = ("created_at", "updated_at")
    list_display = ["email"]
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Permissions"),
            {"fields": (
                "is_staff", "is_active", "is_superuser"
            )}
        ),
        (
            _("Important Dates"),
            {"fields": ("last_login", "created_at", "updated_at")}
        )
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide", ),
            "fields": ("email", "username", "password1", "password2")
        }),
    )

admin.site.register(models.User, UserAdmin)
