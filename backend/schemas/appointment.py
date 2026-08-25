from datetime import date, time, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================
# CREATE APPOINTMENT
# ==========================================

class AppointmentCreate(BaseModel):

    patient_id: int

    doctor_id: int

    appointment_date: date

    appointment_time: time

    consultation_type: str = "chat"

    reason: Optional[str] = None


# ==========================================
# APPOINTMENT RESPONSE
# ==========================================

class AppointmentResponse(BaseModel):

    id: int

    patient_id: int

    doctor_id: int

    appointment_date: date

    appointment_time: time

    consultation_type: str

    status: str

    reason: Optional[str]

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )