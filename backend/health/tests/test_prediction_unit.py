from django.test import SimpleTestCase

from health.prediction import detect_symptoms_in_text, predict_from_symptoms


class PredictionUnitTests(SimpleTestCase):
    def test_phrase_detection_does_not_double_count_generic_pain(self):
        self.assertEqual(detect_symptoms_in_text("stomach pain"), ["stomach pain"])

    def test_generic_stomach_is_still_detected(self):
        self.assertEqual(detect_symptoms_in_text("my stomach feels upset"), ["stomach"])

    def test_multiple_symptoms_are_detected(self):
        found = detect_symptoms_in_text("fever and cough")
        self.assertIn("fever", found)
        self.assertIn("cough", found)

    def test_prediction_is_deterministic(self):
        first = predict_from_symptoms(["fever", "cough"])
        second = predict_from_symptoms(["fever", "cough"])
        self.assertEqual(first, second)
        self.assertTrue(first["prediction"])
        self.assertGreaterEqual(first["confidence"], 0)
