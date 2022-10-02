from django.contrib import admin

from post.models.post_model import Post
from post.models.postremark_model import PostRemark


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "text", "created", "updated")


admin.site.register(Post, PostAdmin)


class PostRemarkAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "get_on_postID", "popularity"]


admin.site.register(PostRemark, PostRemarkAdmin)
