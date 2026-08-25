let selectedDoctor = null;
let selectedSlot = null;

function getDoctorId() {

    const params =
        new URLSearchParams(window.location.search);

    return params.get("doctor_id");
}

async function loadDoctor() {

    const doctorId = getDoctorId();

    if (!doctorId) {

        document.getElementById("doctorDetails").innerHTML = `
            <div class="empty">
                No doctor selected.
                <br><br>
                <a href="doctors.html"
                   class="btn btn-primary">
                    Find a Doctor
                </a>
            </div>
        `;

        return;
    }

    try {

        selectedDoctor =
            await getDoctor(doctorId);

        document.getElementById("doctorDetails").innerHTML = `

            <div class="doctor-card">

                <div class="doctor-avatar">
                    ${(selectedDoctor.specialization || "D")
                        .charAt(0)
                        .toUpperCase()}
                </div>

                <h3>
                    Doctor #${selectedDoctor.id}
                </h3>

                <p class="specialization">
                    ${selectedDoctor.specialization || "General Doctor"}
                </p>

                <div class="doctor-info">

                    <p>
                        ${selectedDoctor.qualification || ""}
                    </p>

                    <p>
                        ${selectedDoctor.hospital || ""}
                    </p>

                    <p>
                        ${selectedDoctor.city || ""}
                    </p>

                </div>

            </div>

        `;

    } catch (error) {

        document.getElementById("doctorDetails").innerHTML =
            `<p>${error.message}</p>`;
    }
}

async function loadSlots() {

    selectedSlot = null;

    const date =
        document.getElementById("appointmentDate").value;

    const slotGrid =
        document.getElementById("slotGrid");

    if (!date || !selectedDoctor) {

        slotGrid.innerHTML =
            "Select a date.";

        return;
    }

    slotGrid.innerHTML =
        "Loading available slots...";

    try {

        const result =
            await getAvailableSlots(
                selectedDoctor.id,
                date
            );

        if (!result.available_slots.length) {

            slotGrid.innerHTML = `
                <div class="empty">
                    No available slots for this date.
                </div>
            `;

            return;
        }

        slotGrid.innerHTML =
            result.available_slots.map(slot => `

                <button
                    class="slot"
                    data-time="${slot}">

                    ${slot}

                </button>

            `).join("");

        document
            .querySelectorAll(".slot")
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        document
                            .querySelectorAll(".slot")
                            .forEach(item =>
                                item.classList.remove("selected")
                            );

                        button.classList.add("selected");

                        selectedSlot =
                            button.dataset.time;
                    }
                );

            });

    } catch (error) {

        slotGrid.innerHTML =
            `<div class="empty">${error.message}</div>`;
    }
}

document.addEventListener("DOMContentLoaded", async () => {

    const user = await requireAuth();

    if (!user) return;

    if (user.role !== "patient") {

        window.location.href =
            "doctor-dashboard.html";

        return;
    }

    const dateInput =
        document.getElementById("appointmentDate");

    const today =
        new Date().toISOString().split("T")[0];

    dateInput.min = today;
    dateInput.value = today;

    await loadDoctor();

    await loadSlots();

    dateInput.addEventListener(
        "change",
        loadSlots
    );

    document
        .getElementById("bookButton")
        .addEventListener(
            "click",
            async () => {

                const message =
                    document.getElementById(
                        "appointmentMessage"
                    );

                if (!selectedDoctor) {

                    showMessage(
                        message,
                        "Please select a doctor."
                    );

                    return;
                }

                if (!selectedSlot) {

                    showMessage(
                        message,
                        "Please select an available time slot."
                    );

                    return;
                }

                const patient =
                    JSON.parse(
                        localStorage.getItem(
                            "ayurconnect_patient"
                        )
                    );

                if (!patient) {

                    showMessage(
                        message,
                        "Patient profile could not be found. Please return to the dashboard."
                    );

                    return;
                }

                const reason =
                    document
                        .getElementById("reason")
                        .value
                        .trim();

                const consultationType =
                    document
                        .getElementById("consultationType")
                        .value;

                const button =
                    document.getElementById(
                        "bookButton"
                    );

                button.disabled = true;
                button.textContent =
                    "Booking...";

                try {

                    const result =
                        await bookAppointment({

                            patient_id:
                                patient.id,

                            doctor_id:
                                selectedDoctor.id,

                            appointment_date:
                                dateInput.value,

                            appointment_time:
                                selectedSlot + ":00",

                            consultation_type:
                                consultationType,

                            reason:
                                reason

                        });

                    showMessage(
                        message,
                        "Appointment booked successfully!",
                        "success"
                    );

                    setTimeout(() => {

                        window.location.href =
                            "dashboard.html";

                    }, 1200);

                } catch (error) {

                    showMessage(
                        message,
                        error.message
                    );

                } finally {

                    button.disabled = false;
                    button.textContent =
                        "Book Consultation";
                }
            }
        );
});