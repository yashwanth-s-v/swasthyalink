from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from database.database import get_db

from models.doctor import Doctor

from schemas.doctor import (
    DoctorCreate,
    DoctorResponse
)
from datetime import date

from fastapi import Query

from services.doctor_matching import (
    DoctorMatchingService
)

from schemas.doctor import (
    DoctorMatch,
    DoctorMatchResponse
)


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


# ==========================================
# CREATE DOCTOR
# ==========================================

@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_doctor(
    doctor_data: DoctorCreate,
    db: Session = Depends(get_db)
):

    # Check whether this user already has
    # a doctor profile.

    existing_doctor = (
        db.query(Doctor)
        .filter(
            Doctor.user_id
            == doctor_data.user_id
        )
        .first()
    )

    if existing_doctor:

        raise HTTPException(
            status_code=400,
            detail=(
                "Doctor profile already exists "
                "for this user."
            )
        )

    doctor = Doctor(
        user_id=doctor_data.user_id,
        qualification=doctor_data.qualification,
        specialization=doctor_data.specialization,
        registration_number=(
            doctor_data.registration_number
        ),
        hospital=doctor_data.hospital,
        city=doctor_data.city,
        experience_years=(
            doctor_data.experience_years
        ),
        is_government_doctor=(
            doctor_data.is_government_doctor
        ),
        is_verified=(
            doctor_data.is_verified
        ),
        consultation_type=(
            doctor_data.consultation_type
        ),
        is_available=(
            doctor_data.is_available
        )
    )

    db.add(doctor)

    db.commit()

    db.refresh(doctor)

    return doctor


# ==========================================
# GET ALL DOCTORS
# ==========================================

@router.get(
    "/",
    response_model=list[DoctorResponse]
)
def get_doctors(
    specialization: Optional[str] = None,
    city: Optional[str] = None,
    government_only: bool = False,
    verified_only: bool = False,
    db: Session = Depends(get_db)
):

    query = db.query(Doctor)

    # Filter by specialization

    if specialization:

        query = query.filter(
            Doctor.specialization
            .ilike(
                f"%{specialization}%"
            )
        )

    # Filter by city

    if city:

        query = query.filter(
            Doctor.city.ilike(
                f"%{city}%"
            )
        )

    # Government doctors only

    if government_only:

        query = query.filter(
            Doctor.is_government_doctor
            == True
        )

    # Verified doctors only

    if verified_only:

        query = query.filter(
            Doctor.is_verified
            == True
        )

    # Available doctors first

    query = query.order_by(
        Doctor.is_available.desc(),
        Doctor.is_verified.desc(),
        Doctor.is_government_doctor.desc()
    )

    return query.all()


# ==========================================
# GET SINGLE DOCTOR
# ==========================================

@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
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

    return doctor


# ==========================================
# UPDATE DOCTOR AVAILABILITY
# ==========================================

@router.patch(
    "/{doctor_id}/availability"
)
def update_doctor_availability(
    doctor_id: int,
    is_available: bool,
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

    doctor.is_available = is_available

    db.commit()

    db.refresh(doctor)
    # ==========================================
# AI DOCTOR MATCHING
# ==========================================

doctor_matching_service = (
    DoctorMatchingService()
)


@router.get(
    "/match",
    response_model=DoctorMatchResponse
)
def match_doctors(
    message: str = Query(
        ...,
        min_length=2,
        max_length=2000
    ),

    target_date: date = Query(
        ...
    ),

    consultation_type: str = Query(
        "any"
    ),

    db: Session = Depends(get_db)
):

    matched_doctors = (
        doctor_matching_service
        .get_fastest_available_doctors(
            db=db,
            message=message,
            target_date=target_date,
            consultation_type=consultation_type
        )
    )

    doctors = []

    for item in matched_doctors:

        doctor = item["doctor"]

        doctors.append(
            DoctorMatch(
                doctor_id=doctor.id,

                specialization=(
                    doctor.specialization
                ),

                qualification=(
                    doctor.qualification
                ),

                hospital=doctor.hospital,

                city=doctor.city,

                experience_years=(
                    doctor.experience_years
                    or 0
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

                available_slots=(
                    item["available_slots"]
                )
            )
        )

    return DoctorMatchResponse(
        date=target_date.isoformat(),
        doctors=doctors
    )