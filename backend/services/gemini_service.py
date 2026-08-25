from google import genai

from config import settings


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = "gemini-3.6-flash"

    def generate_response(
        self,
        user_message: str,
        safety_result: dict,
        guidance: dict
    ):

        risk_level = safety_result.get(
            "risk_level",
            "unknown"
        )

        emergency = safety_result.get(
            "emergency",
            False
        )

        requires_doctor = safety_result.get(
            "requires_doctor",
            False
        )

        prompt = f"""
You are AyurConnect's general Ayurveda wellness assistant.

You are NOT a doctor.

Your purpose is to provide general educational
wellness information and help users connect with
qualified healthcare professionals.

USER MESSAGE:
{user_message}

SAFETY RESULT:
{risk_level}

REQUIRES DOCTOR:
{requires_doctor}

EMERGENCY:
{emergency}

GENERAL AYURVEDA GUIDANCE:
{guidance}

STRICT RULES:

- Never diagnose a disease.
- Never claim certainty about the user's condition.
- Never prescribe medicines.
- Never give medicine dosage.
- Never tell users to stop prescribed medicines.
- Never replace a doctor.
- Never make emergency cases sound safe.
- Never contradict the safety assessment.
- Do not promise that food or Ayurveda will cure a disease.

If the safety result is urgent:
Clearly recommend prompt professional medical evaluation.

If the safety result is emergency:
Tell the user to seek urgent medical attention.
Do not give lengthy home remedies.

If the safety result requires a doctor:
Encourage consultation with a qualified doctor.

If the situation is general:
Give simple, conservative wellness information.

Keep the response friendly, concise and easy to understand.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text