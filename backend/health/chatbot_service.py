"""Safe, deterministic health-information chatbot.

This service is intentionally informational. It does not diagnose disease or
prescribe medication. Responses are matched to the user's topic so the bot
stays relevant instead of returning a generic message for known symptoms.
"""
from .prediction import detect_symptoms_in_text


TOPIC_RESPONSES = {
    "fever": "Fever is a rise in body temperature and can happen with infections or other causes. Rest, drink fluids, and monitor your temperature. Seek medical care for a very high or persistent fever, severe weakness, confusion, stiff neck, trouble breathing, or worsening symptoms.",
    "headache": "Headaches can have many causes, including stress, dehydration, lack of sleep, or migraine. Rest, hydrate, and avoid known triggers. Get urgent medical help for a sudden, extremely severe headache or headache with weakness, confusion, fainting, seizures, vision changes, or trouble speaking.",
    "cough": "A cough can occur with a cold, infection, allergies, asthma, or irritation. Drink fluids and avoid smoke or other irritants. Seek medical care if the cough is severe, persistent, associated with chest pain, coughing blood, or breathing difficulty.",
    "cold": "Cold symptoms such as a runny or blocked nose, sneezing, sore throat, and cough often improve with rest and fluids. Seek care if symptoms are severe, keep getting worse, or cause breathing difficulty.",
    "stomach pain": "Stomach or abdominal pain has many possible causes. Note where the pain is, when it started, and whether vomiting, diarrhea, fever, or other symptoms are present. Seek urgent care for severe or worsening pain, a rigid abdomen, fainting, blood in vomit or stool, or persistent vomiting.",
    "nausea": "For nausea, take small frequent sips of water or an oral rehydration drink and choose light foods when you can tolerate them. Seek care for repeated vomiting, severe abdominal pain, blood, confusion, or signs of dehydration.",
    "diarrhea": "Diarrhea can cause dehydration. Drink water or oral rehydration solution and eat light foods as tolerated. Seek medical care for blood or black stool, severe abdominal pain, high fever, severe dehydration, or diarrhea that persists.",
    "vomiting": "Repeated vomiting can lead to dehydration. Take small sips of water or oral rehydration solution rather than drinking a large amount at once. Seek urgent care for blood or coffee-ground-like vomit, severe pain, confusion, fainting, or inability to keep fluids down.",
    "chest pain": "Chest pain should be taken seriously. If it is severe, new, pressure-like, spreading to the arm, jaw, back, or accompanied by sweating, nausea, fainting, or breathing difficulty, call 112 in India or your local emergency service immediately.",
    "breathing": "Breathing difficulty can be an emergency. If you are struggling to breathe, cannot speak normally because of breathlessness, have blue or grey lips, severe chest pain, confusion, or sudden worsening, call 112 in India or your local emergency service now.",
    "back pain": "Back pain can result from muscle strain and many other causes. Gentle movement and avoiding activities that worsen pain may help. Seek urgent care for new weakness or numbness, loss of bladder or bowel control, fever with severe back pain, major injury, or rapidly worsening pain.",
    "joint pain": "Joint pain can follow overuse, injury, inflammation, or infection. Rest the affected joint from aggravating activity and monitor swelling and movement. Seek care for a hot, very swollen joint, fever, major injury, or inability to use the joint.",
    "fatigue": "Fatigue can be related to sleep, stress, illness, nutrition, medicines, or other conditions. Consider sleep, hydration, food intake, and recent changes. If fatigue is severe, persistent, or comes with unexplained weight loss, fainting, chest pain, or breathing difficulty, see a clinician.",
    "dizziness": "Dizziness can have several causes, including dehydration, low blood pressure, inner-ear problems, or medication effects. Sit or lie down if you feel faint and rise slowly. Get urgent help for fainting, severe headache, chest pain, weakness, trouble speaking, or new difficulty walking.",
    "sore throat": "A sore throat is commonly associated with viral infections but can have other causes. Drink fluids and use soothing warm liquids if comfortable. Seek care for difficulty breathing or swallowing, drooling, severe swelling, dehydration, or symptoms that are severe or persistent.",
    "runny nose": "A runny nose commonly occurs with a cold or allergies. Fluids, rest, and avoiding known irritants may help. Seek care if symptoms are severe, persistent, or accompanied by breathing difficulty or significant facial pain/swelling.",
    "body aches": "Body aches can happen with infections, exertion, stress, or other conditions. Rest, hydrate, and monitor for fever or other symptoms. Seek medical care if pain is severe, unexplained, follows major injury, or occurs with weakness, confusion, or breathing difficulty.",
    "skin rash": "A skin rash can have many causes, including irritation, allergy, infection, or medication reactions. Avoid suspected irritants and monitor changes. Seek urgent care for a rapidly spreading rash, facial or tongue swelling, breathing difficulty, blistering, or a rash with severe illness.",
    "ear pain": "Ear pain can be related to infection, congestion, irritation, or dental or jaw problems. Avoid putting objects or unprescribed drops into the ear. Seek care for severe pain, fever, discharge, hearing loss, swelling around the ear, or symptoms that persist.",
    "eye pain": "Eye pain should be evaluated carefully because causes range from irritation to conditions needing urgent treatment. Avoid rubbing the eye. Seek urgent medical care for severe pain, sudden vision loss or change, significant redness with pain, injury, chemical exposure, or light sensitivity with severe symptoms.",
    "toothache": "A toothache may come from decay, gum problems, infection, or injury. Keep the area clean and arrange a dental evaluation. Seek urgent care for facial swelling, fever, difficulty swallowing or breathing, or rapidly worsening pain.",
    "insomnia": "Insomnia means difficulty falling asleep, staying asleep, or getting restorative sleep. Keep a regular sleep schedule, reduce caffeine late in the day, and limit screens close to bedtime. See a clinician if sleep problems persist or seriously affect daytime function.",
    "anxiety": "Anxiety can cause worry, restlessness, rapid heartbeat, and other physical symptoms. Slow breathing, regular sleep, movement, and talking to someone you trust can help. If anxiety is overwhelming, persistent, or interfering with daily life, consider speaking with a mental-health professional. If you may harm yourself, seek emergency help immediately.",
    "depression": "Depression can involve persistent low mood, loss of interest, changes in sleep or appetite, low energy, or hopelessness. Support from a mental-health professional can help. If you are thinking about self-harm or suicide, contact emergency services or a crisis service immediately and stay with someone you trust.",
    "diabetes": "Diabetes is a condition involving high blood glucose. Common warning signs can include increased thirst, frequent urination, fatigue, and unexplained weight loss, but symptoms alone cannot confirm diabetes. A clinician can diagnose it using appropriate blood tests. Seek urgent help for confusion, severe weakness, vomiting, or difficulty breathing.",
    "blood pressure": "High blood pressure often has no obvious symptoms, so it is usually identified by measurement rather than how you feel. If you have a reading that is very high, repeat it after resting and seek medical advice. Very high readings with chest pain, severe headache, breathing difficulty, weakness, or confusion require urgent care.",
    "allergies": "Allergies can cause sneezing, runny nose, itching, rash, or other symptoms. Avoid known triggers when possible. Sudden swelling of the lips, tongue, or throat, wheezing, or difficulty breathing can be a severe allergic reaction and requires emergency care.",
    "constipation": "Constipation can improve with enough fluids, dietary fiber, and regular movement when appropriate. Seek medical care for severe or persistent abdominal pain, vomiting, blood in stool, marked swelling, or inability to pass stool or gas.",
    "weight loss": "Unintentional weight loss can have many causes, including diet changes, stress, digestive problems, or medical conditions. If weight loss is unexplained, significant, or continuing, arrange a medical evaluation rather than relying on symptoms alone.",
    "irregular periods": "Irregular periods can occur with stress, weight changes, hormonal conditions, some medicines, pregnancy, and other causes. Track cycle dates and related symptoms. A clinician can help determine the cause, especially if irregularity is new, persistent, associated with very heavy bleeding, severe pain, or possible pregnancy.",
}


def _contains(text, phrase):
    """Phrase match with a small negation guard for symptom statements."""
    import re
    for match in re.finditer(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text):
        prefix = text[max(0, match.start() - 24):match.start()].strip()
        if re.search(r"\b(no|not|don't|dont|do not|doesn't|doesnt|without|never)\b(?:\s+\w+){0,3}\s*$", prefix):
            continue
        return True
    return False


# Natural-language aliases improve topic recognition without pretending that
# the bot can diagnose a disease from symptoms.
TOPIC_ALIASES = {
    "fever": ("fever", "fevr", "feever", "feverish", "high temperature", "temperature is high", "temperature's high", "running a temperature", "running a temp", "high temp", "got a temp", "feelin feverish", "feeling feverish", "bukhar", "bukhar hai"),
    "headache": ("headache", "head ache", "hedache", "headche", "head hurts", "head is hurting", "pain in my head", "pain in the head", "head is killing me", "head is banging", "bad head pain", "head pain", "sir dard", "sir dard ho raha"),
    "cough": ("cough", "coughh", "cof", "coughing", "keep coughing", "dry cough", "wet cough", "cant stop coughing", "can't stop coughing", "coughing like crazy", "coughing a lot"),
    "cold": ("cold", "caught a cold", "blocked nose", "stuffy nose", "sneezing and runny nose", "sniffles", "got the sniffles", "down with a cold", "nose blocked and sneezing"),
    "stomach pain": ("stomach pain", "stomak pain", "stomache pain", "stomachpain", "stomach hurts", "stomach ache", "stomach is paining", "belly ache", "belly hurts", "belly is hurting", "tummy hurts", "tummy pain", "abdominal pain", "abdominal ache", "pet dard", "pet dard ho raha"),
    "nausea": ("nausea", "nauseous", "feeling sick", "feel sick", "queasy", "feeling like puking", "feel like puking", "feels like vomiting", "feel like vomiting"),
    "diarrhea": ("diarrhea", "diarrhoea", "loose motions", "loose stools", "watery stools", "stomach is running", "running stomach", "watery poop"),
    "vomiting": ("vomiting", "vomit", "throwing up", "threw up", "keep throwing up", "puking", "puking a lot", "keep puking", "vomited twice", "vomited", "throwing up a lot"),
    "chest pain": ("chest pain", "chest hurts", "chest is hurting", "chest ache", "chest pressure", "chest tightness", "pain in chest", "seene mein dard", "seene me dard", "seene mein bahut dard"),
    "breathing": ("difficulty breathing", "shortness of breath", "short of breath", "breathlessness", "can't breathe", "cannot breathe", "trouble breathing", "cant catch my breath", "can't catch my breath", "breathing feels hard", "saans lene mein dikkat", "saans nahi aa rahi", "saans nahi aati"),
    "back pain": ("back pain", "back hurts", "backache", "back is aching", "lower back pain", "upper back pain", "lower back is killing me", "kamar dard", "kamar mein dard"),
    "joint pain": ("joint pain", "joint hurts", "joints hurt", "joints are aching", "joint ache", "painful joints", "knees hurt", "knee pain", "ghutno mein dard", "ghutne mein dard"),
    "fatigue": ("fatigue", "tired", "very tired", "extreme tiredness", "exhausted", "no energy", "low energy", "totally drained", "feeling totally drained", "bahut thakaan", "bahut thakan", "no strength"),
    "dizziness": ("dizziness", "dizzyy", "dizzyness", "dizzy", "feel dizzy", "feeling giddy", "room is spinning", "head feels woozy", "spinning sensation", "lightheaded", "light-headed", "chakkar", "chakkar aa raha", "feeling woozy"),
    "sore throat": ("sore throat", "throat hurts", "throat pain", "painful throat", "throat is killing me", "pain when swallowing", "gala dard", "gale mein dard"),
    "runny nose": ("runny nose", "nose is running", "nasal discharge", "running nose", "nose wont stop running", "nose won't stop running", "constant runny nose", "naak beh rahi", "naak bah rahi"),
    "body aches": ("body aches", "body ache", "whole body hurts", "body pain", "muscle aches", "body is sore all over", "everything in my body aches", "poora badan dard", "poora badan dukh raha"),
    "skin rash": ("skin rash", "rash", "rashes", "itchy rash", "red rash", "breaking out in a rash", "skin is super itchy and red", "skin pe daane", "skin par daane", "red itchy skin"),
    "ear pain": ("ear pain", "ear hurts", "pain in my ear", "painful ear", "ear is killing me", "ear is aching", "my ear is aching", "kaan mein dard", "kaan me dard"),
    "eye pain": ("eye pain", "eye hurts", "pain in my eye", "painful eye", "eyes hurt", "my eye is killing me", "aankh mein dard", "aankh me dard"),
    "toothache": ("toothache", "tooth pain", "tooth hurts", "tooth ache", "tooth is killing me", "my tooth hurts bad", "daant mein dard", "daant me dard"),
    "insomnia": ("insomnia", "can't sleep", "cannot sleep", "cannot fall asleep", "trouble sleeping", "difficulty sleeping", "poor sleep", "cant get any sleep", "can't get any sleep", "been up all night", "sleep is messed up", "not getting sleep"),
    "anxiety": ("anxiety", "anxious", "feel anxious", "feeling anxious", "constant worry", "panic", "panic attack", "mind wont stop racing", "mind won't stop racing", "bahut ghabrahat", "ghabrahat", "feeling panicky"),
    "depression": ("depression", "depressed", "feel depressed", "feeling depressed", "hopeless", "persistent hopelessness", "low mood", "feeling really low lately", "nothing feels good anymore", "feeling hopeless", "feel empty all the time"),
    "diabetes": ("diabetes", "diabetis", "diabetic", "high blood sugar", "blood sugar is high", "sugar is high", "blood sugar is up", "sugar level is high", "my sugar is high"),
    "blood pressure": ("blood pressure", "bp", "high blood pressure", "low blood pressure", "blood pressure is high", "blood pressure is low", "bp is high", "bp is shooting up", "my bp is bad", "pressure is high", "bp high"),
    "allergies": ("allergies", "allergy", "allergys", "allergy", "allergic", "allergic reaction", "pollen allergy", "pollen", "hay fever", "allergy acting up", "pollen is messing me up", "allergic to"),
    "constipation": ("constipation", "constipatedd", "constiption", "constipated", "hard stool", "hard stools", "difficulty passing stool", "can't pass stool", "cant poop", "can't poop", "havent pooped in days", "haven't pooped in days", "stool is stuck", "not able to poop"),
    "weight loss": ("weight loss", "losing weight", "lost weight", "unexplained weight loss", "unintentional weight loss", "losing weight without trying", "dropping weight for no reason", "weight keeps going down", "weight is dropping"),
    "irregular periods": ("irregular periods", "irregular period", "period irregular", "periods are irregular", "menstrual cycle irregular", "irregular menstrual cycle", "irregular menstrual cycles", "periods are all over the place", "cycle is messed up", "periods not coming regularly", "period not regular", "cycle is irregular"),
}



def _topic_for(text, found):
    # Specific topics first. Use aliases before the generic prediction detector.
    for topic, phrases in TOPIC_ALIASES.items():
        if any(_contains(text, phrase) for phrase in phrases):
            return topic

    for topic in TOPIC_RESPONSES:
        if _contains(text, topic):
            return topic

    normalized = {x.lower() for x in found if _contains(text, x)}
    fallback = {
        "fever": {"fever"}, "headache": {"headache"}, "cough": {"cough"},
        "cold": {"cold"}, "nausea": {"nausea"}, "diarrhea": {"diarrhea", "diarrhoea"},
        "vomiting": {"vomit", "vomiting"}, "fatigue": {"fatigue", "tired"},
        "dizziness": {"dizziness"}, "constipation": {"constipation"},
        "anxiety": {"anxiety"}, "depression": {"depression"},
        "diabetes": {"diabetes"}, "allergies": {"allergies", "allergy"},
        "weight loss": {"weight loss"},
    }
    for topic, keys in fallback.items():
        if normalized & keys:
            return topic
    return None

def generate_chatbot_response(message: str, language: str = "en") -> dict:
    text = (message or "").strip()
    lower = text.lower()
    language = (language or "en").strip() or "en"

    if not text:
        return {"response": "Please enter a health question or symptom.", "language": language, "intent": "empty"}

    # Emergency checks must happen before all normal topics.
    emergency_terms = (
        "severe chest pain", "crushing chest pain", "difficulty breathing", "can't breathe",
        "cannot breathe", "heavy bleeding", "unconscious", "seizure", "stroke symptoms",
        "face drooping", "slurred speech", "saans nahi aa rahi", "saans nahi aati", "saans lene mein bahut dikkat", "seene mein bahut dard", "bahut chest pain", "suicidal", "kill myself", "self harm",
        "emergency", "dying",
    )
    if any(_contains(lower, term) for term in emergency_terms):
        return {
            "response": "🚨 This may be an emergency. Call 112 in India (or your local emergency service) or go to the nearest emergency department now. Do not rely on this chatbot for emergency care.",
            "language": language,
            "intent": "emergency",
        }

    greeting_only = lower in {"hi", "hello", "hey", "good morning", "good evening", "good afternoon"}
    if greeting_only:
        return {
            "response": "Hello! I can help with general health information. Tell me a symptom or health question, for example: 'I have a headache' or 'What should I know about diabetes?'",
            "language": language,
            "intent": "greeting",
        }

    found = detect_symptoms_in_text(lower)
    topic = _topic_for(lower, found)
    if topic:
        return {"response": TOPIC_RESPONSES[topic] + "\n\n⚠️ This is general information, not a diagnosis.", "language": language, "intent": "health_information", "topic": topic}

    if any(k in lower for k in ("medicine", "medication", "drug", "prescription", "tablet", "pill", "dose")):
        return {
            "response": "I can give general medication information, but I cannot prescribe or change a medicine or dose. Tell me the medicine name and what you want to know, or ask a doctor or pharmacist about the correct dose, interactions, and contraindications.",
            "language": language, "intent": "medication"
        }

    if any(k in lower for k in ("doctor", "hospital", "clinic", "appointment", "nearby")):
        return {
            "response": "If you need an in-person evaluation, use Check MyCure's Find Nearby Clinics feature to look for healthcare facilities near your location.",
            "language": language, "intent": "clinic"
        }

    return {
        "response": "I can help with general health information, but I do not want to guess about your condition. Please describe the symptom, how long you have had it, and any important related symptoms. For diagnosis or treatment, consult a qualified healthcare professional.",
        "language": language, "intent": "general"
    }
