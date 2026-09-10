"""Pure-Python chatbot intent benchmark. No Django server or network required."""
from health.chatbot_service import generate_chatbot_response

CASES = {
    "fever": ["I have a fever", "my temperature is high", "feeling feverish"],
    "headache": ["I have a headache", "my head hurts", "pain in my head"],
    "cough": ["I keep coughing", "dry cough"],
    "cold": ["I caught a cold", "blocked nose and sneezing"],
    "stomach pain": ["my stomach hurts", "abdominal pain", "belly ache"],
    "nausea": ["I feel nauseous", "feeling sick"],
    "diarrhea": ["I have diarrhea", "loose motions"],
    "vomiting": ["I am vomiting", "throwing up"],
    "chest pain": ["my chest hurts", "chest pressure"],
    "breathing": ["I am short of breath"],
    "back pain": ["my back hurts", "backache"],
    "joint pain": ["my joints hurt", "joint ache"],
    "fatigue": ["I am exhausted", "extreme tiredness"],
    "dizziness": ["I feel dizzy", "the room is spinning"],
    "sore throat": ["my throat hurts", "sore throat"],
    "runny nose": ["my nose is running", "nasal discharge"],
    "body aches": ["my whole body hurts", "body ache"],
    "skin rash": ["I have a skin rash", "red itchy rash"],
    "ear pain": ["my ear hurts", "pain in my ear"],
    "eye pain": ["my eye hurts", "pain in my eye"],
    "toothache": ["my tooth hurts", "tooth pain"],
    "insomnia": ["I cannot sleep", "trouble sleeping"],
    "anxiety": ["I feel anxious", "constant worry"],
    "depression": ["I feel depressed", "persistent hopelessness"],
    "diabetes": ["could I have diabetes", "high blood sugar"],
    "blood pressure": ["my BP is high", "high blood pressure"],
    "allergies": ["I have an allergy", "sneezing due to pollen"],
    "constipation": ["I am constipated", "hard stool"],
    "weight loss": ["I am losing weight", "unexplained weight loss"],
    "irregular periods": ["my periods are irregular", "irregular menstrual cycle"],
}


HUMAN_SLANG_CASES = {
    "fever": ["im running a temp", "got a high temp", "body feels hot n feverish", "bukhar hai"],
    "headache": ["my head is killing me", "head is banging", "got a bad head pain", "sir dard ho raha"],
    "cough": ["cant stop coughing", "been coughing like crazy", "coughing a lot"],
    "cold": ["got the sniffles", "nose blocked and sneezing", "down with a cold"],
    "stomach pain": ["my tummy hurts", "belly is hurting", "stomach is paining", "pet dard ho raha"],
    "nausea": ["feeling like puking", "feel sick to my stomach", "feels like vomiting"],
    "diarrhea": ["loose motions", "my stomach is running", "watery stools"],
    "vomiting": ["i keep throwing up", "puking a lot", "vomited twice"],
    "chest pain": ["chest is hurting", "pain in chest", "seene mein dard"],
    "breathing": ["cant catch my breath", "breathing feels hard", "saans lene mein dikkat"],
    "back pain": ["lower back is killing me", "back is aching", "kamar dard"],
    "joint pain": ["knees hurt", "my joints are aching", "ghutno mein dard"],
    "fatigue": ["feeling totally drained", "no energy at all", "bahut thakaan"],
    "dizziness": ["feeling giddy", "head feels woozy", "chakkar aa raha"],
    "sore throat": ["throat is killing me", "pain when swallowing", "gala dard"],
    "runny nose": ["nose wont stop running", "constant runny nose", "naak beh rahi"],
    "body aches": ["everything in my body aches", "body is sore all over", "poora badan dard"],
    "skin rash": ["breaking out in a rash", "skin is super itchy and red", "skin pe daane"],
    "ear pain": ["ear is killing me", "my ear is aching", "kaan mein dard"],
    "eye pain": ["eyes hurt", "my eye is killing me", "aankh mein dard"],
    "toothache": ["tooth is killing me", "my tooth hurts bad", "daant mein dard"],
    "insomnia": ["cant get any sleep", "been up all night", "sleep is messed up"],
    "anxiety": ["feeling really anxious", "my mind wont stop racing", "bahut ghabrahat"],
    "depression": ["feeling really low lately", "nothing feels good anymore", "feeling hopeless"],
    "diabetes": ["sugar is high", "blood sugar is up", "my sugar is high"],
    "blood pressure": ["bp is shooting up", "pressure is high", "my bp is bad"],
    "allergies": ["allergy acting up", "pollen is messing me up", "allergic reaction"],
    "constipation": ["cant poop", "havent pooped in days", "stool is stuck"],
    "weight loss": ["losing weight without trying", "dropping weight for no reason", "weight keeps going down"],
    "irregular periods": ["periods are all over the place", "cycle is messed up", "periods not coming regularly"],
}


def main():
    total = passed = 0
    failures = []
    for expected, messages in CASES.items():
        for message in messages:
            total += 1
            result = generate_chatbot_response(message)
            actual = result.get("topic") if result.get("intent") == "health_information" else result.get("intent")
            if actual == expected:
                passed += 1
            else:
                failures.append((message, expected, actual))

    typo_cases = {
        "fever": ["fevr", "feever"],
        "headache": ["hedache", "headche"],
        "stomach pain": ["stomak pain", "stomache pain"],
        "dizziness": ["dizzyy", "dizzyness"],
        "constipation": ["constipatedd", "constiption"],
        "diabetes": ["diabetis"],
        "allergies": ["allergys"],
    }
    typo_total = typo_passed = 0
    for expected, messages in typo_cases.items():
        for message in messages:
            typo_total += 1
            result = generate_chatbot_response(message)
            actual = result.get("topic") if result.get("intent") == "health_information" else result.get("intent")
            if actual == expected:
                typo_passed += 1
            else:
                failures.append((message, expected, actual))

    safety_cases = [
        ("I don't have fever", "general"),
        ("I do not have chest pain", "general"),
        ("I have no cough", "general"),
        ("I do not have severe chest pain", "general"),
        ("severe chest pain and difficulty breathing", "emergency"),
        ("yaar saans nahi aa rahi", "emergency"),
        ("bro seene mein bahut dard hai", "emergency"),
    ]
    slang_total = slang_passed = 0
    for expected, messages in HUMAN_SLANG_CASES.items():
        for message in messages:
            slang_total += 1
            result = generate_chatbot_response(message)
            actual = result.get("topic") if result.get("intent") == "health_information" else result.get("intent")
            if actual == expected:
                slang_passed += 1
            else:
                failures.append((message, expected, actual))

    safety_passed = 0
    for message, expected_intent in safety_cases:
        actual = generate_chatbot_response(message).get("intent")
        if actual == expected_intent:
            safety_passed += 1
        else:
            failures.append((message, expected_intent, actual))

    print(f"TOPIC BENCHMARK: {passed}/{total} = {passed / total * 100:.1f}%")
    print(f"HUMAN/SLANG BENCHMARK: {slang_passed}/{slang_total} = {slang_passed / slang_total * 100:.1f}%")
    print(f"SPELLING-ERROR CASES: {typo_passed}/{typo_total} = {typo_passed / typo_total * 100:.1f}%")
    print(f"SAFETY/EMERGENCY CASES: {safety_passed}/{len(safety_cases)} = {safety_passed / len(safety_cases) * 100:.1f}%")
    if failures:
        print("FAILURES:")
        for item in failures:
            print(" -", item)
        raise SystemExit(1)
    print("CHATBOT BENCHMARK: PASS")


if __name__ == "__main__":
    main()
