from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatbotView, LoginView, PredictView, RegisterView, SymptomCheckViewSet, detect_eye_disease, get_eye_detection_history, eye_chat, geocode_place, nearby_clinics, health_status

router = DefaultRouter()
router.register(r"symptom-checks", SymptomCheckViewSet, basename="symptom-checks")

urlpatterns = [
    path("health/", health_status, name="health-status"),
    path("predict/", PredictView.as_view(), name="predict"),
    path("chatbot/", ChatbotView.as_view(), name="chatbot"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("eye-detection/", detect_eye_disease, name="eye-detection"),
    path("eye-detection/history/", get_eye_detection_history, name="eye-detection-history"),
    path("eye-chat/", eye_chat, name="eye-chat"),
    path("locations/geocode/", geocode_place, name="locations-geocode"),
    path("locations/nearby/", nearby_clinics, name="locations-nearby"),
    path("", include(router.urls)),
]
