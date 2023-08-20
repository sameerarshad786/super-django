from django.contrib import admin

from .models.posts_model import Posts
from .models.comments_model import Comments
from .models.remarks_model import Remarks


class PostsAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "get_text", "get_files", "created", "updated"
    )
    ordering = ("-created_at", )


admin.site.register(Posts, PostsAdmin)


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post",
        "get_text",
        "get_files",
        "created",
        "updated"
    )


admin.site.register(Comments, CommentsAdmin)


class RemarksAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "post", "comment", "created", "updated"
    )


admin.site.register(Remarks, RemarksAdmin)
