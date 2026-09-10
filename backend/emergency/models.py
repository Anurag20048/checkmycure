from django.db import models
from django.contrib.auth.models import User


class MedicalProfile(models.Model):
    """User medical profile for emergency situations."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medical_profile')
    
    # Personal Information
    name = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    height = models.IntegerField(null=True, blank=True, help_text="Height in cm")
    weight = models.IntegerField(null=True, blank=True, help_text="Weight in kg")
    
    # Medical Information
    blood_group = models.CharField(max_length=10, blank=True)
    allergies = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    conditions = models.TextField(blank=True)
    previous_surgeries = models.TextField(blank=True)
    
    # Emergency Contacts
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    secondary_contact_phone = models.CharField(max_length=20, blank=True)
    secondary_contact_relation = models.CharField(max_length=100, blank=True)
    
    # Additional Information
    insurance_info = models.CharField(max_length=200, blank=True)
    primary_doctor = models.CharField(max_length=200, blank=True)
    special_needs = models.TextField(blank=True)
    dnr_order = models.BooleanField(default=False, help_text="Do Not Resuscitate order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MedicalProfile for {self.user.username}"


class EmergencyContact(models.Model):
    """Emergency contacts for a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='additional_emergency_contacts')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    relationship = models.CharField(max_length=100, blank=True)
    priority = models.IntegerField(default=1, help_text="1=Primary, 2=Secondary, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['priority', 'created_at']

    def __str__(self):
        return f"{self.name} ({self.phone})"


class EmergencyLog(models.Model):
    """Log of emergency events triggered by users."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_logs')
    activated_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Location
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_accuracy = models.FloatField(null=True, blank=True, help_text="Accuracy in meters")
    
    # Emergency Information
    message = models.TextField(blank=True)
    symptoms = models.JSONField(default=list, blank=True)
    hospitals_found = models.IntegerField(default=0)
    contacts_notified = models.IntegerField(default=0)
    emergency_services_called = models.BooleanField(default=False)
    
    # Medical snapshot at time of emergency
    medical_snapshot = models.JSONField(null=True, blank=True, help_text="Medical info at time of SOS")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Emergency SOS Log'
        verbose_name_plural = 'Emergency SOS Logs'

    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"Emergency #{self.id} by {user_str} at {self.created_at}"
    
    def get_location_url(self):
        """Generate Google Maps URL for the emergency location."""
        if self.latitude and self.longitude:
            return f"https://maps.google.com/?q={self.latitude},{self.longitude}"
        return None
