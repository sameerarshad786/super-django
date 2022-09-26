from django.contrib import admin

from post.models.post_model import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "text", "created", "updated")

admin.site.register(Post, PostAdmin)
