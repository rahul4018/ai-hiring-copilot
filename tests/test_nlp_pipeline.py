from backend.services.nlp_pipeline import (
    extract_skills_from_text,
    get_missing_skills
)


def test_extract_skills_known_jd():
    """Verifies known skills are extracted."""
    jd = """
    Looking for Python developer with FastAPI,
    PostgreSQL, Docker, AWS experience.
    """

    skills = extract_skills_from_text(jd)

    expected = [
        "python",
        "fastapi",
        "postgresql",
        "docker",
        "aws"
    ]

    for skill in expected:
        assert skill in skills


def test_extract_empty_text():
    """Verifies empty input returns empty list."""
    assert extract_skills_from_text("") == []


def test_missing_skills():
    """Verifies missing skill calculation."""
    jd_skills = ["python", "docker", "aws"]
    resume_skills = ["python"]

    missing = get_missing_skills(
        jd_skills,
        resume_skills
    )

    assert missing == ["aws", "docker"]