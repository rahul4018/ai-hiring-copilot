import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Boolean,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.database import Base, engine


# ---------------------------------------------------
# JOBS TABLE
# Stores job descriptions uploaded by users
# ---------------------------------------------------
class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    raw_jd = Column(Text, nullable=False)
    extracted_skills = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Cascade delete scores when job is deleted
    scores = relationship(
        "Score",
        back_populates="job",
        cascade="all, delete-orphan"
    )

    # Cascade delete applications when job is deleted
    applications = relationship(
        "Application",
        back_populates="job",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Job(id={self.id}, "
            f"title={self.title}, "
            f"company={self.company})>"
        )


# ---------------------------------------------------
# RESUMES TABLE
# Stores parsed resume text + extracted skills
# ---------------------------------------------------
class Resume(Base):
    __tablename__ = "resumes"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    raw_text = Column(Text, nullable=False)
    skills = Column(JSONB, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Cascade delete scores when resume is deleted
    scores = relationship(
        "Score",
        back_populates="resume",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Resume(id={self.id})>"


# ---------------------------------------------------
# SCORES TABLE
# Stores resume-job match scoring results
# ---------------------------------------------------
class Score(Base):
    __tablename__ = "scores"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    resume_id = Column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False
    )

    match_percent = Column(Float, nullable=False)
    missing_skills = Column(JSONB, nullable=True)
    prep_plan = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship(
        "Job",
        back_populates="scores"
    )

    resume = relationship(
        "Resume",
        back_populates="scores"
    )

    def __repr__(self):
        return (
            f"<Score(id={self.id}, "
            f"match_percent={self.match_percent})>"
        )


# ---------------------------------------------------
# APPLICATIONS TABLE
# Tracks job applications and follow-ups
# ---------------------------------------------------
class Application(Base):
    __tablename__ = "applications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    status = Column(String(100), nullable=False)
    applied_date = Column(Date, nullable=True)
    followup_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship(
        "Job",
        back_populates="applications"
    )

    def __repr__(self):
        return (
            f"<Application(id={self.id}, "
            f"status={self.status})>"
        )


# ---------------------------------------------------
# SKILL GAPS TABLE
# Tracks commonly missing skills across resumes
# ---------------------------------------------------
class SkillGap(Base):
    __tablename__ = "skill_gaps"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    skill = Column(String(255), nullable=False)
    frequency = Column(Integer, default=0)
    in_resume = Column(Boolean, default=False)

    def __repr__(self):
        return (
            f"<SkillGap(skill={self.skill}, "
            f"frequency={self.frequency}, "
            f"in_resume={self.in_resume})>"
        )


# ---------------------------------------------------
# CREATE TABLES FUNCTION
# ---------------------------------------------------
def create_tables():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")