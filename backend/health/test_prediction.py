from django.test import SimpleTestCase

from .prediction import detect_symptoms_in_text, predict_from_symptoms


class PredictionEngineTests(SimpleTestCase):
    def test_specific_symptom_phrase_is_canonicalized(self):
        symptoms = detect_symptoms_in_text("I have chest tightness and a dry cough")
        self.assertIn("chest pain", symptoms)
        self.assertIn("cough", symptoms)
        self.assertNotIn("pain", symptoms)

    def test_prediction_returns_safe_structure(self):
        result = predict_from_symptoms(["fever", "cough", "fatigue", "headache"])
        self.assertIn("prediction", result)
        self.assertIn("confidence", result)
        self.assertIn("probabilities", result)
        self.assertIsInstance(result["probabilities"], dict)

    def test_unknown_symptoms_do_not_invent_a_condition(self):
        result = predict_from_symptoms(["unknown symptom"])
        self.assertEqual(result["raw_prediction"], "unknown")
        self.assertEqual(result["confidence"], 0.0)
