from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('learning/', views.learning_view, name='learning'),
    path('jobs/', views.jobs_view, name='jobs'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('settings/appearance/', views.appearance_view, name='appearance'),
    
    # API Endpoints
    path('api/theme/save/', views.api_save_theme, name='api_save_theme'),
    path('api/job-match/', views.api_job_match, name='api_job_match'),
    path('api/salary-predict/', views.api_salary_predict, name='api_salary_predict'),
    path('api/company-prep/', views.api_company_prep, name='api_company_prep'),
    path('api/tutor/', views.api_tutor, name='api_tutor'),
    path('api/notes/', views.api_notes, name='api_notes'),
    path('api/quiz/', views.api_quiz, name='api_quiz'),
    path('api/career-coach/', views.api_career_coach, name='api_career_coach'),
    path('api/career-coach/upload/', views.api_career_coach_upload, name='api_career_coach_upload'),
    path('api/roadmap/', views.api_roadmap, name='api_roadmap'),
]

