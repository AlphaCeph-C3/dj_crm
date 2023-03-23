from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Agent, Category, Lead, UserProfile

# Register your models here.
User = get_user_model()


# FIXME: the fieldset is giving the error of "cannot unpack non-iterable None Type object"
# HACK: just had to remove the add fieldset because that was causing the problem.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "first_name", "last_name", "is_staff", "is_active"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_organizer",
                    "is_agent",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = [
        "username",
    ]


# admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Agent)
admin.site.register(Lead)
admin.site.register(UserProfile)
