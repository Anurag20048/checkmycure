from rest_framework import serializers
from .models import MedicalProfile, EmergencyContact, EmergencyLog


class MedicalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalProfile
        fields = [
            'id', 'name', 'age', 'gender', 'height', 'weight',
            'blood_group', 'allergies', 'medications', 'conditions', 'previous_surgeries',
            'emergency_contact_name', 'emergency_contact_phone',
            'secondary_contact_phone', 'secondary_contact_relation',
            'insurance_info', 'primary_doctor', 'special_needs', 'dnr_order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['id', 'name', 'phone', 'relationship', 'priority', 'created_at']
        read_only_fields = ['id', 'created_at']


class EmergencyLogSerializer(serializers.ModelSerializer):
    location_url = serializers.SerializerMethodField()
    
    class Meta:
        model = EmergencyLog
        fields = [
            'id', 'activated_at', 'resolved_at', 'status',
            'latitude', 'longitude', 'location_accuracy', 'location_url',
            'message', 'symptoms', 'hospitals_found', 'contacts_notified',
            'emergency_services_called', 'medical_snapshot', 'notes',
            'created_at'
        ]
        read_only_fields = ['id', 'activated_at', 'created_at']
    
    def get_location_url(self, obj):
        return obj.get_location_url()


class SOSRequestSerializer(serializers.Serializer):
    lat = serializers.FloatField(min_value=-90, max_value=90)
    lon = serializers.FloatField(min_value=-180, max_value=180)
    accuracy = serializers.FloatField(required=False, allow_null=True, min_value=0)
    contacts_notified = serializers.IntegerField(required=False, min_value=0, default=0)
    hospitals_notified = serializers.IntegerField(required=False, min_value=0, default=0)
    emergency_services_called = serializers.BooleanField(required=False, default=False)
    symptoms = serializers.ListField(child=serializers.CharField(), required=False, default=list)
