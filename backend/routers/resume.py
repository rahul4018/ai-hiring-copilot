import io
import pdfplumber

from uuid import UUID
from datetime import datetime

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Resume, Job, Score
from backend.services.nlp_pipeline import (
    extract_skills_from_text,
    get_missing_skills
)
from backend.services.scorer import compute_match_details
from backend.services.ollama_service import generate_prep_plan


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


# -----------------------------------------
# PDF TEXT EXTRACTION
# -----------------------------------------
def extract_resume_text(file_bytes: bytes) -> str:
    """
    Extract text safely from uploaded PDF.
    Works better on Render/cloud deployments.
    """
    extracted_text = ""

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    extracted_text += page_text + "\n"

    except Exception as e:
        raise Exception(f"PDF extraction failed: {str(e)}")

    return extracted_text.strip()


# -----------------------------------------
# Upload Resume
# -----------------------------------------
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload resume PDF
    Extract text
    Extract skills
    Store in database
    """
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=422,
                detail="Only PDF files are supported"
            )

        # Read file bytes properly
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        # Extract resume text
        resume_text = extract_resume_text(file_bytes)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume PDF"
            )

        print("\n===== EXTRACTED RESUME TEXT =====")
        print(resume_text[:2000])
        print("=================================\n")

        # Extract skills
        skills = extract_skills_from_text(resume_text)

        resume = Resume(
            raw_text=resume_text,
            skills=skills,
            uploaded_at=datetime.utcnow()
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return {
            "resume_id": str(resume.id),
            "skills_found": skills,
            "text_length": len(resume_text)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Resume upload failed: {str(e)}"
        )


# -----------------------------------------
# Score Resume
# -----------------------------------------
@router.post("/score/{job_id}/{resume_id}")
async def score_resume_endpoint(
    job_id: UUID,
    resume_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Score resume against job description
    """
    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

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


# -----------------------------------------
# Get Existing Score
# -----------------------------------------
@router.get("/score/{job_id}/{resume_id}")
async def get_score(
    job_id: UUID,
    resume_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Fetch previously generated score
    """
    score = db.query(Score).filter(
        Score.job_id == job_id,
        Score.resume_id == resume_id
    ).first()

    if not score:
        raise HTTPException(
            status_code=404,
            detail="Score not found"
        )

    return score