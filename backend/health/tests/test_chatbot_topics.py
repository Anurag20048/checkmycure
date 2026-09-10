from django.test import SimpleTestCase
from health.chatbot_service import generate_chatbot_response


class ChatbotTopicCoverageTests(SimpleTestCase):
    cases = {
        "fever": "fever",
        "headache": "headache",
        "cough": "cough",
        "cold": "cold",
        "stomach pain": "stomach pain",
        "nausea": "nausea",
        "diarrhea": "diarrhea",
        "vomiting": "vomiting",
        "chest pain": "chest pain",
        "breathing difficulty": "breathing",
        "back pain": "back pain",
        "joint pain": "joint pain",
        "fatigue": "fatigue",
        "dizziness": "dizziness",
        "sore throat": "sore throat",
        "runny nose": "runny nose",
        "body aches": "body aches",
        "skin rash": "skin rash",
        "ear pain": "ear pain",
        "eye pain": "eye pain",
        "toothache": "toothache",
        "insomnia": "insomnia",
        "anxiety": "anxiety",
        "depression": "depression",
        "diabetes": "diabetes",
        "blood pressure": "blood pressure",
        "allergies": "allergies",
        "constipation": "constipation",
        "weight loss": "weight loss",
        "irregular periods": "irregular periods",
    }

    def test_each_topic_is_relevant(self):
        for message, expected_topic in self.cases.items():
            with self.subTest(message=message):
                result = generate_chatbot_response(message)
                self.assertEqual(result.get("topic"), expected_topic)
                self.assertNotIn("I can provide general health information about symptoms", result["response"])

    def test_emergency_stays_priority(self):
        result = generate_chatbot_response("I have severe chest pain and difficulty breathing")
        self.assertEqual(result["intent"], "emergency")
        self.assertIn("112", result["response"])

    def test_unknown_does_not_guess_a_disease(self):
        result = generate_chatbot_response("I feel strange")
        self.assertEqual(result["intent"], "general")
        self.assertNotIn("Possible condition suggestion", result["response"])
    def test_natural_language_variants(self):
        cases = {
            "my temperature is high": "fever",
            "my head hurts": "headache",
            "I keep coughing": "cough",
            "blocked nose and sneezing": "cold",
            "my stomach hurts": "stomach pain",
            "I feel nauseous": "nausea",
            "loose motions": "diarrhea",
            "throwing up": "vomiting",
            "my chest hurts": "chest pain",
            "I am short of breath": "breathing",
            "my back hurts": "back pain",
            "my joints hurt": "joint pain",
            "I am exhausted": "fatigue",
            "the room is spinning": "dizziness",
            "my throat hurts": "sore throat",
            "my nose is running": "runny nose",
            "my whole body hurts": "body aches",
            "red itchy rash": "skin rash",
            "my ear hurts": "ear pain",
            "my eye hurts": "eye pain",
            "my tooth hurts": "toothache",
            "I cannot sleep": "insomnia",
            "I feel anxious": "anxiety",
            "I feel depressed": "depression",
            "high blood sugar": "diabetes",
            "my BP is high": "blood pressure",
            "sneezing due to pollen": "allergies",
            "I am constipated": "constipation",
            "I am losing weight": "weight loss",
            "my periods are irregular": "irregular periods",
        }
        for message, expected_topic in cases.items():
            with self.subTest(message=message):
                result = generate_chatbot_response(message)
                self.assertEqual(result.get("topic"), expected_topic)

    def test_negated_symptoms_are_not_reported_as_active_topics(self):
        for message in ("I don't have fever", "I do not have chest pain", "I have no cough"):
            with self.subTest(message=message):
                result = generate_chatbot_response(message)
                self.assertEqual(result["intent"], "general")

    def test_negated_emergency_phrase_does_not_trigger_emergency(self):
        result = generate_chatbot_response("I do not have severe chest pain")
        self.assertNotEqual(result["intent"], "emergency")

