from uuid import UUID
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Job, Score
from backend.services.nlp_pipeline import extract_skills_from_text

router = APIRouter(prefix="/jobs", tags=["Jobs"])


class JobCreate(BaseModel):
    title: str
    company: str
    jd_text: str


@router.post("/scan", status_code=status.HTTP_201_CREATED)
async def scan_job(job_data: JobCreate, db: Session = Depends(get_db)):
    """Scan job description, extract skills, save job."""
    try:
        skills = extract_skills_from_text(job_data.jd_text)

        job = Job(
            title=job_data.title,
            company=job_data.company,
            raw_jd=job_data.jd_text,
            extracted_skills=skills,
            created_at=datetime.utcnow()
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        return {
            "job_id": str(job.id),
            "extracted_skills": skills
        }

    except Exception as e:
        raise HTTPException(500, f"Failed to scan job: {str(e)}")


@router.get("/")
async def get_jobs(db: Session = Depends(get_db)):
    """Return all jobs."""
    jobs = db.query(Job).all()

    return [
        {
            "id": str(job.id),
            "title": job.title,
            "company": job.company,
            "created_at": job.created_at,
            "skill_count": len(job.extracted_skills or [])
        }
        for job in jobs
    ]


@router.get("/{job_id}")
async def get_job(job_id: UUID, db: Session = Depends(get_db)):
    """Return single job."""
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    return job


@router.delete("/{job_id}")
async def delete_job(job_id: UUID, db: Session = Depends(get_db)):
    """Delete job and related scores."""
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    db.query(Score).filter(Score.job_id == job_id).delete()
    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}