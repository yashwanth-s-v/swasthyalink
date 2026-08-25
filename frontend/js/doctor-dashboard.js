let currentDoctor = null;

document.addEventListener("DOMContentLoaded", async () => {

    const user = await requireAuth();

    if (!user) return;

    if (user.role !== "doctor") {

        window.location.href =
            "dashboard.html";

        return;
    }

    document.getElementById(
        "doctorWelcome"
    ).textContent =
        `Welcome, ${user.full_name}. Manage your availability and consultations.`;

    try {

        const doctors =
            await getDoctors();

        currentDoctor =
            doctors.find(
                doctor =>
                    doctor.user_id === user.id
            );

        if (!currentDoctor) {

            document.getElementById(
                "doctorProfile"
            ).innerHTML = `

                <p>
                    Your doctor profile has not been created yet.
                </p>

                <br>

                <p style="color:var(--muted);">
                    Your account exists, but a doctor profile
                    must be created before you can receive
                    appointments.
                </p>

            `;

            document.getElementById(
                "availabilityButton"
            ).textContent =
                "Profile incomplete";

            document.getElementById(
                "availabilityButton"
            ).disabled = true;

            return;
        }

        document.getElementById(
            "doctorProfile"
        ).innerHTML = `

            <p>
                <strong>
                    Specialization:
                </strong>

                ${currentDoctor.specialization || "Not provided"}
            </p>

            <p>
                <strong>
                    Qualification:
                </strong>

                ${currentDoctor.qualification || "Not provided"}
            </p>

            <p>
                <strong>
                    Hospital:
                </strong>

                ${currentDoctor.hospital || "Not provided"}
            </p>

            <p>
                <strong>
                    City:
                </strong>

                ${currentDoctor.city || "Not provided"}
            </p>

            <p>
                <strong>
                    Experience:
                </strong>

                ${currentDoctor.experience_years || 0} years
            </p>

            <br>

            <span class="status ${
                currentDoctor.is_available
                    ? "available"
                    : "unavailable"
            }">

                ${
                    currentDoctor.is_available
                        ? "Currently Available"
                        : "Currently Unavailable"
                }

            </span>
        `;

        const availabilityButton =
            document.getElementById(
                "availabilityButton"
            );

        availabilityButton.textContent =
            currentDoctor.is_available
                ? "Set as Unavailable"
                : "Set as Available";

        availabilityButton.className =
            currentDoctor.is_available
                ? "btn btn-danger"
                : "btn btn-primary";

        availabilityButton.addEventListener(
            "click",
            async () => {

                try {

                    const newStatus =
                        !currentDoctor.is_available;

                    await updateDoctorAvailability(
                        currentDoctor.id,
                        newStatus
                    );

                    currentDoctor.is_available =
                        newStatus;

                    availabilityButton.textContent =
                        newStatus
                            ? "Set as Unavailable"
                            : "Set as Available";

                    availabilityButton.className =
                        newStatus
                            ? "btn btn-danger"
                            : "btn btn-primary";

                    showMessage(
                        document.getElementById(
                            "doctorMessage"
                        ),
                        newStatus
                            ? "You are now available for consultations."
                            : "You are now marked as unavailable.",
                        "success"
                    );

                } catch (error) {

                    showMessage(
                        document.getElementById(
                            "doctorMessage"
                        ),
                        error.message
                    );
                }
            }
        );

        const appointments =
            await getDoctorAppointments(
                currentDoctor.id
            );

        const container =
            document.getElementById(
                "doctorAppointments"
            );

        if (!appointments.length) {

            container.innerHTML = `
                <div class="empty">
                    No appointments yet.
                </div>
            `;

            return;
        }

        container.className =
            "table-wrapper";

        container.innerHTML = `

            <table>

                <thead>

                    <tr>

                        <th>Date</th>
                        <th>Time</th>
                        <th>Patient</th>
                        <th>Type</th>
                        <th>Reason</th>
                        <th>Status</th>

                    </tr>

                </thead>

                <tbody>

                    ${appointments.map(a => `

                        <tr>

                            <td>
                                ${a.appointment_date}
                            </td>

                            <td>
                                ${a.appointment_time}
                            </td>

                            <td>
                                Patient #${a.patient_id}
                            </td>

                            <td>
                                ${a.consultation_type || "-"}
                            </td>

                            <td>
                                ${a.reason || "-"}
                            </td>

                            <td>
                                ${a.status}
                            </td>

                        </tr>

                    `).join("")}

                </tbody>

            </table>
        `;

    } catch (error) {

        showMessage(
            document.getElementById(
                "doctorMessage"
            ),
            error.message
        );
    }
});