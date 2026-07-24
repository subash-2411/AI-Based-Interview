from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('upload/', views.upload_resume_view, name='upload_resume'),
    path('builder/', views.create_resume_view, name='resume_builder'),
    path('optimize-objective/', views.optimize_objective_api, name='optimize_objective'),
    path('analysis/<int:resume_id>/', views.resume_analysis_view, name='resume_analysis'),
]
