from django.test import SimpleTestCase
from rest_framework.test import APIClient
from unittest.mock import patch

class EyeChatTests(SimpleTestCase):
    def test_empty(self):
        self.assertEqual(APIClient().post('/api/eye-chat/', {}, format='json').status_code, 400)

    def test_local_fallback(self):
        with patch('health.views.requests.post', side_effect=Exception('offline')):
            r = APIClient().post('/api/eye-chat/', {'message': 'meri aankh red hai'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['source'], 'local_fallback')
        self.assertEqual(r.data['intent'], 'eye_redness')

    def test_emergency(self):
        with patch('health.views.requests.post', side_effect=Exception('offline')):
            r = APIClient().post('/api/eye-chat/', {'message': 'sudden loss of vision'}, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['intent'], 'emergency_eye')
