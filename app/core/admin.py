"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

from core import models

from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define admin pages for users"""

    ordering = ["id"]
    list_display = ["email", "name"]

    fieldsets = (
        (None, {"fields": ("email", "password", "team")}),
        (
            _("Permissions"),
            {"fields": (
                "is_active",
                "is_staff",
                "is_superuser",
            )}
        ),
        (
            _("Important dates"),
            {"fields": (
                "last_login",
            )}
        ),
    )
    readonly_fields = ["last_login"]

    search_fields = ['email', ]

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "name",
                "team",
                "is_active",
                "is_staff",
                "is_superuser"
            )
        }),
    )


class SolicitorInline(admin.TabularInline):  # you can also use admin.StackedInline
    model = models.Solicitor
    extra = 1  # defines the number of extra forms displayed at the bottom of the change list


class AgencyAdmin(admin.ModelAdmin):
    inlines = [SolicitorInline]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Team)
admin.site.register(models.Solicitor)
admin.site.register(models.Agency, AgencyAdmin)
admin.site.register(models.ApplicationStatus)
admin.site.register(models.Application)
admin.site.register(models.Estate)
