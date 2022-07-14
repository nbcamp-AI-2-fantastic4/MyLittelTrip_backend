from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'fullname')
    list_display_links = ('username', )
    list_filter = ('username', )
    search_fields = ('email' 'username', )

    filter_horizontal = []

    # 생성 / 수정 모두 readonly로 설정
    readonly_fields = ('join_date', )

    # 생성 시 write 가능, 수정 시 readonly field로 설정
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date', )
        else:
            return ('join_date', )

    def get_writeonly_fields(self, request, obj=None):
        return ('password', )

    fieldsets = (
        ("info", {'fields': ('email', 'username', 'fullname', 'password', 'join_date')}),
        ('permissions', {'fields': ('is_admin', 'is_active', )}),
    )


admin.site.register(User, UserAdmin)