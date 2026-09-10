from django.contrib import admin

from .models import Profile, SymptomCheck, EyeDetection


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "full_name", "gender"]
    search_fields = ["user__username", "user__email", "full_name"]


@admin.register(SymptomCheck)
class SymptomCheckAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "prediction", "confidence", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "prediction"]


@admin.register(EyeDetection)
class EyeDetectionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "disease", "confidence", "severity", "created_at"]
    list_filter = ["severity", "created_at"]
    search_fields = ["user__username", "disease"]
    readonly_fields = ["created_at", "original_image", "processed_image"]
