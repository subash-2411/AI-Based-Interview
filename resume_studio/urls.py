from django.urls import path
from . import views

app_name = 'resume_studio'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('builder/', views.resume_builder, name='resume_builder'),
    path('preview/', views.resume_preview, name='resume_preview'),
    path('ats-checker/', views.ats_checker, name='ats_checker'),
    path('analyzer/', views.resume_analyzer, name='resume_analyzer'),
    path('cover-letter/', views.cover_letter_generator, name='cover_letter_generator'),
    path('ai-improver/', views.ai_improver, name='ai_improver'),
    path('templates/', views.template_selection, name='template_selection'),
]
