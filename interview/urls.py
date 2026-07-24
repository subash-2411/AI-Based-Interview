from django.urls import path
from . import views
from .reports import download_report_view
app_name = 'interview'

urlpatterns = [
    path('start/', views.start_interview_view, name='start_interview'),
    path('quick-start/', views.quick_start_interview_view, name='quick_start_interview'),
    path('room/<int:session_id>/', views.interview_room_view, name='interview_room'),
    path('generate-questions/<int:session_id>/', views.generate_questions_api, name='generate_questions_api'),
    path('submit-answer/<int:session_id>/', views.submit_answer_api, name='submit_answer_api'),
    path('complete/<int:session_id>/', views.complete_interview_view, name='complete_interview'),
    path('result/<int:session_id>/', views.interview_result_view, name='interview_result'),
    path('upload-recording/<int:session_id>/', views.upload_recording_api, name='upload_recording_api'),
    path('report/<int:session_id>/', download_report_view, name='download_report'),
]
