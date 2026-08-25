function assessSymptoms(symptoms, duration, age) {

    const text =
        symptoms.toLowerCase();

    const highRiskTerms = [
        "difficulty breathing",
        "can't breathe",
        "cannot breathe",
        "severe chest pain",
        "chest pain",
        "unconscious",
        "fainted",
        "seizure",
        "convulsion",
        "severe bleeding",
        "vomiting blood",
        "blood in vomit",
        "black stool",
        "blue lips",
        "severe confusion",
        "not responding",
        "stroke",
        "paralysis"
    ];

    const mediumRiskTerms = [
        "high fever",
        "fever",
        "persistent fever",
        "severe headache",
        "severe pain",
        "persistent vomiting",
        "dehydration",
        "dizzy",
        "weakness",
        "worsening",
        "infection"
    ];

    const highRisk =
        highRiskTerms.some(
            term => text.includes(term)
        );

    const prolonged =
        duration === "7_plus_days";

    const feverConcern =
        text.includes("fever") &&
        (
            duration === "3_6_days" ||
            duration === "7_plus_days"
        );

    const mediumRisk =
        !highRisk &&
        (
            mediumRiskTerms.some(
                term => text.includes(term)
            ) ||
            prolonged ||
            feverConcern
        );

    if (highRisk) {

        return {
            level: "high",
            title: "Professional medical attention is important",
            message:
                "Some symptoms you entered may require prompt professional assessment. Do not rely on this screening result alone.",
            action:
                "Please seek appropriate medical care promptly. If symptoms are severe or rapidly worsening, seek emergency medical help."
        };
    }

    if (mediumRisk) {

        return {
            level: "medium",
            title: "A doctor consultation is recommended",
            message:
                "Your symptoms or their duration suggest that speaking with a healthcare professional would be appropriate.",
            action:
                "You can use AyurConnect to find an available doctor and request a consultation."
        };
    }

    return {
        level: "low",
        title: "No immediate warning signs detected by this screening",
        message:
            "This screening did not identify the warning signs included in our safety checks.",
        action:
            "This is not a diagnosis and does not rule out illness. Monitor your symptoms and consult a doctor if they persist, worsen, or concern you."
    };
}

function showAssessmentResult(result) {

    const container =
        document.getElementById(
            "assessmentResult"
        );

    container.innerHTML = `

        <div class="risk-box risk-${result.level}">

            <div class="risk-label">
                ${result.level} screening
            </div>

            <h2>
                ${result.title}
            </h2>

            <p>
                ${result.message}
            </p>

            <br>

            <strong>
                ${result.action}
            </strong>

            <br><br>

            ${
                result.level === "high"
                    ? `
                        <a
                            href="doctors.html"
                            class="btn btn-danger">

                            Find a Doctor Now

                        </a>
                      `
                    : result.level === "medium"
                        ? `
                            <a
                                href="doctors.html"
                                class="btn btn-primary">

                                View Available Doctors

                            </a>
                          `
                        : `
                            <a
                                href="doctors.html"
                                class="btn btn-outline">

                                Talk to a Doctor

                            </a>
                          `
            }

        </div>

        <div class="action-card">

            <h3>
                Important
            </h3>

            <p style="margin-top:10px;color:var(--muted);">

                AyurConnect's screening is intended to help
                users decide when professional attention may
                be appropriate. It does not diagnose diseases,
                prescribe medicines, or replace a qualified
                healthcare professional.

            </p>

        </div>
    `;
}

document.addEventListener("DOMContentLoaded", async () => {

    const user = await requireAuth();

    if (!user) return;

    const button =
        document.getElementById(
            "assessButton"
        );

    button.addEventListener(
        "click",
        () => {

            const symptoms =
                document
                    .getElementById("symptoms")
                    .value
                    .trim();

            const duration =
                document
                    .getElementById("duration")
                    .value;

            const age =
                document
                    .getElementById("age")
                    .value;

            if (!symptoms) {

                document.getElementById(
                    "assessmentResult"
                ).innerHTML = `

                    <div class="message error">

                        Please describe your symptoms first.

                    </div>

                `;

                return;
            }

            const result =
                assessSymptoms(
                    symptoms,
                    duration,
                    age
                );

            showAssessmentResult(result);
        }
    );
});