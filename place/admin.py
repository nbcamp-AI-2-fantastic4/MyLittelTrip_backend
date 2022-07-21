from django.contrib import admin
from .models import Duration, Place, PlaceType
from django.utils.html import mark_safe  # type: ignore


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'user', 'name')
    list_display_links = ('id', 'user', 'name')
    search_fields = ('word',)   

    fieldsets = (                              
        ("info", {'fields': ('user', 
         '_id', 'placetype','name', 'x', 'y', 'rating', 'address')}),
        ('image', {'fields': ('image', )}),)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100"/>')
        return None


admin.site.register(Duration)
admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceType)
