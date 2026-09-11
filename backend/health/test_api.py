from django.urls import reverse
from rest_framework.test import APITestCase


class HealthApiTests(APITestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("health-status"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ok"], True)

    def test_predict_endpoint_rejects_non_list(self):
        response = self.client.post("/api/predict/", {"symptoms": "fever"}, format="json")
        self.assertEqual(response.status_code, 400)
