from django.contrib import admin

# Register your models here.
from post.models import PostComment, Post

admin.site.register(Post)
admin.site.register(PostComment)