from django.contrib import admin

from .models import Types, Store


class TypesAdmin(admin.ModelAdmin):
    list_display = (
        "id", "type", "valid_name", "created", "updated"
    )

admin.site.register(Types, TypesAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "type", "name", "is_verified", "get_image",
        "created", "updated"
    )


admin.site.register(Store, StoreAdmin)
