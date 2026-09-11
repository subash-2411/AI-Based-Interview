from django.urls import path
from . import views
app_name = 'coding'

urlpatterns = [
    path('', views.coding_dashboard_view, name='coding_dashboard'),
    path('list/<str:language>/', views.coding_list_view, name='coding_list'),
    path('setup/', views.coding_setup_view, name='coding_setup'),
    path('generate/', views.generate_practice_api, name='generate_practice_api'),
    path('generate-single/', views.generate_single_challenge_api, name='generate_single_challenge_api'),
    path('editor/<int:problem_id>/', views.coding_editor_view, name='coding_editor'),
    path('submit/<int:problem_id>/', views.submit_code_api, name='submit_code_api'),
    path('hint/<int:problem_id>/', views.get_hint_api, name='get_hint_api'),
]
