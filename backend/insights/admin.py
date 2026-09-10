from django.contrib import admin
from .models import SymptomLog


@admin.register(SymptomLog)
class SymptomLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'symptom', 'created_at']
    list_filter = ['created_at', 'symptom']
    search_fields = ['user__username', 'symptom']
