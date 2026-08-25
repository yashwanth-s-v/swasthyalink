from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.database import Base


class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    qualification = Column(
        String,
        nullable=False
    )

    specialization = Column(
        String,
        nullable=False
    )

    registration_number = Column(
        String,
        unique=True,
        nullable=True
    )

    hospital = Column(
        String,
        nullable=True
    )

    city = Column(
        String,
        nullable=True
    )

    experience_years = Column(
        Integer,
        default=0
    )

    is_government_doctor = Column(
        Boolean,
        default=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    consultation_type = Column(
        String,
        default="appointment"
    )

    is_available = Column(
        Boolean,
        default=True
    )

    user = relationship(
        "User"
    )

    schedules = relationship(
        "DoctorSchedule",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )