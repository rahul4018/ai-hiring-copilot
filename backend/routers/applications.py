from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Application, Job

router = APIRouter(prefix="/applications", tags=["Applications"])


class ApplicationCreate(BaseModel):
    job_id: UUID
    status: str
    applied_date: date
    followup_date: date | None = None


class NotesUpdate(BaseModel):
    notes: str


class StatusUpdate(BaseModel):
    status: str


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_application(
    data: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create job application."""
    app = Application(**data.model_dump())

    db.add(app)
    db.commit()
    db.refresh(app)

    return app


@router.get("/")
async def get_applications(db: Session = Depends(get_db)):
    """Get all applications."""
    apps = db.query(Application, Job).join(
        Job, Application.job_id == Job.id
    ).all()

    return [
        {
            "application_id": str(app.id),
            "job_title": job.title,
            "company": job.company,
            "status": app.status
        }
        for app, job in apps
    ]


@router.patch("/{app_id}/status")
async def update_status(
    app_id: UUID,
    data: StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update application status."""
    app = db.query(Application).filter(
        Application.id == app_id
    ).first()

    if not app:
        raise HTTPException(404, "Application not found")

    app.status = data.status
    db.commit()

    return {"message": "Status updated"}


@router.patch("/{app_id}/notes")
async def update_notes(
    app_id: UUID,
    data: NotesUpdate,
    db: Session = Depends(get_db)
):
    """Append notes."""
    app = db.query(Application).filter(
        Application.id == app_id
    ).first()

    if not app:
        raise HTTPException(404, "Application not found")

    current_notes = app.notes or ""
    app.notes = current_notes + "\n" + data.notes

    db.commit()

    return {"message": "Notes updated"}