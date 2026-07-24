from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'uploaded_at', 'ats_score']
    search_fields = ['user__username', 'extracted_text']
