from django.contrib import admin
from .models import Messages, BotMessages, Conversation, GroupConversation


class MessagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "from_user",
        "to_user",
        "conversation_on_id",
        "get_message",
        "created_at"
    )


admin.site.register(Messages, MessagesAdmin)


class BotMessagesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_deleted", "created_at")


admin.site.register(BotMessages, BotMessagesAdmin)


class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")


admin.site.register(Conversation, ConversationAdmin)


class GroupConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "name", "is_deleted", "created_at")


admin.site.register(GroupConversation, GroupConversationAdmin)
