from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import os
import requests

from .models import MedicalProfile, EmergencyContact, EmergencyLog
from .serializers import (
    MedicalProfileSerializer,
    EmergencyContactSerializer,
    EmergencyLogSerializer,
    SOSRequestSerializer,
)


class MedicalProfileView(APIView):
    """Get or update the authenticated user's medical profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = MedicalProfile.objects.get_or_create(user=request.user)
        serializer = MedicalProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = MedicalProfile.objects.get_or_create(user=request.user)
        serializer = MedicalProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EmergencyContactViewSet(viewsets.ModelViewSet):
    """CRUD for emergency contacts."""
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyContactSerializer

    def get_queryset(self):
        return EmergencyContact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EmergencyLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only access to emergency logs for authenticated users."""
    permission_classes = [IsAuthenticated]
    serializer_class = EmergencyLogSerializer

    def get_queryset(self):
        return EmergencyLog.objects.filter(user=self.request.user)


def _twilio_send_sms(to_number, body):
    """Send an SMS through Twilio when server credentials are configured."""
    sid = os.environ.get('TWILIO_ACCOUNT_SID', '').strip()
    token = os.environ.get('TWILIO_AUTH_TOKEN', '').strip()
    from_number = os.environ.get('TWILIO_FROM_NUMBER', '').strip()
    if not all([sid, token, from_number, to_number]):
        return {'sent': False, 'reason': 'Twilio SMS is not configured'}
    url = f'https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json'
    try:
        response = requests.post(
            url,
            data={'From': from_number, 'To': to_number, 'Body': body},
            auth=(sid, token),
            timeout=15,
        )
        if response.ok:
            return {'sent': True}
        return {'sent': False, 'reason': f'Twilio returned HTTP {response.status_code}'}
    except requests.RequestException as exc:
        return {'sent': False, 'reason': str(exc)}


def _twilio_send_whatsapp(to_number, body):
    """Send a WhatsApp message through Twilio when WhatsApp credentials are configured."""
    sid = os.environ.get('TWILIO_ACCOUNT_SID', '').strip()
    token = os.environ.get('TWILIO_AUTH_TOKEN', '').strip()
    from_number = os.environ.get('TWILIO_WHATSAPP_FROM', '').strip()
    if not all([sid, token, from_number, to_number]):
        return {'sent': False, 'reason': 'Twilio WhatsApp is not configured'}
    destination = to_number if to_number.startswith('whatsapp:') else f'whatsapp:{to_number}'
    url = f'https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json'
    try:
        response = requests.post(
            url,
            data={'From': from_number, 'To': destination, 'Body': body},
            auth=(sid, token),
            timeout=15,
        )
        if response.ok:
            return {'sent': True}
        return {'sent': False, 'reason': f'Twilio returned HTTP {response.status_code}'}
    except requests.RequestException as exc:
        return {'sent': False, 'reason': str(exc)}


def _send_configured_contact_alerts(contacts, message):
    """Try SMS and optional WhatsApp delivery for configured emergency contacts."""
    sms_sent = 0
    whatsapp_sent = 0
    failures = []
    for contact in contacts:
        phone = (getattr(contact, 'phone', '') or '').strip()
        if not phone:
            continue
        sms_result = _twilio_send_sms(phone, message)
        if sms_result['sent']:
            sms_sent += 1
        elif sms_result.get('reason') and 'not configured' not in sms_result['reason']:
            failures.append(f'{getattr(contact, "name", "contact")}: {sms_result["reason"]}')

        wa_result = _twilio_send_whatsapp(phone, message)
        if wa_result['sent']:
            whatsapp_sent += 1
        elif wa_result.get('reason') and 'not configured' not in wa_result['reason']:
            failures.append(f'{getattr(contact, "name", "contact")}: {wa_result["reason"]}')
    return {'sms_sent': sms_sent, 'whatsapp_sent': whatsapp_sent, 'failures': failures}


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def notify_hospitals(request):
    """Send the emergency message to nearby hospital phone numbers supplied by OSM."""
    hospitals = request.data.get('hospitals', [])
    message = (request.data.get('message') or '').strip()
    if not isinstance(hospitals, list) or not message:
        return Response({'error': 'hospitals list and message are required'}, status=400)

    results = []
    for hospital in hospitals[:10]:
        if not isinstance(hospital, dict):
            continue
        phone = str(hospital.get('phone') or '').strip()
        name = str(hospital.get('name') or 'Nearby hospital').strip()
        if not phone:
            results.append({'name': name, 'sent': False, 'reason': 'No public phone number available'})
            continue
        sms = _twilio_send_sms(phone, message)
        results.append({'name': name, 'phone': phone, 'sent': sms['sent'], 'reason': sms.get('reason', '')})

    sent = sum(1 for item in results if item.get('sent'))
    return Response({'sent': sent, 'results': results})


@api_view(['POST'])
@permission_classes([AllowAny])
def trigger_sos(request):
    """
    SOS endpoint - logs emergency and returns a pre-formatted message.
    Works for both authenticated and anonymous users.
    """
    serializer = SOSRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    lat = serializer.validated_data['lat']
    lon = serializer.validated_data['lon']
    symptoms = serializer.validated_data.get('symptoms', [])

    user = request.user if request.user.is_authenticated else None

    # Build emergency message
    location_link = f"https://maps.google.com/?q={lat},{lon}"
    
    # Get additional data from request
    accuracy = serializer.validated_data.get('accuracy')
    contacts_notified = serializer.validated_data.get('contacts_notified', 0)
    hospitals_notified = serializer.validated_data.get('hospitals_notified', 0)
    emergency_services_called = serializer.validated_data.get('emergency_services_called', False)
    
    medical_snapshot = None

    if user:
        profile = MedicalProfile.objects.filter(user=user).first()
        contacts = EmergencyContact.objects.filter(user=user)
        if not contacts_notified:
            contacts_notified = contacts.count()

        message_parts = [
            "🚨 EMERGENCY ALERT 🚨",
            "",
            f"Name: {profile.name if profile and profile.name else user.username}",
            f"Location: {location_link}",
            "",
        ]

        if profile:
            # Create medical snapshot
            medical_snapshot = {
                'name': profile.name,
                'age': profile.age,
                'gender': profile.gender,
                'blood_group': profile.blood_group,
                'allergies': profile.allergies,
                'conditions': profile.conditions,
                'medications': profile.medications,
                'height': profile.height,
                'weight': profile.weight,
            }
            
            message_parts.extend([
                f"Blood Group: {profile.blood_group or 'N/A'}",
                f"Allergies: {profile.allergies or 'None'}",
                f"Conditions: {profile.conditions or 'None'}",
                f"Medications: {profile.medications or 'None'}",
                "",
            ])

        if symptoms:
            message_parts.append(f"Symptoms: {', '.join(symptoms)}")
            message_parts.append("")

        message_parts.append("Immediate medical assistance required.")
        message_parts.append("— Sent via Check MyCure")

        message = "\n".join(message_parts)
    else:
        contacts_notified = 0
        message = f"""🚨 EMERGENCY ALERT 🚨

Location: {location_link}

{"Symptoms: " + ", ".join(symptoms) if symptoms else "Critical Emergency"}

Immediate medical assistance required.
— Sent via Check MyCure"""

    # Log the emergency
    sos_log = EmergencyLog.objects.create(
        user=user,
        latitude=lat,
        longitude=lon,
        location_accuracy=accuracy,
        message=message,
        symptoms=symptoms,
        contacts_notified=contacts_notified,
        hospitals_found=hospitals_notified,
        emergency_services_called=emergency_services_called,
        medical_snapshot=medical_snapshot,
        status='active'
    )

    notification_result = {'sms_sent': 0, 'whatsapp_sent': 0, 'failures': []}
    if user and contacts.exists():
        notification_result = _send_configured_contact_alerts(contacts, message)
        delivered = notification_result['sms_sent'] + notification_result['whatsapp_sent']
        if delivered:
            sos_log.contacts_notified = delivered
            sos_log.save(update_fields=['contacts_notified'])

    return Response({
        "id": sos_log.id,
        "message": message,
        "location": location_link,
        "contacts_notified": sos_log.contacts_notified,
        "notifications": notification_result,
        "status": "active"
    })
