from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import User, UserSensitiveInformation


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_superuser", "is_verified",
                    "is_deactivate_by_admin", "joined", "updated")


admin.site.register(User, UserAdmin)


class UserSensitiveInformationAdmin(OSMGeoAdmin):
    list_display = ("id", "point")


admin.site.register(UserSensitiveInformation, UserSensitiveInformationAdmin)
