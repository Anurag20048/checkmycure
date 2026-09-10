from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Basic user profile info."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.full_name or self.user.get_username()


class SymptomCheck(models.Model):
    """Stores a symptom check event (optionally linked to a logged-in user)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="symptom_checks",
    )

    symptoms = models.JSONField(default=list)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    medical_history = models.TextField(blank=True)

    prediction = models.CharField(max_length=200, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        base = f"SymptomCheck #{self.id}"
        if self.user_id:
            return f"{base} ({self.user.get_username()})"
        return base


class EyeDetection(models.Model):
    """Stores eye health detection results using YOLO model."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eye_detections",
    )
    
    # Image storage
    original_image = models.ImageField(upload_to='eye_scans/original/', null=True, blank=True)
    processed_image = models.ImageField(upload_to='eye_scans/processed/', null=True, blank=True)
    
    # Detection results
    disease = models.CharField(max_length=200, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    detections = models.JSONField(default=dict, help_text="Full YOLO detection results")
    
    # Comprehensive disease information
    disease_info = models.TextField(blank=True, help_text="Detailed disease information")
    symptoms = models.JSONField(default=list, help_text="List of symptoms")
    causes = models.JSONField(default=list, help_text="List of causes")
    treatment = models.TextField(blank=True, help_text="Treatment information")
    prevention = models.JSONField(default=list, help_text="Prevention measures")
    
    # Recommendations
    recommendations = models.TextField(blank=True)
    severity = models.CharField(max_length=50, blank=True, choices=[
        ('normal', 'Normal'),
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        base = f"EyeDetection #{self.id}"
        if self.user_id:
            return f"{base} ({self.user.get_username()}) - {self.disease}"
        return f"{base} - {self.disease}"
