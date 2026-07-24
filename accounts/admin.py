from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Skill, UserHistory, ThemePreference


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'phone_number', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'phone_number']
    ordering = ['-date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('profile_pic', 'bio', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('phone_number',)}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'level']
    list_filter = ['level']
    search_fields = ['user__username', 'name']


@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_interviews', 'avg_score', 'xp', 'level']
    search_fields = ['user__username']


@admin.register(ThemePreference)
class ThemePreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme_name', 'last_updated']
