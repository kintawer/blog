from django.contrib import admin
from .models import Post, Subscribe, Comment, Tag, Viewer

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('viewers',)


admin.site.register(Post, PostAdmin)
admin.site.register(Subscribe)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Viewer)
