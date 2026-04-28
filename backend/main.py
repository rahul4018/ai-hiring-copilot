from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

# Database
from backend.database import engine
from backend.models import Base

# IMPORTANT:
# Explicitly import models so SQLAlchemy registers tables
from backend.models.job import Job
from backend.models.application import Application

# Add this if you have resume model
# from backend.models.resume import Resume

# Routers
from backend.routers import (
    jobs,
    resume,
    applications,
    insights
)

# ----------------------------------------
# FastAPI App Config
# ----------------------------------------
app = FastAPI(
    title="AI Hiring Copilot API",
    description="""
    AI-powered hiring assistant that:
    - scans job descriptions
    - extracts skills
    - scores resumes
    - generates interview prep plans
    - tracks job applications
    - provides hiring insights
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ----------------------------------------
# CORS Configuration
# ----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------
# Startup Event
# ----------------------------------------
@app.on_event("startup")
async def startup_event():
    """
    Runs when app starts:
    1. Tests DB connection
    2. Creates missing tables automatically
    """
    try:
        print("Checking database connection...")

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful")

        # Create all tables automatically
        Base.metadata.create_all(bind=engine)

        print("Database tables created successfully")
        print("AI Hiring Copilot API started successfully")

    except Exception as e:
        print(f"Startup failed: {str(e)}")


# ----------------------------------------
# Root Endpoint
# ----------------------------------------
@app.get("/")
async def root():
    return {
        "message": "AI Hiring Copilot API is running",
        "docs": "https://ai-hiring-copilot-qj5t.onrender.com/docs",
        "health_check": "https://ai-hiring-copilot-qj5t.onrender.com/health"
    }


# ----------------------------------------
# Health Check Endpoint
# ----------------------------------------
@app.get("/health")
async def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


# ----------------------------------------
# Register API Routers
# ----------------------------------------
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


# ----------------------------------------
# Global Exception Handler
# ----------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )