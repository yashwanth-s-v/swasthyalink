const API_BASE = "http://127.0.0.1:8000/api";

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("ayurconnect_token");

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });

    let data;

    try {
        data = await response.json();
    } catch {
        data = null;
    }

    if (!response.ok) {
        let message = "Something went wrong.";

        if (data) {
            if (typeof data.detail === "string") {
                message = data.detail;
            } else if (Array.isArray(data.detail)) {
                message = data.detail
                    .map(error => {
                        if (typeof error === "string") return error;

                        const field = error.loc
                            ? error.loc.join(".")
                            : "field";

                        return `${field}: ${error.msg || "Invalid value"}`;
                    })
                    .join(" | ");
            } else if (typeof data.message === "string") {
                message = data.message;
            } else {
                message = JSON.stringify(data);
            }
        }

        throw new Error(message);
    }

    return data;
}

async function registerUser(payload) {
    return apiRequest("/auth/register", {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

async function loginUser(payload) {
    return apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

async function getCurrentUser() {
    return apiRequest("/auth/me");
}

async function updatePatientProfile(payload) {
    return apiRequest("/auth/patient/profile", {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

async function getDoctors(params = {}) {
    const query = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
            query.append(key, value);
        }
    });

    const url = query.toString()
        ? `/doctors/?${query.toString()}`
        : "/doctors/";

    return apiRequest(url);
}

async function getDoctor(doctorId) {
    return apiRequest(`/doctors/${doctorId}`);
}

async function createDoctor(payload) {
    return apiRequest("/doctors/", {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

async function updateDoctorAvailability(doctorId, isAvailable) {
    return apiRequest(
        `/doctors/${doctorId}/availability?is_available=${isAvailable}`,
        {
            method: "PATCH"
        }
    );
}

async function getPatients() {
    return apiRequest("/patients/");
}

async function getAvailableSlots(doctorId, date) {
    return apiRequest(`/appointments/available/${doctorId}/${date}`);
}

async function bookAppointment(payload) {
    return apiRequest("/appointments/", {
        method: "POST",
        body: JSON.stringify(payload)
    });
}

async function getPatientAppointments(patientId) {
    return apiRequest(`/appointments/patient/${patientId}`);
}

async function getDoctorAppointments(doctorId) {
    return apiRequest(`/appointments/doctor/${doctorId}`);
}

async function cancelAppointment(appointmentId) {
    return apiRequest(`/appointments/${appointmentId}/cancel`, {
        method: "PATCH"
    });
}