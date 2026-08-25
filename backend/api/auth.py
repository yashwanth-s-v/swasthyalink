from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.database import get_db

from models.user import User
from models.patient import Patient

from schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    PatientProfileCreate,
    PatientProfileResponse
)

from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


security = HTTPBearer()


# ==========================================
# REGISTER
# ==========================================

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == user_data.email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    if user_data.role not in [
        "patient",
        "doctor"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(
            user_data.password
        ),
        full_name=user_data.full_name,
        role=user_data.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    # Automatically create a patient profile
    # when the registered user is a patient.

    if new_user.role == "patient":

        patient = Patient(
            user_id=new_user.id
        )

        db.add(patient)

        db.commit()

    return new_user


# ==========================================
# LOGIN
# ==========================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == login_data.email
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        login_data.password,
        user.hashed_password
    )

    if not password_valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    token = create_access_token(
        user_id=user.id,
        role=user.role
    )

    return TokenResponse(
        access_token=token
    )


# ==========================================
# CURRENT USER
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_access_token(
        token
    )

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================================
# PATIENT PROFILE
# ==========================================

@router.post(
    "/patient/profile",
    response_model=PatientProfileResponse
)
def create_or_update_patient_profile(
    profile_data: PatientProfileCreate,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_access_token(
        token
    )

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "patient":

        raise HTTPException(
            status_code=403,
            detail="Only patients can access this endpoint"
        )

    patient = (
        db.query(Patient)
        .filter(
            Patient.user_id == user.id
        )
        .first()
    )

    if not patient:

        patient = Patient(
            user_id=user.id
        )

        db.add(patient)

    patient.age = profile_data.age
    patient.gender = profile_data.gender
    patient.phone = profile_data.phone
    patient.city = profile_data.city

    db.commit()

    db.refresh(patient)

    return patient