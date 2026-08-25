from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=72
    )

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    role: str = "patient"


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: int

    email: EmailStr

    full_name: str

    role: str

    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class PatientProfileCreate(BaseModel):

    age: int | None = None

    gender: str | None = None

    phone: str | None = None

    city: str | None = None


class PatientProfileResponse(BaseModel):

    id: int

    user_id: int

    age: int | None

    gender: str | None

    phone: str | None

    city: str | None

    class Config:
        from_attributes = True