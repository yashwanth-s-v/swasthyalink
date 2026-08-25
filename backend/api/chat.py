from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatSafety,
    RecommendedDoctor
)

from services.gemini_service import GeminiService
from services.safety_service import SafetyService
from services.ayurveda_service import AyurvedaService
from services.doctor_matching import DoctorMatchingService


router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


gemini_service = GeminiService()

safety_service = SafetyService()

ayurveda_service = AyurvedaService()

doctor_matching_service = (
    DoctorMatchingService()
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    user_message = request.message.strip()

    # ========================================================
    # SAFETY FIRST
    # ========================================================

    safety_result = safety_service.analyze(
        user_message
    )

    risk_level = safety_result.get(
        "risk_level",
        "unknown"
    )

    requires_doctor = safety_result.get(
        "requires_doctor",
        False
    )

    emergency = safety_result.get(
        "emergency",
        False
    )

    # ========================================================
    # GENERAL GUIDANCE
    # ========================================================

    guidance = ayurveda_service.get_guidance(
        user_message
    )

    # ========================================================
    # GEMINI
    # ========================================================

    ai_response = gemini_service.generate_response(
        user_message=user_message,
        safety_result=safety_result,
        guidance=guidance
    )

    # ========================================================
    # EMERGENCY
    # ========================================================

    if emergency:

        return ChatResponse(

            message=ai_response,

            safety=ChatSafety(
                risk_level=risk_level,
                requires_doctor=True,
                emergency=True
            ),

            doctor_recommended=False,

            recommended_doctors=[],

            next_step=(
                "Please seek urgent medical attention. "
                "This chatbot cannot safely handle "
                "emergency medical situations."
            )
        )

    # ========================================================
    # DOCTOR MATCHING
    # ========================================================

    recommended_doctors = []

    if requires_doctor:

        today = date.today()

        matches = (
            doctor_matching_service
            .get_fastest_available_doctors(
                db=db,
                message=user_message,
                target_date=today,
                consultation_type="any"
            )
        )

        for item in matches[:5]:

            doctor = item["doctor"]

            slots = item["available_slots"]

            earliest_slot = (
                slots[0]
                if slots
                else None
            )

            recommended_doctors.append(

                RecommendedDoctor(

                    doctor_id=doctor.id,

                    name=doctor.name,

                    specialization=(
                        doctor.specialization
                    ),

                    qualification=(
                        doctor.qualification
                    ),

                    hospital=doctor.hospital,

                    city=doctor.city,

                    experience_years=(
                        doctor.experience_years or 0
                    ),

                    is_government_doctor=(
                        doctor.is_government_doctor
                    ),

                    is_verified=(
                        doctor.is_verified
                    ),

                    consultation_type=(
                        doctor.consultation_type
                        or "appointment"
                    ),

                    match_score=item["score"],

                    earliest_slot=earliest_slot
                )
            )

    # ========================================================
    # NEXT STEP
    # ========================================================

    if recommended_doctors:

        next_step = (
            "A qualified Ayurvedic doctor is available. "
            "Choose a doctor to continue."
        )

    elif requires_doctor:

        next_step = (
            "A doctor consultation is recommended, "
            "but no suitable doctor is currently available."
        )

    else:

        next_step = (
            "You can continue with general wellness "
            "information. If symptoms persist or worsen, "
            "consult a qualified healthcare professional."
        )

    # ========================================================
    # RESPONSE
    # ========================================================

    return ChatResponse(

        message=ai_response,

        safety=ChatSafety(
            risk_level=risk_level,
            requires_doctor=requires_doctor,
            emergency=emergency
        ),

        doctor_recommended=requires_doctor,

        recommended_doctors=recommended_doctors,

        next_step=next_step
    )