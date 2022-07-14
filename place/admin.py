from django.contrib import admin
from .models import Duration, Place, PlaceType
from django.utils.html import mark_safe


class PlaceAdmin(admin.ModelAdmin):
    # object 목록에 띄워줄 필드를 지정한다.
    list_display = ('id', 'image_preview', 'user', 'name')
    # object 목록에서 클릭 시 상세 페이지로 들어갈 수 있는 필드를 지정한다.
    list_display_links = ('id', 'user', 'name')
    # list_filter = ('username', )                # filter를 걸 수 있는 필드를 생성한다.
    search_fields = ('word',)     # 검색에 사용될 필드를 지정한다.

    fieldsets = (                               # 상세페이지에서 필드를 분류하는데 사용된다.
        ("info", {'fields': ('user', 'typename',
         'name', 'x', 'y', 'rating', 'address')}),
        ('image', {'fields': ('image', )}),)

    # filter_horizontal = []

    # 상세페이지에서 읽기 전용 필드를 설정할 때 사용된다. obj=None 기본페이지에서 수정이 가능하니까 그걸 막기위해서
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ('user', 'name', 'image', )
    #     else:
    #         return ()
    # def image_tag(self, obj):
    #     if obj.image:
    #         return mark_safe(f'<img src="{obj.image.url}" width="150" height="150"/>')
    #     return None

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100"/>')
        return None


admin.site.register(Duration)
admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceType)
