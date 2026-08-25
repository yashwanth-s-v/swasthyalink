from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from database.database import Base


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False
    )

    appointment_date = Column(
        Date,
        nullable=False
    )

    appointment_time = Column(
        Time,
        nullable=False
    )

    consultation_type = Column(
        String,
        default="chat"
    )

    status = Column(
        String,
        default="booked"
    )

    reason = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False
    )

    patient = relationship(
        "Patient"
    )

    doctor = relationship(
        "Doctor"
    )