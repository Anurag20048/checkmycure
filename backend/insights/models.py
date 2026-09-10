from django.db import models
from django.contrib.auth.models import User

class SymptomLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
