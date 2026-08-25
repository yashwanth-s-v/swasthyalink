/* ==========================================
   SWASTHYALINK AUTHENTICATION
========================================== */


/* ==========================================
   REGISTER
========================================== */

async function handleRegister(event) {

    event.preventDefault();

    const fullNameElement = document.getElementById("full_name");
    const nameElement = document.getElementById("name");

    const emailElement = document.getElementById("email");
    const passwordElement = document.getElementById("password");
    const roleElement = document.getElementById("role");

    /*
     * Some versions of the register page may use
     * "name" instead of "full_name".
     *
     * We support both.
     */

    const fullName =
        fullNameElement?.value ||
        nameElement?.value ||
        "";

    const email =
        emailElement?.value ||
        "";

    const password =
        passwordElement?.value ||
        "";

    const role =
        roleElement?.value ||
        "patient";


    if (!fullName.trim()) {
        alert("Please enter your full name.");
        return;
    }

    if (!email.trim()) {
        alert("Please enter your email.");
        return;
    }

    if (!password) {
        alert("Please enter your password.");
        return;
    }


    const userData = {

        /*
         * IMPORTANT:
         * Backend expects full_name,
         * NOT name.
         */
        full_name: fullName.trim(),

        email: email.trim(),

        password: password,

        role: role

    };


    try {

        console.log("Registering user:", {
            full_name: userData.full_name,
            email: userData.email,
            role: userData.role
        });


        const result = await registerUser(userData);


        console.log("Registration successful:", result);


        alert("Registration successful! Please login.");

        window.location.href = "login.html";


    } catch (error) {

        console.error("Registration failed:", error);

        alert(
            "Registration failed: " +
            (error.message || "Unable to connect to server.")
        );

    }

}


/* ==========================================
   LOGIN
========================================== */

async function handleLogin(event) {

    event.preventDefault();


    const emailElement =
        document.getElementById("email");

    const passwordElement =
        document.getElementById("password");


    const email =
        emailElement?.value?.trim() || "";

    const password =
        passwordElement?.value || "";


    if (!email) {
        alert("Please enter your email.");
        return;
    }

    if (!password) {
        alert("Please enter your password.");
        return;
    }


    try {

        const result = await loginUser({

            email: email,

            password: password

        });


        console.log("Login successful:", result);


        /*
         * Backend may return the token
         * under different common names.
         */

        const token =
            result.access_token ||
            result.token;


        if (token) {

            localStorage.setItem(
                "ayurconnect_token",
                token
            );

        }


        if (result.user) {

            localStorage.setItem(
                "ayurconnect_user",
                JSON.stringify(result.user)
            );

        }


        alert("Login successful!");


        /*
         * Redirect based on role if available.
         */

        const role =
            result.user?.role ||
            result.role ||
            "patient";


        if (role === "doctor") {

            window.location.href =
                "doctor-dashboard.html";

        } else {

            window.location.href =
                "dashboard.html";

        }


    } catch (error) {

        console.error("Login failed:", error);

        alert(
            "Login failed: " +
            (error.message || "Unable to connect to server.")
        );

    }

}


/* ==========================================
   LOGOUT
========================================== */

function logoutUser() {

    localStorage.removeItem(
        "ayurconnect_token"
    );

    localStorage.removeItem(
        "ayurconnect_user"
    );

    window.location.href =
        "login.html";
}


/* ==========================================
   REGISTER PAGE
========================================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const registerForm =
            document.getElementById("registerForm");

        if (registerForm) {

            registerForm.addEventListener(
                "submit",
                handleRegister
            );

        }


        const loginForm =
            document.getElementById("loginForm");

        if (loginForm) {

            loginForm.addEventListener(
                "submit",
                handleLogin
            );

        }

    }
);