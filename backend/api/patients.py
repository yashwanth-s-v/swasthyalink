from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from models.patient import Patient


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.get("/")
def get_patients(
    db: Session = Depends(get_db)
):
    """
    Return all registered patients.
    """

    patients = db.query(Patient).all()

    return {
        "success": True,
        "count": len(patients),
        "patients": [
            {
                "id": patient.id,
                "user_id": patient.user_id,
                "age": patient.age,
                "gender": patient.gender,
                "location": patient.location
            }
            for patient in patients
        ]
    }


@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    """
    Return a single patient.
    """

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return {
        "success": True,
        "patient": {
            "id": patient.id,
            "user_id": patient.user_id,
            "age": patient.age,
            "gender": patient.gender,
            "location": patient.location
        }
    }


@router.post("/")
def create_patient(
    age: Optional[int] = None,
    gender: Optional[str] = None,
    location: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Create a basic patient profile.
    """

    patient = Patient(
        user_id=user_id,
        age=age,
        gender=gender,
        location=location
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return {
        "success": True,
        "message": "Patient profile created successfully",
        "patient": {
            "id": patient.id,
            "user_id": patient.user_id,
            "age": patient.age,
            "gender": patient.gender,
            "location": patient.location
        }
    }