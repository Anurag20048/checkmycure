from django.urls import path
from .views import log_and_analyze_symptom, get_preventive_tip

urlpatterns = [
    path('log-symptom/', log_and_analyze_symptom, name='log-symptom'),
    path('preventive-tip/', get_preventive_tip, name='preventive-tip'),
]
