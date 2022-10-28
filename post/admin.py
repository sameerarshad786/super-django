from django.contrib import admin

from post.models.post_model import Post
from post.models.remarks_model import PostRemarks, CommentRemarks, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "text", "created", "updated"
    )


admin.site.register(Post, PostAdmin)


class PostRemarksAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "on_post", "popularity", "created", "updated"
    )


admin.site.register(PostRemarks, PostRemarksAdmin)


class CommentRemarksAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "on_post", "on_comment", "popularity", "created",
        "updated"
    )


admin.site.register(CommentRemarks, CommentRemarksAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "on_post", "parent", "comment", "created", "updated"
    )


admin.site.register(Comments, CommentAdmin)
