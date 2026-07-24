from django.contrib import admin
from .models import InterviewSession, InterviewQuestion

class QuestionInline(admin.TabularInline):
    model = InterviewQuestion
    extra = 0

@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'score', 'is_completed', 'created_at']
    list_filter = ['language', 'is_completed']
    inlines = [QuestionInline]
