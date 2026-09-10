"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Frontend directory path
FRONTEND_DIR = settings.BASE_DIR.parent / 'frontend'


def serve_frontend_file(request, filename):
    """Serve frontend CSS, JS and image assets."""
    return serve(request, filename, document_root=FRONTEND_DIR)


urlpatterns = [
    # Frontend pages
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login'),
    path('signup.html', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('about.html', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact.html', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('profile.html', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('settings.html', TemplateView.as_view(template_name='settings.html'), name='settings'),
    path('nearby-clinics.html', TemplateView.as_view(template_name='nearby-clinics.html'), name='nearby-clinics'),
    path('symptom-checker.html', TemplateView.as_view(template_name='symptom-checker.html'), name='symptom-checker'),
    path('chatbot.html', TemplateView.as_view(template_name='chatbot.html'), name='chatbot'),
    path('emergency-profile.html', TemplateView.as_view(template_name='emergency-profile.html'), name='emergency-profile'),
    path('emergency-sos.html', TemplateView.as_view(template_name='emergency-sos.html'), name='emergency-sos'),
    path('admin-login.html', TemplateView.as_view(template_name='admin-login.html'), name='admin-login'),
    path('admin.html', TemplateView.as_view(template_name='admin.html'), name='admin'),
    path('eye-health.html', TemplateView.as_view(template_name='eye-health.html'), name='eye-health'),

    # Admin panel
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('api.urls')),
    path('api/', include('health.urls')),
    path('api/', include('emergency.urls')),
    path('api/', include('insights.urls')),

    # Frontend assets. These routes are enabled in production as well,
    # because the project is deployed as a simple Django/Gunicorn service.
    re_path(r'^(?P<filename>[^/]+\.(?:css|js|png|jpg|jpeg|gif|ico|svg|webp))$', serve_frontend_file),
    re_path(r'^(?P<filename>manifest\.json)$', serve_frontend_file),
    re_path(r'^(?P<filename>service-worker\.js)$', serve_frontend_file),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
