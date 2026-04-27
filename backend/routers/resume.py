import pdfplumber
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Resume, Job, Score
from backend.services.nlp_pipeline import extract_skills_from_text, get_missing_skills
from backend.services.scorer import compute_match_details
from backend.services.ollama_service import generate_prep_plan

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload PDF resume and extract skills."""
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(422, "Only PDF files supported")

        text = ""

        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        skills = extract_skills_from_text(text)

        resume = Resume(
            raw_text=text,
            skills=skills,
            uploaded_at=datetime.utcnow()
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return {
            "resume_id": str(resume.id),
            "skills_found": skills
        }

    except Exception as e:
        raise HTTPException(500, f"Resume upload failed: {str(e)}")


@router.post("/score/{job_id}/{resume_id}")
async def score_resume_endpoint(
    job_id: UUID,
    resume_id: UUID,
    db: Session = Depends(get_db)
):
    """Score resume against job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    if not resume:
        raise HTTPException(404, "Resume not found")

    details = compute_match_details(
        job.raw_jd,
        resume.raw_text,
        job.extracted_skills,
        resume.skills
    )

    prep_plan = generate_prep_plan(
        tuple(details["missing_skills"]),
        job.title
    )

    score = Score(
        job_id=job.id,
        resume_id=resume.id,
        match_percent=details["match_percent"],
        missing_skills=details["missing_skills"],
        prep_plan=prep_plan
    )

    db.add(score)
    db.commit()
    db.refresh(score)

    return {
        "score_id": str(score.id),
        **details,
        "prep_plan": prep_plan
    }


@router.get("/score/{job_id}/{resume_id}")
async def get_score(
    job_id: UUID,
    resume_id: UUID,
    db: Session = Depends(get_db)
):
    """Get cached score."""
    score = db.query(Score).filter(
        Score.job_id == job_id,
        Score.resume_id == resume_id
    ).first()

    if not score:
        raise HTTPException(404, "Score not found")

    return score