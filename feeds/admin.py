from django.contrib import admin

from .models.feeds_model import Feeds
from .models.comments_model import Comments
from .models.remarks_model import Remarks


class FeedsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "get_text", "get_files", "created", "updated"
    )


admin.site.register(Feeds, FeedsAdmin)


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "on_post", "on_comment", "get_text", "get_files",
        "created", "updated"
    )


admin.site.register(Comments, CommentsAdmin)


class RemarksAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "on_post", "on_comment", "popularity", "created",
        "updated"
    )


admin.site.register(Remarks, RemarksAdmin)
