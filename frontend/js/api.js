const API_BASE_URL = "https://swasthyalink-sph1.onrender.com/api";


async function apiRequest(endpoint, options = {}) {

    const url = `${API_BASE_URL}${endpoint}`;

    const config = {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    };

    const token = localStorage.getItem("ayurconnect_token");

    if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
    }

    console.log("API REQUEST:", url);

    try {

        const response = await fetch(url, config);

        console.log("API RESPONSE:", response.status);

        const contentType =
            response.headers.get("content-type") || "";

        let data;

        if (contentType.includes("application/json")) {
            data = await response.json();
        } else {
            data = await response.text();
        }

        if (!response.ok) {

            let message = "Request failed";

            if (data && data.detail) {

                if (Array.isArray(data.detail)) {

                    message = data.detail
                        .map(error => error.msg)
                        .join(", ");

                } else {

                    message = data.detail;

                }
            }

            throw new Error(message);
        }

        return data;

    } catch (error) {

        console.error("API ERROR:", error);

        throw error;
    }
}


/* ==========================================
   REGISTER
========================================== */

async function registerUser(userData) {

    return await apiRequest(
        "/auth/register",
        {
            method: "POST",
            body: JSON.stringify(userData)
        }
    );
}


/* ==========================================
   LOGIN
========================================== */

async function loginUser(loginData) {

    return await apiRequest(
        "/auth/login",
        {
            method: "POST",
            body: JSON.stringify(loginData)
        }
    );
}


/* ==========================================
   CURRENT USER
========================================== */

async function getCurrentUser() {

    return await apiRequest(
        "/auth/me",
        {
            method: "GET"
        }
    );
}