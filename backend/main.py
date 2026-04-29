from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

# Database
from backend.database import engine
from backend.models import Base, Job, Application, Resume, Score

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
    allow_origins=["*"],   # tighten later
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
    1. Checks DB connection
    2. Creates tables automatically
    """
    try:
        print("Checking database connection...")

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful")

        # Create all tables
        Base.metadata.create_all(bind=engine)

        print("Database tables created successfully")
        print("AI Hiring Copilot API started successfully")

    except Exception as e:
        print(f"Startup failed: {str(e)}")
        raise e


# ----------------------------------------
# Root Endpoint
# ----------------------------------------
@app.get("/")
async def root():
    return {
        "message": "AI Hiring Copilot API is running",
        "docs": "/docs",
        "health_check": "/health"
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
# Register Routers
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


# ----------------------------------------
# Local Run
# ----------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )