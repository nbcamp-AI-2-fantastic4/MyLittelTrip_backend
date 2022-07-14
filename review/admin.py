from django.contrib import admin
from .models import ReviewImage, Review

from django.utils.html import mark_safe


class ReviewImageInline(admin.StackedInline):
    model = ReviewImage
    extra = 0

    fieldsets = (
        ('image', {'fields': ('order','image','image_tag',)}),
        )

    def get_readonly_fields(self, request, obj): 
        if obj:
            return ('image_tag',)
        else:
            return ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="100" height="100"/>'.format(obj.image.url))


class ReviewAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'title', 'image_preview',)
    list_display_links = ('id', 'user', 'title', 'image_preview',)
    list_filter = ('user',)

    search_fields = ('user__username', 'title')

    readonly_fields = ('created_at',)

    fieldsets = (                               
        ('info', {'fields': ('created_at', 'user', 'trip')}),
        ('content', {'fields': ('title', 'content')}),
        )


    def image_preview(self, obj):
        images = obj.reviewimage_set.all().first()
        if obj.reviewimage_set:
            return mark_safe(f'<img src="{images.image.url}" width="100" height="100"/>')

    inlines = (
            ReviewImageInline,
        )


class ReviewImageAdmin(admin.ModelAdmin):

    list_display = ('id', 'review', 'image_tag',)
    list_display_links = ('id', 'review', 'image_tag',)
    list_filter = ('review',)

    search_fields = ('review__title',)

    fieldsets = (                               
        ('info', {'fields': ('review', 'order',)}),
        ('image', {'fields': ('image', 'image_tag')}),
        )


    def get_readonly_fields(self, request, obj=None): 
        if obj:
            return ('image_tag',)
        else:
            return ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100"/>')
        return None
    
    
admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewImage, ReviewImageAdmin)