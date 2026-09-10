from __future__ import annotations

from dataclasses import dataclass
import re


SYMPTOM_KEYWORDS: list[str] = [
    "breathing difficulty",
    "chest pain",
    "stomach pain",
    "runny nose",
    "sore throat",
    "joint pain",
    "back pain",
    "skin rash",
    "ear pain",
    "eye pain",
    "toothache",
    "irregular periods",
    "blood pressure",
    "fever",
    "cough",
    "headache",
    "nausea",
    "fatigue",
    "pain",
    "tired",
    "vomit",
    "stomach",
    "cold",
    "diarrhea",
    "vomiting",
    "dizziness",
    "anxiety",
    "depression",
    "diabetes",
    "allergies",
    "constipation",
    "weight loss",
    "insomnia",
    "shortness of breath",
    "chest tightness",
    "wheezing",
    "palpitations",
    "swelling in legs",
    "rapid heartbeat",
    "sneezing",
    "blocked nose",
    "stuffy nose",
    "dry cough",
    "productive cough",
    "chest pressure",
    "rapid breathing",
]


SYMPTOM_CANONICAL = {
    "shortness of breath": "breathing difficulty",
    "chest tightness": "chest pain",
    "chest pressure": "chest pain",
    "wheezing": "breathing difficulty",
    "rapid breathing": "breathing difficulty",
    "blocked nose": "runny nose",
    "stuffy nose": "runny nose",
    "sneezing": "runny nose",
    "dry cough": "cough",
    "productive cough": "cough",
    "palpitations": "pain",
    "rapid heartbeat": "pain",
    "swelling in legs": "pain",
}


def canonicalize_symptoms(symptoms: list[str]) -> list[str]:
    return normalize_symptoms([SYMPTOM_CANONICAL.get(str(s).strip().lower(), str(s).strip().lower()) for s in symptoms])


@dataclass(frozen=True)
class DiseaseRule:
    name: str
    symptoms: set[str]
    base_confidence: float
    advice: str


DISEASE_RULES: list[DiseaseRule] = [
    DiseaseRule(
        name="Breathing-related concern",
        symptoms={"breathing difficulty", "chest pain"},
        base_confidence=0.55,
        advice=(
            "Breathing difficulty or chest symptoms need clinical assessment. If you are struggling to breathe, "
            "have severe chest pain, blue or grey lips, confusion, fainting, or sudden worsening, seek emergency care immediately."
        ),
    ),
    DiseaseRule(
        name="Upper respiratory symptom concern",
        symptoms={"runny nose", "cough"},
        base_confidence=0.60,
        advice=(
            "Runny nose and cough can have several causes. Rest, hydrate, and monitor symptoms. "
            "Seek care if symptoms become severe, persist, or cause breathing difficulty."
        ),
    ),
    DiseaseRule(
        name="Common Cold",
        symptoms={"cough", "headache", "fatigue", "fever"},
        base_confidence=0.75,
        advice=(
            "Rest, drink plenty of fluids, and consider over-the-counter cold medicines. "
            "If symptoms worsen or persist, consult a healthcare professional."
        ),
    ),
    DiseaseRule(
        name="Influenza (Flu)",
        symptoms={"fever", "cough", "fatigue", "headache", "pain"},
        base_confidence=0.80,
        advice=(
            "Get plenty of rest, stay hydrated, and consider medical advice if caught early. "
            "Seek urgent care for difficulty breathing, chest pain, or severe symptoms."
        ),
    ),
    DiseaseRule(
        name="Gastroenteritis (Stomach Flu)",
        symptoms={"nausea", "vomit", "stomach", "fatigue"},
        base_confidence=0.78,
        advice=(
            "Stay hydrated (oral rehydration solutions can help). Eat bland foods when you can. "
            "Seek medical care if you can't keep fluids down or symptoms are severe."
        ),
    ),
    DiseaseRule(
        name="Migraine",
        symptoms={"headache", "nausea", "fatigue"},
        base_confidence=0.72,
        advice=(
            "Rest in a dark, quiet room. Hydrate and consider over-the-counter pain relief. "
            "If headaches are frequent or severe, consult a clinician."
        ),
    ),
    DiseaseRule(
        name="Tension Headache",
        symptoms={"headache", "pain", "fatigue"},
        base_confidence=0.70,
        advice=(
            "Try stress reduction, hydration, gentle stretching, and OTC pain relief. "
            "Seek care if severe, sudden, or persistent."
        ),
    ),
    DiseaseRule(
        name="Upper Respiratory Infection",
        symptoms={"cough", "fever", "fatigue", "headache"},
        base_confidence=0.76,
        advice=(
            "Rest, hydrate, use a humidifier, and consider OTC symptom relief. "
            "See a doctor if symptoms worsen or do not improve."
        ),
    ),
    DiseaseRule(
        name="Food Poisoning",
        symptoms={"nausea", "vomit", "stomach", "fever"},
        base_confidence=0.74,
        advice=(
            "Hydrate, rest, and avoid heavy foods. Seek care if there is severe dehydration, "
            "blood in stool, or high fever."
        ),
    ),
    DiseaseRule(
        name="Viral Infection",
        symptoms={"fever", "fatigue", "headache", "pain"},
        base_confidence=0.68,
        advice=(
            "Rest and hydrate. Use OTC medications for symptom relief as directed. "
            "Consult a healthcare professional if symptoms are severe or persist."
        ),
    ),
    DiseaseRule(
        name="COVID-19",
        symptoms={"fever", "cough", "fatigue", "headache"},
        base_confidence=0.70,
        advice=(
            "Consider testing for COVID-19 and follow local guidance. Isolate if needed and monitor symptoms. "
            "Seek urgent care for difficulty breathing, chest pain, or confusion."
        ),
    ),
]


def normalize_symptoms(symptoms: list[str]) -> list[str]:
    cleaned: list[str] = []
    for s in symptoms:
        if not isinstance(s, str):
            continue
        v = s.strip().lower()
        if v and v not in cleaned:
            cleaned.append(v)
    return cleaned


def predict_from_symptoms(symptoms: list[str]) -> dict:
    """Rule-based prediction (kept intentionally simple & runnable without ML libs)."""

    s = set(canonicalize_symptoms(symptoms))

    scored: list[tuple[DiseaseRule, float, set[str]]] = []
    for rule in DISEASE_RULES:
        matches = rule.symptoms.intersection(s)
        if not matches:
            continue
        match_ratio = len(matches) / max(len(rule.symptoms), 1)
        score = match_ratio * rule.base_confidence
        scored.append((rule, score, matches))

    scored.sort(key=lambda x: x[1], reverse=True)

    if not scored:
        return {
            "prediction": "General health concern",
            "raw_prediction": "unknown",
            "confidence": 0.0,
            "probabilities": {},
            "suggestions": [
                "Use the Symptom Checker with more details",
                "Consult a healthcare professional for a proper diagnosis",
            ],
        }

    best_rule, best_score, _matches = scored[0]

    # Convert scores to a probability-like distribution for top 5
    top = scored[:5]
    total = sum(score for _r, score, _m in top) or 1.0
    probabilities = {r.name: score / total for r, score, _m in top}

    suggestions = [
        best_rule.advice,
        "If symptoms are severe, worsening, or include breathing difficulty, seek urgent medical attention.",
        "Stay hydrated and rest.",
    ]

    return {
        "prediction": best_rule.name,
        "raw_prediction": best_rule.name,
        "confidence": float(round(best_score, 4)),
        "probabilities": probabilities,
        "suggestions": suggestions,
    }


def detect_symptoms_in_text(message: str) -> list[str]:
    lower = (message or "").lower()
    found: list[str] = []
    for keyword in SYMPTOM_KEYWORDS:
        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
        if re.search(pattern, lower):
            found.append(keyword)

    # Prefer specific phrases over shorter overlapping symptom tokens.
    # Example: "stomach pain" should produce only "stomach pain", not
    # both "stomach pain" and the shorter generic "stomach"/"pain" terms.
    specific_phrases = sorted(
        [item for item in found if " " in item],
        key=len,
        reverse=True,
    )
    for phrase in specific_phrases:
        found = [
            item for item in found
            if item == phrase or item not in phrase.split()
        ]

    # "vomiting" and "vomit" describe the same symptom for rule matching.
    if "vomiting" in found and "vomit" in found:
        found.remove("vomit")

    return normalize_symptoms(found)
