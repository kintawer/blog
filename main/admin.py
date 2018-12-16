from django.contrib import admin
from .models import Post, Subscribe, Comment, Tag

# Register your models here.

admin.site.register(Post)
admin.site.register(Subscribe)
admin.site.register(Comment)
admin.site.register(Tag)
