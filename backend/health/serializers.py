from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, SymptomCheck


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    gender = serializers.ChoiceField(choices=[("male", "Male"), ("female", "Female"), ("others", "Others")], required=False, allow_blank=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["full_name"]


class SymptomCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymptomCheck
        fields = [
            "id",
            "user",
            "symptoms",
            "age",
            "gender",
            "medical_history",
            "prediction",
            "confidence",
            "created_at",
        ]
        read_only_fields = ["id", "user", "prediction", "confidence", "created_at"]
