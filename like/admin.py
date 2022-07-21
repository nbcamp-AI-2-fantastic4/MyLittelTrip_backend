from django.contrib import admin

from comment.models import Like

class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "posttype", "post_id"]
    list_display_links = ["id", "post_id"]
    list_filter = ["user", "posttype"]

    search_fields = ["user__username", "posttype__typename", "post_id"]

admin.site.register(Like, LikeAdmin)
