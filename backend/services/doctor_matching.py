from datetime import date

from sqlalchemy.orm import Session

from models.doctor import Doctor
from models.doctor_schedule import DoctorSchedule
from models.appointment import Appointment


class DoctorMatchingService:

    """
    Matches patients with suitable Ayurvedic doctors.

    Matching currently considers:

    1. Doctor availability
    2. Doctor verification
    3. Government doctor status
    4. Specialization
    5. Consultation type
    6. Existing booked appointments

    This service does NOT diagnose patients.
    """

    def _calculate_score(
        self,
        doctor: Doctor,
        message: str
    ) -> int:

        score = 0

        text = message.lower()

        # --------------------------------------
        # Verified doctor
        # --------------------------------------

        if doctor.is_verified:
            score += 30

        # --------------------------------------
        # Government doctor
        # --------------------------------------

        if doctor.is_government_doctor:
            score += 20

        # --------------------------------------
        # Available doctor
        # --------------------------------------

        if doctor.is_available:
            score += 30

        # --------------------------------------
        # Experience
        # --------------------------------------

        if doctor.experience_years:

            score += min(
                doctor.experience_years,
                20
            )

        # --------------------------------------
        # Basic specialization matching
        # --------------------------------------

        specialization = (
            doctor.specialization or ""
        ).lower()

        keywords = {
            "digest": [
                "stomach",
                "digestion",
                "gas",
                "bloating",
                "constipation",
                "acidity"
            ],

            "skin": [
                "skin",
                "rash",
                "itching",
                "acne"
            ],

            "respiratory": [
                "cough",
                "cold",
                "breathing",
                "throat"
            ],

            "pain": [
                "pain",
                "joint",
                "back",
                "muscle"
            ],

            "stress": [
                "stress",
                "anxiety",
                "sleep",
                "insomnia"
            ]
        }

        for category, category_words in keywords.items():

            if any(
                word in text
                for word in category_words
            ):

                if category in specialization:

                    score += 25

        return score

    def find_doctors(
        self,
        db: Session,
        message: str,
        consultation_type: str = "chat"
    ):

        doctors = (
            db.query(Doctor)
            .filter(
                Doctor.is_available == True
            )
            .all()
        )

        results = []

        for doctor in doctors:

            # ----------------------------------
            # Consultation type
            # ----------------------------------

            doctor_type = (
                doctor.consultation_type
                or "appointment"
            ).lower()

            requested_type = (
                consultation_type.lower()
            )

            if (
                requested_type != "any"
                and requested_type not in doctor_type
                and doctor_type != "both"
            ):
                continue

            score = self._calculate_score(
                doctor,
                message
            )

            results.append(
                {
                    "doctor": doctor,
                    "score": score
                }
            )

        # --------------------------------------
        # Highest score first
        # --------------------------------------

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results

    def get_fastest_available_doctors(
        self,
        db: Session,
        message: str,
        target_date: date,
        consultation_type: str = "chat"
    ):

        matched_doctors = self.find_doctors(
            db=db,
            message=message,
            consultation_type=consultation_type
        )

        results = []

        day_name = (
            target_date
            .strftime("%A")
            .lower()
        )

        for item in matched_doctors:

            doctor = item["doctor"]

            schedules = (
                db.query(DoctorSchedule)
                .filter(
                    DoctorSchedule.doctor_id
                    == doctor.id,

                    DoctorSchedule.day_of_week
                    == day_name,

                    DoctorSchedule.is_active
                    == True
                )
                .all()
            )

            if not schedules:
                continue

            booked_times = {
                appointment.appointment_time

                for appointment in (
                    db.query(Appointment)
                    .filter(
                        Appointment.doctor_id
                        == doctor.id,

                        Appointment.appointment_date
                        == target_date,

                        Appointment.status
                        == "booked"
                    )
                    .all()
                )
            }

            available_slots = []

            for schedule in schedules:

                from datetime import datetime, timedelta

                current = datetime.combine(
                    target_date,
                    schedule.start_time
                )

                end = datetime.combine(
                    target_date,
                    schedule.end_time
                )

                while current < end:

                    slot = current.time()

                    if slot not in booked_times:

                        available_slots.append(
                            slot.strftime("%H:%M")
                        )

                    current += timedelta(
                        minutes=(
                            schedule.slot_duration_minutes
                        )
                    )

            if available_slots:

                results.append(
                    {
                        "doctor": doctor,
                        "score": item["score"],
                        "date": target_date,
                        "available_slots": available_slots
                    }
                )

        # --------------------------------------
        # Sort by earliest slot
        # --------------------------------------

        def first_slot(item):

            return item["available_slots"][0]

        results.sort(
            key=lambda item: (
                first_slot(item),
                -item["score"]
            )
        )

        return results