async function loadDoctors() {

    const grid =
        document.getElementById("doctorGrid");

    grid.innerHTML =
        `<div class="loading">Finding doctors...</div>`;

    try {

        const specialization =
            document
                .getElementById("specialization")
                .value
                .trim();

        const city =
            document
                .getElementById("city")
                .value
                .trim();

        const doctors = await getDoctors({
            specialization,
            city
        });

        if (!doctors.length) {

            grid.innerHTML = `
                <div class="empty">
                    No doctors found.
                </div>
            `;

            return;
        }

        grid.innerHTML = doctors.map(doctor => `

            <div class="doctor-card">

                <div class="doctor-avatar">
                    ${(
                        doctor.specialization || "D"
                    ).charAt(0).toUpperCase()}
                </div>

                <h3>
                    Doctor #${doctor.id}
                </h3>

                <div class="specialization">
                    ${doctor.specialization || "General Doctor"}
                </div>

                <div class="doctor-info">

                    <p>
                        🎓 ${doctor.qualification || "Qualified Doctor"}
                    </p>

                    <p>
                        🏥 ${doctor.hospital || "Clinic"}
                    </p>

                    <p>
                        📍 ${doctor.city || "Location not provided"}
                    </p>

                    <p>
                        💼 ${doctor.experience_years || 0}
                        years experience
                    </p>

                    <br>

                    <span class="status ${
                        doctor.is_available
                            ? "available"
                            : "unavailable"
                    }">

                        ${
                            doctor.is_available
                                ? "Available"
                                : "Currently unavailable"
                        }

                    </span>

                    ${
                        doctor.is_verified
                            ? `<span class="status available">
                                ✓ Verified
                               </span>`
                            : ""
                    }

                </div>

                <a
                    href="appointment.html?doctor_id=${doctor.id}"
                    class="btn btn-primary full-btn">

                    View Availability

                </a>

            </div>

        `).join("");

    } catch (error) {

        grid.innerHTML = `
            <div class="empty">
                ${error.message}
            </div>
        `;
    }
}

document.addEventListener("DOMContentLoaded", async () => {

    const token =
        localStorage.getItem("ayurconnect_token");

    if (!token) {

        window.location.href = "login.html";
        return;
    }

    await loadDoctors();

    document
        .getElementById("searchDoctors")
        .addEventListener(
            "click",
            loadDoctors
        );

});