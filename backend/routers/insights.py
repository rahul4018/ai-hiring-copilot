from collections import Counter
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import get_db
from backend.models import Score, Application

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/skill-gaps")
async def skill_gaps(db: Session = Depends(get_db)):
    """Top missing skills."""
    scores = db.query(Score).all()

    all_skills = []

    for score in scores:
        all_skills.extend(score.missing_skills or [])

    counts = Counter(all_skills)

    return [
        {
            "skill": skill,
            "frequency": freq,
            "in_resume": False
        }
        for skill, freq in counts.most_common(10)
    ]


@router.get("/funnel")
async def application_funnel(db: Session = Depends(get_db)):
    """Application funnel stats."""
    results = db.query(
        Application.status,
        func.count(Application.id)
    ).group_by(Application.status).all()

    return [
        {
            "status": status,
            "count": count
        }
        for status, count in results
    ]


@router.get("/match-trend")
async def match_trend(db: Session = Depends(get_db)):
    """Weekly match trend."""
    four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)

    scores = db.query(Score).filter(
        Score.created_at >= four_weeks_ago
    ).all()

    weekly = {}

    for score in scores:
        week = score.created_at.strftime("%Y-%W")

        if week not in weekly:
            weekly[week] = []

        weekly[week].append(score.match_percent)

    return [
        {
            "week": week,
            "avg_match": round(sum(vals) / len(vals), 2)
        }
        for week, vals in weekly.items()
    ]