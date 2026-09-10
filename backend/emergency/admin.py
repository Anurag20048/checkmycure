from django.contrib import admin
from .models import MedicalProfile, EmergencyContact, EmergencyLog


@admin.register(MedicalProfile)
class MedicalProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'age', 'gender', 'blood_group', 'emergency_contact_name', 'emergency_contact_phone', 'updated_at']
    list_filter = ['gender', 'blood_group', 'dnr_order']
    search_fields = ['user__username', 'user__email', 'name', 'blood_group']
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'age', 'gender', 'height', 'weight')
        }),
        ('Medical Information', {
            'fields': ('blood_group', 'allergies', 'medications', 'conditions', 'previous_surgeries')
        }),
        ('Emergency Contacts', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'secondary_contact_phone', 'secondary_contact_relation')
        }),
        ('Additional Information', {
            'fields': ('insurance_info', 'primary_doctor', 'special_needs', 'dnr_order')
        }),
    )


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone', 'relationship', 'priority', 'created_at']
    list_filter = ['priority', 'relationship']
    search_fields = ['user__username', 'name', 'phone']


@admin.register(EmergencyLog)
class EmergencyLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'activated_at', 'latitude', 'longitude', 'contacts_notified', 'emergency_services_called']
    list_filter = ['status', 'emergency_services_called', 'activated_at']
    search_fields = ['user__username', 'message', 'notes']
    readonly_fields = ['activated_at', 'get_location_link']
    
    def get_location_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://maps.google.com/?q={obj.latitude},{obj.longitude}"
            return f'<a href="{url}" target="_blank">View on Google Maps</a>'
        return 'No location'
    get_location_link.short_description = 'Location'
    get_location_link.allow_tags = True
