from django.contrib import admin
from .models import Trip, TripCourse, TripCourseType

class TripCourseInline(admin.StackedInline):
    model = TripCourse

class TripAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'user',  'created_at',)
    list_display_links = ('id', 'title',)
    list_filter = ('user',)

    search_fields = ('title',)

    fieldsets = (                               
        ('info', {'fields': ('user', 'title', 'content', 'created_at')}),
        )

    readonly_fields =  ('created_at',)

    inlines =  (
            TripCourseInline,
        )
   


admin.site.register(Trip, TripAdmin)
admin.site.register(TripCourse)
admin.site.register(TripCourseType)