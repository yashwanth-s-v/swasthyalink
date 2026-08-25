document.addEventListener("DOMContentLoaded", async () => {

    const user = await requireAuth();

    if (!user) return;

    if (user.role !== "patient") {
        window.location.href = "doctor-dashboard.html";
        return;
    }

    const nameElement =
        document.getElementById("userName");

    nameElement.textContent =
        user.full_name || "Patient";

    try {

        const result = await getPatients();

        const patient = result.patients.find(
            item => item.user_id === user.id
        );

        if (!patient) {

            document.getElementById("profileInfo").innerHTML = `
                <p>Your patient profile is not complete.</p>
                <br>
                <a href="assessment.html"
                   class="btn btn-primary">
                    Complete health information
                </a>
            `;

            return;
        }

        localStorage.setItem(
            "ayurconnect_patient",
            JSON.stringify(patient)
        );

        document.getElementById("profileInfo").innerHTML = `
            <p><strong>Name:</strong> ${user.full_name}</p>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Age:</strong> ${patient.age ?? "Not provided"}</p>
            <p><strong>Gender:</strong> ${patient.gender ?? "Not provided"}</p>
            <p><strong>Location:</strong> ${patient.location ?? "Not provided"}</p>
        `;

        const appointments =
            await getPatientAppointments(patient.id);

        document.getElementById("appointmentCount")
            .textContent = appointments.length;

        const container =
            document.getElementById("appointments");

        if (!appointments.length) {

            container.innerHTML = `
                <div class="empty">
                    You don't have any appointments yet.
                    <br><br>
                    <a href="doctors.html"
                       class="btn btn-primary">
                        Find a Doctor
                    </a>
                </div>
            `;

            return;
        }

        container.className = "table-wrapper";

        container.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Doctor</th>
                        <th>Type</th>
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
                                Doctor #${a.doctor_id}
                            </td>

                            <td>
                                ${a.consultation_type || "Consultation"}
                            </td>

                            <td>
                                <span class="status ${
                                    a.status === "booked"
                                        ? "available"
                                        : "unavailable"
                                }">
                                    ${a.status}
                                </span>
                            </td>

                        </tr>
                    `).join("")}

                </tbody>
            </table>
        `;

    } catch (error) {

        document.getElementById("profileInfo").innerHTML =
            `<p>${error.message}</p>`;

    }
});