from typing import List, Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):

    message: str


class ChatSafety(BaseModel):

    risk_level: str

    requires_doctor: bool

    emergency: bool


class RecommendedDoctor(BaseModel):

    doctor_id: int

    name: str

    specialization: str

    qualification: str

    hospital: Optional[str] = None

    city: Optional[str] = None

    experience_years: int = 0

    is_government_doctor: bool = False

    is_verified: bool = False

    consultation_type: str = "appointment"

    match_score: int = 0

    earliest_slot: Optional[str] = None


class ChatResponse(BaseModel):

    message: str

    safety: ChatSafety

    doctor_recommended: bool

    recommended_doctors: List[RecommendedDoctor]

    next_step: str