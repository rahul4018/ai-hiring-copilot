from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from backend.database import engine
from backend.routers import (
    jobs,
    resume,
    applications,
    insights
)

# ----------------------------
# FastAPI App Config
# ----------------------------
app = FastAPI(
    title="AI Hiring Copilot API",
    description="""
    AI-powered hiring assistant that:
    - scans job descriptions
    - extracts skills
    - scores resumes
    - generates interview prep plans
    - tracks applications
    - provides hiring insights
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ----------------------------
# CORS Middleware
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Startup Event
# ----------------------------
@app.on_event("startup")
async def startup_event():
    """
    Verify database connection on app startup.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful")
        print("AI Hiring Copilot API started successfully")

    except Exception as e:
        print(f"Database connection failed: {str(e)}")


# ----------------------------
# Root Endpoint
# ----------------------------
@app.get("/")
async def root():
    """
    Root API endpoint.
    """
    return {
        "message": "AI Hiring Copilot API is running",
        "docs": "http://127.0.0.1:8000/docs",
        "health_check": "http://127.0.0.1:8000/health"
    }


# ----------------------------
# Health Check
# ----------------------------
@app.get("/health")
async def health():
    """
    Basic health check endpoint.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }


# ----------------------------
# API Routers
# ----------------------------
app.include_router(
    jobs.router,
    prefix="/api/v1"
)

app.include_router(
    resume.router,
    prefix="/api/v1"
)

app.include_router(
    applications.router,
    prefix="/api/v1"
)

app.include_router(
    insights.router,
    prefix="/api/v1"
)


# ----------------------------
# Global Exception Handler
# ----------------------------
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    """
    Catch unexpected server errors.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )