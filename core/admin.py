from django.contrib import admin
from .models.user_model import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_superuser", "is_verified",
                    "is_deactivate_by_admin", "joined", "updated")


admin.site.register(User, UserAdmin)
