from typing import List, Optional

from pydantic import BaseModel


# ============================================================
# DOCTOR CREATION
# ============================================================

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    qualification: str

    hospital: Optional[str] = None
    city: Optional[str] = None

    experience_years: int = 0

    is_government_doctor: bool = False
    is_verified: bool = False

    consultation_type: str = "appointment"

    is_available: bool = True


# ============================================================
# DOCTOR RESPONSE
# ============================================================

class DoctorResponse(BaseModel):
    id: int

    name: str
    specialization: str
    qualification: str

    hospital: Optional[str] = None
    city: Optional[str] = None

    experience_years: int

    is_government_doctor: bool
    is_verified: bool

    consultation_type: str

    is_available: bool

    class Config:
        from_attributes = True


# ============================================================
# DOCTOR MATCH RESULT
# ============================================================

class DoctorMatch(BaseModel):

    doctor_id: int

    name: str

    specialization: str

    qualification: str

    hospital: Optional[str] = None

    city: Optional[str] = None

    experience_years: int

    is_government_doctor: bool

    is_verified: bool

    consultation_type: str

    match_score: int

    available_slots: List[str]


# ============================================================
# DOCTOR MATCH RESPONSE
# ============================================================

class DoctorMatchResponse(BaseModel):

    date: str

    doctors: List[DoctorMatch]