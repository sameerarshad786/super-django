from django.contrib import admin
from .models import Messages, BotMessages


class MessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "message", "created_at")


admin.site.register(Messages)


class BotMessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")


admin.site.register(BotMessages)
