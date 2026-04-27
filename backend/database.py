import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing in .env file")

# PostgreSQL engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # shows SQL queries in terminal (disable in production)
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

# Base model class
Base = declarative_base()


def get_db():
    """
    FastAPI dependency to get DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()