function showMessage(element, message, type = "error") {
    if (!element) return;

    element.textContent = message;
    element.className = `message ${type}`;
}

function logout() {
    localStorage.removeItem("ayurconnect_token");
    localStorage.removeItem("ayurconnect_user");
    localStorage.removeItem("ayurconnect_patient");
    localStorage.removeItem("ayurconnect_doctor");

    window.location.href = "index.html";
}

async function requireAuth() {
    const token = localStorage.getItem("ayurconnect_token");

    if (!token) {
        window.location.href = "login.html";
        return null;
    }

    try {
        const user = await getCurrentUser();

        localStorage.setItem(
            "ayurconnect_user",
            JSON.stringify(user)
        );

        return user;
    } catch (error) {
        localStorage.removeItem("ayurconnect_token");
        localStorage.removeItem("ayurconnect_user");

        window.location.href = "login.html";
        return null;
    }
}

async function redirectIfLoggedIn() {
    const token = localStorage.getItem("ayurconnect_token");

    if (!token) return;

    try {
        const user = await getCurrentUser();

        if (user.role === "doctor") {
            window.location.href = "doctor-dashboard.html";
        } else {
            window.location.href = "dashboard.html";
        }
    } catch {
        localStorage.removeItem("ayurconnect_token");
        localStorage.removeItem("ayurconnect_user");
    }
}

document.addEventListener("DOMContentLoaded", () => {

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {

        redirectIfLoggedIn();

        registerForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const message = document.getElementById("registerMessage");
            const button = document.getElementById("registerButton");

            const fullName =
                document.getElementById("full_name").value.trim();

            const email =
                document.getElementById("email").value.trim();

            const password =
                document.getElementById("password").value;

            const role =
                document.getElementById("role").value;

            if (!fullName || !email || !password) {
                showMessage(
                    message,
                    "Please fill in all required fields."
                );
                return;
            }

            if (password.length < 6) {
                showMessage(
                    message,
                    "Password must contain at least 6 characters."
                );
                return;
            }

            button.disabled = true;
            button.textContent = "Creating account...";

            try {

                const user = await registerUser({
                    email,
                    password,
                    full_name: fullName,
                    role
                });

                localStorage.setItem(
                    "ayurconnect_user",
                    JSON.stringify(user)
                );

                if (role === "doctor") {

                    localStorage.setItem(
                        "pending_doctor_registration",
                        "true"
                    );

                    showMessage(
                        message,
                        "Account created. Please complete your doctor profile after login.",
                        "success"
                    );

                } else {

                    showMessage(
                        message,
                        "Account created successfully. Redirecting to login...",
                        "success"
                    );
                }

                setTimeout(() => {
                    window.location.href = "login.html";
                }, 1000);

            } catch (error) {

                showMessage(
                    message,
                    error.message
                );

            } finally {

                button.disabled = false;
                button.textContent = "Create Account";
            }
        });
    }

    const loginForm = document.getElementById("loginForm");

    if (loginForm) {

        redirectIfLoggedIn();

        loginForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const message =
                document.getElementById("loginMessage");

            const button =
                document.getElementById("loginButton");

            const email =
                document.getElementById("loginEmail").value.trim();

            const password =
                document.getElementById("loginPassword").value;

            button.disabled = true;
            button.textContent = "Signing in...";

            try {

                const result = await loginUser({
                    email,
                    password
                });

                localStorage.setItem(
                    "ayurconnect_token",
                    result.access_token
                );

                const user = await getCurrentUser();

                localStorage.setItem(
                    "ayurconnect_user",
                    JSON.stringify(user)
                );

                if (user.role === "doctor") {
                    window.location.href = "doctor-dashboard.html";
                } else {
                    window.location.href = "dashboard.html";
                }

            } catch (error) {

                showMessage(
                    message,
                    error.message
                );

            } finally {

                button.disabled = false;
                button.textContent = "Login";
            }
        });
    }

    document
        .querySelectorAll("[data-logout]")
        .forEach(button => {
            button.addEventListener("click", logout);
        });
});