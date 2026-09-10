from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

FRONTEND_DIR = settings.BASE_DIR.parent / 'frontend'

def serve_frontend_file(request, filename):
    return serve(request, filename, document_root=FRONTEND_DIR)

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html')),
    path('login.html', TemplateView.as_view(template_name='login.html')),
    path('signup.html', TemplateView.as_view(template_name='signup.html')),
    path('about.html', TemplateView.as_view(template_name='about.html')),
    path('contact.html', TemplateView.as_view(template_name='contact.html')),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html')),
    path('profile.html', TemplateView.as_view(template_name='profile.html')),
    path('settings.html', TemplateView.as_view(template_name='settings.html')),
    path('nearby-clinics.html', TemplateView.as_view(template_name='nearby-clinics.html')),
    path('symptom-checker.html', TemplateView.as_view(template_name='symptom-checker.html')),
    path('chatbot.html', TemplateView.as_view(template_name='chatbot.html')),
    path('emergency-profile.html', TemplateView.as_view(template_name='emergency-profile.html')),
    path('emergency-sos.html', TemplateView.as_view(template_name='emergency-sos.html')),
    path('admin-login.html', TemplateView.as_view(template_name='admin-login.html')),
    path('admin.html', TemplateView.as_view(template_name='admin.html')),
    path('eye-health.html', TemplateView.as_view(template_name='eye-health.html')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('health.urls')),
    path('api/', include('emergency.urls')),
    path('api/', include('insights.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^(?P<filename>.+\.(?:css|js|png|jpg|jpeg|gif|ico|svg|webp|json))$', serve_frontend_file),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
