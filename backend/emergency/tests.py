from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import MedicalProfile, EmergencyContact, EmergencyLog


class EmergencySOSTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="sos_user", password="TestPass123!")

    def post_sos(self, data, authenticated=False):
        if authenticated:
            self.client.force_authenticate(user=self.user)
        return self.client.post("/api/sos/", data, format="json")

    def test_valid_anonymous_sos_creates_log(self):
        response = self.post_sos({"lat": 22.3072, "lon": 73.1812, "accuracy": 8.5, "symptoms": ["chest pain"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EmergencyLog.objects.count(), 1)
        log = EmergencyLog.objects.get()
        self.assertIsNone(log.user)
        self.assertEqual(log.latitude, 22.3072)
        self.assertEqual(log.longitude, 73.1812)
        self.assertEqual(log.location_accuracy, 8.5)
        self.assertEqual(log.symptoms, ["chest pain"])
        self.assertEqual(log.status, "active")
        self.assertIn("maps.google.com", response.data["location"])

    def test_authenticated_sos_captures_medical_snapshot(self):
        MedicalProfile.objects.create(
            user=self.user, name="Test User", age=22, gender="Male",
            blood_group="O+", allergies="Peanuts", medications="None",
            conditions="Asthma"
        )
        EmergencyContact.objects.create(user=self.user, name="Parent", phone="9999999999")
        response = self.post_sos({"lat": 23.0, "lon": 72.5, "symptoms": ["breathing difficulty"]}, authenticated=True)
        self.assertEqual(response.status_code, 200)
        log = EmergencyLog.objects.get()
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.contacts_notified, 1)
        self.assertEqual(log.medical_snapshot["blood_group"], "O+")
        self.assertEqual(log.medical_snapshot["allergies"], "Peanuts")

    def test_missing_coordinates_rejected(self):
        response = self.post_sos({"symptoms": ["fever"]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(EmergencyLog.objects.count(), 0)

    def test_invalid_latitude_rejected(self):
        response = self.post_sos({"lat": 95, "lon": 73})
        self.assertEqual(response.status_code, 400)

    def test_invalid_longitude_rejected(self):
        response = self.post_sos({"lat": 22, "lon": 181})
        self.assertEqual(response.status_code, 400)

    def test_negative_valid_coordinates_accepted(self):
        response = self.post_sos({"lat": -22.3, "lon": -73.1})
        self.assertEqual(response.status_code, 200)

    def test_accuracy_cannot_be_negative(self):
        response = self.post_sos({"lat": 22.3, "lon": 73.1, "accuracy": -1})
        self.assertEqual(response.status_code, 400)

    def test_counts_cannot_be_negative(self):
        response = self.post_sos({"lat": 22.3, "lon": 73.1, "contacts_notified": -1})
        self.assertEqual(response.status_code, 400)

    def test_emergency_flags_are_saved(self):
        response = self.post_sos({"lat": 22.3, "lon": 73.1, "contacts_notified": 2, "hospitals_notified": 3, "emergency_services_called": True})
        self.assertEqual(response.status_code, 200)
        log = EmergencyLog.objects.get()
        self.assertEqual(log.contacts_notified, 2)
        self.assertEqual(log.hospitals_found, 3)
        self.assertTrue(log.emergency_services_called)

    def test_sos_message_contains_location(self):
        response = self.post_sos({"lat": 22.3072, "lon": 73.1812})
        self.assertEqual(response.status_code, 200)
        self.assertIn("22.3072,73.1812", response.data["message"])


class EmergencyEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="profile_user", password="TestPass123!")
        self.client.force_authenticate(user=self.user)

    def test_medical_profile_get_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/medical-profile/")
        self.assertEqual(response.status_code, 401)

    def test_medical_profile_get_creates_profile(self):
        response = self.client.get("/api/medical-profile/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["gender"], "")
        self.assertTrue(MedicalProfile.objects.filter(user=self.user).exists())

    def test_emergency_contacts_are_private(self):
        EmergencyContact.objects.create(user=self.user, name="Parent", phone="9999999999")
        other = User.objects.create_user(username="other", password="TestPass123!")
        EmergencyContact.objects.create(user=other, name="Other", phone="8888888888")
        response = self.client.get("/api/emergency-contacts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Parent")
