from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # /admin/ redirects to our custom Command Center — no Django admin UI exposed
    path('admin/', RedirectView.as_view(url='/admin-portal/', permanent=False)),

    # Custom Admin Portal
    path('admin-portal/', include('admin_portal.urls')),

    # App URLs
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('dashboard.urls')),
    path('resume/', include('resume.urls')),
    path('interview/', include('interview.urls')),
    path('coding/', include('coding_round.urls')),
    path('resume-studio/', include('resume_studio.urls')),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
