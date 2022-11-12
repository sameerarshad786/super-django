from django.contrib import admin
from profiles.models.profile_model import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "username", "gender", "created", "updated"]


admin.site.register(Profile, ProfileAdmin)
