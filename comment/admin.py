from django.contrib import admin
from .models import Like, Comment, PostType

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(PostType)