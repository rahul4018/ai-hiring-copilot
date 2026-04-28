from backend.services.scorer import (
    score_resume,
    compute_match_details
)


def test_score_range():
    """Verifies score stays between 0-100."""
    score = score_resume(
        "Python FastAPI developer",
        "Python FastAPI engineer"
    )

    assert 0 <= score <= 100


def test_identical_text_high_score():
    """Verifies identical texts score high."""
    text = "Python FastAPI PostgreSQL Docker"

    score = score_resume(text, text)

    assert score > 90


def test_different_text_low_score():
    """Verifies unrelated texts score low."""
    score = score_resume(
        "Python machine learning engineer",
        "Graphic designer photoshop illustrator"
    )

    assert score < 30


def test_match_details_keys():
    """Verifies response contains required keys."""
    result = compute_match_details(
        "Python FastAPI",
        "Python",
        ["python", "fastapi"],
        ["python"]
    )

    required_keys = [
        "match_percent",
        "matched_skills",
        "missing_skills",
        "total_jd_skills"
    ]

    for key in required_keys:
        assert key in result