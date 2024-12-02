# accounts/admin.py
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    # 기존 UserAdmin의 필드셋에 커스텀 필드 추가
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('goal', 'level')}),
    )

    # 목록 화면에서 보여줄 필드들
    list_display = BaseUserAdmin.list_display + ('goal', 'level')

    # 검색 가능한 필드
    search_fields = BaseUserAdmin.search_fields + ('goal', 'level')


admin.site.register(User, CustomUserAdmin)
