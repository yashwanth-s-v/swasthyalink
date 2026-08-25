class AyurvedaService:

    """
    Provides conservative, general wellness guidance.

    This service does not diagnose conditions and
    does not prescribe Ayurvedic medicines.
    """

    FOOD_GUIDANCE = {

        "digestion": {
            "foods": [
                (
                    "Warm, lightly cooked meals",
                    "May be easier to digest than very heavy meals."
                ),
                (
                    "Rice or soft grains",
                    "Can be a simple option when appetite is low."
                ),
                (
                    "Cooked vegetables",
                    "Provides nutrients without relying on very heavy foods."
                )
            ],
            "avoid": [
                "Very heavy meals",
                "Excessively oily foods",
                "Very large portions"
            ]
        },

        "cold": {
            "foods": [
                (
                    "Warm soups",
                    "A warm meal can be comfortable when experiencing cold-like symptoms."
                ),
                (
                    "Warm fluids",
                    "Can help maintain hydration."
                )
            ],
            "avoid": [
                "Very cold drinks if they worsen your symptoms",
                "Skipping fluids"
            ]
        },

        "headache": {
            "foods": [
                (
                    "Water",
                    "Dehydration can contribute to headaches."
                ),
                (
                    "Regular balanced meals",
                    "Skipping meals may contribute to some headaches."
                )
            ],
            "avoid": [
                "Skipping meals",
                "Excessive caffeine",
                "Dehydration"
            ]
        }
    }

    def get_guidance(self, message: str):

        text = message.lower()

        if any(
            word in text
            for word in [
                "stomach",
                "digestion",
                "indigestion",
                "bloating",
                "gas",
                "constipation"
            ]
        ):

            category = "digestion"

        elif any(
            word in text
            for word in [
                "cold",
                "cough",
                "sore throat"
            ]
        ):

            category = "cold"

        elif any(
            word in text
            for word in [
                "headache",
                "head pain"
            ]
        ):

            category = "headache"

        else:

            return {
                "foods": [],
                "avoid": []
            }

        guidance = self.FOOD_GUIDANCE[category]

        return {
            "foods": guidance["foods"],
            "avoid": guidance["avoid"]
        }