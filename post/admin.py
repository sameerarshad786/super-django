from django.contrib import admin

from post.models.post_model import Post
from post.models.postremark_model import PostRemark, Comments


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text", "created", "updated")


admin.site.register(Post, PostAdmin)


class PostRemarkAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "on_post", "popularity", "created", "updated")


admin.site.register(PostRemark, PostRemarkAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "on_post", "comment", "created", "updated")


admin.site.register(Comments, CommentAdmin)
