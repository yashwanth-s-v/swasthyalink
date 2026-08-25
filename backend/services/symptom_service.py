import re


SYMPTOM_KEYWORDS = {
    "headache": [
        "headache",
        "head pain",
        "pain in my head"
    ],
    "fever": [
        "fever",
        "temperature",
        "high temperature"
    ],
    "cough": [
        "cough",
        "coughing"
    ],
    "cold": [
        "cold",
        "runny nose",
        "blocked nose",
        "stuffy nose"
    ],
    "sore throat": [
        "sore throat",
        "throat pain",
        "pain in my throat"
    ],
    "stomach pain": [
        "stomach pain",
        "stomach ache",
        "pain in my stomach",
        "abdominal pain"
    ],
    "bloating": [
        "bloating",
        "bloated",
        "stomach feels full"
    ],
    "acidity": [
        "acidity",
        "acid reflux",
        "heartburn",
        "burning in chest"
    ],
    "indigestion": [
        "indigestion",
        "difficulty digesting",
        "food not digesting"
    ],
    "nausea": [
        "nausea",
        "feeling nauseous",
        "feel like vomiting"
    ],
    "vomiting": [
        "vomiting",
        "vomited",
        "throwing up"
    ],
    "diarrhea": [
        "diarrhea",
        "loose motions",
        "loose stools"
    ],
    "constipation": [
        "constipation",
        "constipated",
        "difficulty passing stool"
    ],
    "fatigue": [
        "fatigue",
        "very tired",
        "extremely tired",
        "tiredness"
    ],
    "weakness": [
        "weakness",
        "feeling weak",
        "very weak"
    ],
    "dizziness": [
        "dizziness",
        "dizzy",
        "light headed",
        "lightheaded"
    ],
    "joint pain": [
        "joint pain",
        "pain in my joints"
    ],
    "back pain": [
        "back pain",
        "pain in my back"
    ]
}


def extract_symptoms(message: str) -> list[str]:

    text = message.lower()

    detected_symptoms = []

    for symptom, keywords in SYMPTOM_KEYWORDS.items():

        for keyword in keywords:

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                text
            ):

                detected_symptoms.append(symptom)

                break

    return detected_symptoms