import sys
from pathlib import Path

# Allow running this pure unit test without Django.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from health.chatbot_service import generate_chatbot_response


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"[PASS] {name}")


def main():
    cases = [
        ("empty message", "", "Please enter"),
        ("greeting", "hello", "Hello!"),
        ("fever", "I have fever", "Fever"),
        ("cough", "I have a cough", "cough"),
        ("headache", "I have headache", "Headaches"),
        ("cold", "I have a cold", "Cold symptoms"),
        ("stomach", "I have stomach pain", "stomach"),
        ("medication", "Can I take medicine?", "cannot prescribe"),
        ("clinic", "I need a doctor", "Find Nearby Clinics"),
        ("multi symptom", "I have fever and cough", "Fever"),
        ("emergency priority", "I have severe chest pain and fever", "emergency"),
        ("unknown", "Tell me about hydration", "I do not want to guess"),
    ]
    for name, message, expected in cases:
        result = generate_chatbot_response(message)
        check(name, expected.lower() in result["response"].lower())
        check(name + " returns language", result["language"] == "en")
        check(name + " returns intent", bool(result.get("intent")))
    print("CHATBOT UNIT TESTS: PASS")


if __name__ == "__main__":
    main()
