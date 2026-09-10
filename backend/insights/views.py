from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import SymptomLog
from .utils import analyze_symptom_pattern
from .preventive import preventive_tip


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_and_analyze_symptom(request):
    """Log a symptom and analyze patterns."""
    user = request.user
    symptom = request.data.get("symptom", "").strip()

    if not symptom:
        return Response({"error": "symptom is required"}, status=400)

    SymptomLog.objects.create(user=user, symptom=symptom)

    insight = analyze_symptom_pattern(user, symptom)

    return Response({
        "symptom": symptom,
        "insight": insight,
        "logged": True,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def get_preventive_tip(request):
    """Get preventive health tips based on disease and weather."""
    disease = request.data.get("disease", "").strip()
    weather = request.data.get("weather", "").strip()

    # Try to get user's medical profile if authenticated
    profile = None
    if request.user.is_authenticated:
        profile = getattr(request.user, 'medical_profile', None)

    tip = preventive_tip(disease, weather, profile)

    return Response({
        "disease": disease,
        "weather": weather,
        "tip": tip or "Stay healthy! Drink plenty of water and maintain good hygiene.",
    })
