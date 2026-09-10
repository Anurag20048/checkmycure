from rest_framework import status
from rest_framework.test import APITestCase


class ChatbotAPITests(APITestCase):
    url = "/api/chatbot/"

    def post(self, message, language="en"):
        return self.client.post(self.url, {"message": message, "language": language}, format="json")

    def test_empty_message_rejected(self):
        response = self.post("")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["intent"], "empty")

    def test_greeting(self):
        response = self.post("hello")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["intent"], "greeting")
        self.assertIn("Hello", response.data["response"])

    def test_single_symptom(self):
        response = self.post("I have fever")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["intent"], "health_information")
        self.assertIn("Fever", response.data["response"])

    def test_multi_symptom_health_information(self):
        response = self.post("I have fever and cough")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["intent"], "health_information")
        self.assertIn("Fever", response.data["response"])

    def test_emergency_has_priority_over_prediction(self):
        response = self.post("I have severe chest pain and fever")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["intent"], "emergency")
        self.assertIn("112", response.data["response"])

    def test_no_authentication_required(self):
        response = self.post("I have a cough")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_language_is_echoed(self):
        response = self.post("hello", language="hi")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["language"], "hi")
