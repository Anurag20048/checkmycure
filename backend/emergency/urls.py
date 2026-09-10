from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MedicalProfileView,
    EmergencyContactViewSet,
    EmergencyLogViewSet,
    trigger_sos,
    notify_hospitals,
)

router = DefaultRouter()
router.register(r'emergency-contacts', EmergencyContactViewSet, basename='emergency-contacts')
router.register(r'emergency-logs', EmergencyLogViewSet, basename='emergency-logs')

urlpatterns = [
    path('sos/', trigger_sos, name='trigger-sos'),
    path('sos/notify-hospitals/', notify_hospitals, name='notify-hospitals'),
    path('medical-profile/', MedicalProfileView.as_view(), name='medical-profile'),
    path('', include(router.urls)),
]
