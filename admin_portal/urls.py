from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    # ── Public pages ──
    path('', views.admin_landing, name='landing'),
    path('login/', views.admin_login_view, name='login'),
    path('logout/', views.admin_logout_view, name='logout'),

    # ── Protected portal (superuser only) ──
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.admin_users, name='users'),
    path('users/<int:user_id>/', views.admin_user_detail, name='user_detail'),
    path('interviews/', views.admin_interviews, name='interviews'),
    path('resumes/', views.admin_resumes, name='resumes'),
    path('coding/', views.admin_coding, name='coding'),
    path('coding/add/', views.admin_add_problem, name='add_problem'),
    path('coding/delete/<int:problem_id>/', views.admin_delete_problem, name='delete_problem'),

    # ── API ──
    path('api/stats/', views.admin_stats_api, name='stats_api'),
    path('resumes/<int:resume_id>/download/', views.admin_download_resume, name='download_resume'),
]
