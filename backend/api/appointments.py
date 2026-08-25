from datetime import (
    datetime,
    timedelta
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database.database import get_db

from models.appointment import Appointment
from models.doctor import Doctor
from models.patient import Patient
from models.doctor_schedule import DoctorSchedule

from schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse
)

from schemas.doctor_schedule import (
    DoctorScheduleCreate,
    DoctorScheduleResponse
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# ==========================================
# CREATE DOCTOR SCHEDULE
# ==========================================

@router.post(
    "/schedule",
    response_model=DoctorScheduleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_schedule(
    schedule_data: DoctorScheduleCreate,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(Doctor)
        .filter(
            Doctor.id
            == schedule_data.doctor_id
        )
        .first()
    )

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )

    if schedule_data.start_time >= schedule_data.end_time:

        raise HTTPException(
            status_code=400,
            detail=(
                "Start time must be before "
                "end time."
            )
        )

    if schedule_data.slot_duration_minutes <= 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "Slot duration must be greater "
                "than zero."
            )
        )

    schedule = DoctorSchedule(
        doctor_id=schedule_data.doctor_id,
        day_of_week=schedule_data.day_of_week.lower(),
        start_time=schedule_data.start_time,
        end_time=schedule_data.end_time,
        slot_duration_minutes=(
            schedule_data.slot_duration_minutes
        ),
        is_active=schedule_data.is_active
    )

    db.add(schedule)

    db.commit()

    db.refresh(schedule)

    return schedule


# ==========================================
# GET DOCTOR SCHEDULES
# ==========================================

@router.get(
    "/schedule/doctor/{doctor_id}",
    response_model=list[DoctorScheduleResponse]
)
def get_doctor_schedules(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(DoctorSchedule)
        .filter(
            DoctorSchedule.doctor_id
            == doctor_id,
            DoctorSchedule.is_active
            == True
        )
        .all()
    )


# ==========================================
# GET AVAILABLE SLOTS
# ==========================================

@router.get(
    "/available/{doctor_id}/{date}"
)
def get_available_slots(
    doctor_id: int,
    date: str,
    db: Session = Depends(get_db)
):

    doctor = (
        db.query(Doctor)
        .filter(
            Doctor.id == doctor_id
        )
        .first()
    )

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )

    try:

        requested_date = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid date format. "
                "Use YYYY-MM-DD."
            )
        )

    day_name = (
        requested_date
        .strftime("%A")
        .lower()
    )

    schedule = (
        db.query(DoctorSchedule)
        .filter(
            DoctorSchedule.doctor_id
            == doctor_id,
            DoctorSchedule.day_of_week
            == day_name,
            DoctorSchedule.is_active
            == True
        )
        .first()
    )

    if not schedule:

        return {
            "doctor_id": doctor_id,
            "date": date,
            "day": day_name,
            "available_slots": []
        }

    # --------------------------------------
    # Generate slots
    # --------------------------------------

    current_time = datetime.combine(
        requested_date,
        schedule.start_time
    )

    end_time = datetime.combine(
        requested_date,
        schedule.end_time
    )

    slots = []

    while current_time < end_time:

        slot_time = current_time.time()

        existing = (
            db.query(Appointment)
            .filter(
                Appointment.doctor_id
                == doctor_id,

                Appointment.appointment_date
                == requested_date,

                Appointment.appointment_time
                == slot_time,

                Appointment.status
                == "booked"
            )
            .first()
        )

        if not existing:

            slots.append(
                slot_time.strftime("%H:%M")
            )

        current_time += timedelta(
            minutes=schedule.slot_duration_minutes
        )

    return {
        "doctor_id": doctor_id,
        "date": date,
        "day": day_name,
        "available_slots": slots
    }


# ==========================================
# BOOK APPOINTMENT
# ==========================================

@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED
)
def book_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(
            Patient.id
            == appointment_data.patient_id
        )
        .first()
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    doctor = (
        db.query(Doctor)
        .filter(
            Doctor.id
            == appointment_data.doctor_id
        )
        .first()
    )

    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )

    if not doctor.is_available:

        raise HTTPException(
            status_code=400,
            detail=(
                "Doctor is currently unavailable."
            )
        )

    # --------------------------------------
    # Verify doctor's schedule
    # --------------------------------------

    day_name = (
        appointment_data.appointment_date
        .strftime("%A")
        .lower()
    )

    schedule = (
        db.query(DoctorSchedule)
        .filter(
            DoctorSchedule.doctor_id
            == doctor.id,

            DoctorSchedule.day_of_week
            == day_name,

            DoctorSchedule.is_active
            == True
        )
        .first()
    )

    if not schedule:

        raise HTTPException(
            status_code=400,
            detail=(
                "Doctor is not available "
                "on this day."
            )
        )

    # --------------------------------------
    # Check time is inside working hours
    # --------------------------------------

    if not (
        schedule.start_time
        <= appointment_data.appointment_time
        < schedule.end_time
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Selected time is outside "
                "doctor's working hours."
            )
        )

    # --------------------------------------
    # Check slot alignment
    # --------------------------------------

    start_datetime = datetime.combine(
        appointment_data.appointment_date,
        schedule.start_time
    )

    requested_datetime = datetime.combine(
        appointment_data.appointment_date,
        appointment_data.appointment_time
    )

    elapsed_minutes = int(
        (
            requested_datetime
            - start_datetime
        ).total_seconds() / 60
    )

    if (
        elapsed_minutes
        % schedule.slot_duration_minutes
        != 0
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Selected time is not a valid "
                "appointment slot."
            )
        )

    # --------------------------------------
    # Duplicate booking protection
    # --------------------------------------

    existing = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id
            == doctor.id,

            Appointment.appointment_date
            == appointment_data.appointment_date,

            Appointment.appointment_time
            == appointment_data.appointment_time,

            Appointment.status
            == "booked"
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=409,
            detail=(
                "This appointment slot is "
                "already booked."
            )
        )

    # --------------------------------------
    # Create appointment
    # --------------------------------------

    appointment = Appointment(

        patient_id=(
            appointment_data.patient_id
        ),

        doctor_id=(
            appointment_data.doctor_id
        ),

        appointment_date=(
            appointment_data.appointment_date
        ),

        appointment_time=(
            appointment_data.appointment_time
        ),

        consultation_type=(
            appointment_data.consultation_type
        ),

        reason=(
            appointment_data.reason
        ),

        status="booked",

        created_at=datetime.utcnow()
    )

    db.add(appointment)

    db.commit()

    db.refresh(appointment)

    return appointment


# ==========================================
# PATIENT APPOINTMENTS
# ==========================================

@router.get(
    "/patient/{patient_id}",
    response_model=list[AppointmentResponse]
)
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(Appointment)
        .filter(
            Appointment.patient_id
            == patient_id
        )
        .order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        )
        .all()
    )


# ==========================================
# DOCTOR APPOINTMENTS
# ==========================================

@router.get(
    "/doctor/{doctor_id}",
    response_model=list[AppointmentResponse]
)
def get_doctor_appointments(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    return (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id
            == doctor_id
        )
        .order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        )
        .all()
    )


# ==========================================
# CANCEL APPOINTMENT
# ==========================================

@router.patch(
    "/{appointment_id}/cancel"
)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id
            == appointment_id
        )
        .first()
    )

    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found."
        )

    if appointment.status == "cancelled":

        raise HTTPException(
            status_code=400,
            detail=(
                "Appointment is already cancelled."
            )
        )

    appointment.status = "cancelled"

    db.commit()

    return {
        "message": (
            "Appointment cancelled successfully."
        ),
        "appointment_id": appointment.id
    }