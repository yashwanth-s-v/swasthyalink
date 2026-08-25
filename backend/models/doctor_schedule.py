from sqlalchemy import (
    Column,
    Integer,
    String,
    Time,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship

from database.database import Base


class DoctorSchedule(Base):

    __tablename__ = "doctor_schedules"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False
    )

    day_of_week = Column(
        String,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    slot_duration_minutes = Column(
        Integer,
        default=30
    )

    is_active = Column(
        Boolean,
        default=True
    )

    doctor = relationship(
        "Doctor",
        back_populates="schedules"
    )