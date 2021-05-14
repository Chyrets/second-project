from django.contrib import admin

from post.models import Post, Stream, Tag

admin.site.register(Post)
admin.site.register(Stream)
admin.site.register(Tag)
