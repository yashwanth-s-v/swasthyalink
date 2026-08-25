from datetime import time

from pydantic import BaseModel, ConfigDict


class DoctorScheduleCreate(BaseModel):

    doctor_id: int

    day_of_week: str

    start_time: time

    end_time: time

    slot_duration_minutes: int = 30

    is_active: bool = True


class DoctorScheduleResponse(BaseModel):

    id: int

    doctor_id: int

    day_of_week: str

    start_time: time

    end_time: time

    slot_duration_minutes: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )