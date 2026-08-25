from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

from database.database import init_db

from api.health import router as health_router
from api.chat import router as chat_router
from api.auth import router as auth_router
from api.doctors import router as doctors_router
from api.appointments import router as appointments_router
from api.patients import router as patients_router


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AyurConnect - AI-powered Ayurveda wellness "
        "guidance and doctor connection platform."
    )
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        # Production frontend
        "https://swasthyalink-1.onrender.com",

        # Local development
        "http://127.0.0.1:5500",
        "http://localhost:5500",

        "http://127.0.0.1:3000",
        "http://localhost:3000",

        "http://127.0.0.1:5173",
        "http://localhost:5173",

        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# DATABASE
# ============================================================

try:

    init_db()

    print("Database initialized successfully.")

except Exception as error:

    print(
        f"Database initialization warning: {error}"
    )


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    health_router,
    prefix="/api"
)


app.include_router(
    chat_router,
    prefix="/api"
)


app.include_router(
    auth_router,
    prefix="/api"
)


app.include_router(
    doctors_router,
    prefix="/api"
)


app.include_router(
    appointments_router,
    prefix="/api"
)


app.include_router(
    patients_router,
    prefix="/api"
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():

    return {

        "application": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "status": "running",

        "message": "AyurConnect backend is running"

    }