import re


class SafetyService:

    """
    Conservative symptom safety screening.

    This service does not diagnose diseases.

    It only determines whether the user should:
    - continue with general information
    - speak with a qualified doctor
    - seek urgent medical attention

    AI responses must never override this result.
    """

    EMERGENCY_PATTERNS = [

        r"\bcan't breathe\b",
        r"\bcannot breathe\b",
        r"\bdifficulty breathing\b",
        r"\bsevere breathing\b",

        r"\bchest pain\b",

        r"\bunconscious\b",
        r"\bpassed out\b",
        r"\bfainted\b",

        r"\bseizure\b",
        r"\bconvulsion\b",

        r"\bsevere bleeding\b",
        r"\bbleeding heavily\b",

        r"\bvomiting blood\b",
        r"\bcoughing blood\b",

        r"\bsuicidal\b",
        r"\bsuicide\b",

        r"\bkill myself\b",

        r"\bblue lips\b",
        r"\bturning blue\b",

        r"\bnot responding\b",
    ]

    URGENT_PATTERNS = [

        r"\bhigh fever\b",
        r"\bvery high fever\b",
        r"\bsevere fever\b",

        r"\bfever\b.*\b5 days\b",
        r"\bfever\b.*\b6 days\b",
        r"\bfever\b.*\b7 days\b",
        r"\bfever\b.*\b8 days\b",
        r"\bfever\b.*\b9 days\b",
        r"\bfever\b.*\b10 days\b",
        r"\bfever\b.*\b11 days\b",
        r"\bfever\b.*\b12 days\b",
        r"\bfever\b.*\b13 days\b",
        r"\bfever\b.*\b14 days\b",

        r"\b5 days\b.*\bfever\b",
        r"\b6 days\b.*\bfever\b",
        r"\b7 days\b.*\bfever\b",
        r"\b8 days\b.*\bfever\b",
        r"\b9 days\b.*\bfever\b",
        r"\b10 days\b.*\bfever\b",
        r"\b11 days\b.*\bfever\b",
        r"\b12 days\b.*\bfever\b",
        r"\b13 days\b.*\bfever\b",
        r"\b14 days\b.*\bfever\b",

        r"\bsevere abdominal pain\b",
        r"\bsevere stomach pain\b",
        r"\bsevere headache\b",
        r"\bsevere pain\b",

        r"\bgetting worse\b",
        r"\bsymptoms getting worse\b",

        r"\bsevere dehydration\b",
        r"\bnot urinating\b",
        r"\bvery little urine\b",

        r"\bcontinuous vomiting\b",
        r"\bpersistent vomiting\b",

        r"\bconfusion\b",
        r"\bconfused\b",
        r"\bdisoriented\b",

        r"\bextreme weakness\b",
    ]

    DOCTOR_PATTERNS = [

        r"\bfever\b",
        r"\bcough\b",
        r"\bcold\b",

        r"\bstomach pain\b",
        r"\babdominal pain\b",

        r"\bdiarrhea\b",
        r"\bconstipation\b",

        r"\bvomiting\b",
        r"\bnausea\b",

        r"\brash\b",
        r"\bskin problem\b",

        r"\bjoint pain\b",
        r"\bback pain\b",

        r"\bdizziness\b",

        r"\bpalpitations\b",

        r"\bweight loss\b",

        r"\bsleep problem\b",
        r"\binsomnia\b",

        r"\banxiety\b",
        r"\bstress\b",
    ]

    def analyze(self, message: str) -> dict:

        if not message:

            return {
                "risk_level": "unknown",
                "requires_doctor": True,
                "emergency": False,
                "reason": "No symptom information was provided."
            }

        text = message.lower().strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        # ======================================================
        # EMERGENCY
        # ======================================================

        for pattern in self.EMERGENCY_PATTERNS:

            if re.search(
                pattern,
                text
            ):

                return {
                    "risk_level": "emergency",
                    "requires_doctor": True,
                    "emergency": True,
                    "reason": (
                        "The reported symptoms may require "
                        "urgent medical attention."
                    )
                }

        # ======================================================
        # URGENT
        # ======================================================

        for pattern in self.URGENT_PATTERNS:

            if re.search(
                pattern,
                text
            ):

                return {
                    "risk_level": "urgent",
                    "requires_doctor": True,
                    "emergency": False,
                    "reason": (
                        "The reported symptoms should be "
                        "evaluated promptly by a qualified "
                        "healthcare professional."
                    )
                }

        # ======================================================
        # DOCTOR REVIEW
        # ======================================================

        for pattern in self.DOCTOR_PATTERNS:

            if re.search(
                pattern,
                text
            ):

                return {
                    "risk_level": "doctor_review",
                    "requires_doctor": True,
                    "emergency": False,
                    "reason": (
                        "A qualified healthcare professional "
                        "should evaluate these symptoms."
                    )
                }

        # ======================================================
        # GENERAL
        # ======================================================

        return {
            "risk_level": "general",
            "requires_doctor": False,
            "emergency": False,
            "reason": (
                "No immediate warning pattern was detected."
            )
        }