const API_BASE_URL = "https://swasthyalink-sph1.onrender.com";

async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    const config = {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    };

    const token = localStorage.getItem("access_token");

    if (token) {
        config.headers["Authorization"] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(url, config);

        const contentType = response.headers.get("content-type");
        let data;

        if (contentType && contentType.includes("application/json")) {
            data = await response.json();
        } else {
            data = await response.text();
        }

        if (!response.ok) {
            let message = "Something went wrong";

            if (typeof data === "object" && data?.detail) {
                message = Array.isArray(data.detail)
                    ? data.detail.map(error => error.msg).join(", ")
                    : data.detail;
            } else if (typeof data === "string" && data) {
                message = data;
            }

            throw new Error(message);
        }

        return data;

    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}