from datetime import timedelta
from django.utils.timezone import now
from .models import SymptomLog

def analyze_symptom_pattern(user, symptom):
    recent_count = SymptomLog.objects.filter(
        user=user,
        symptom=symptom,
        created_at__gte=now() - timedelta(days=60)
    ).count()

    if recent_count >= 3:
        return (
            f"You’ve reported {symptom} multiple times in the last 2 months. "
            "It may be best to consult a specialist."
        )

    return None
