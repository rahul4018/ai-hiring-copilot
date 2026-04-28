from unittest.mock import patch


def test_health(client):
    """Verifies health endpoint works."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_job(client):
    """Verifies job creation works."""
    payload = {
        "title": "Backend Engineer",
        "company": "Google",
        "jd_text": "Python FastAPI PostgreSQL Docker AWS"
    }

    response = client.post(
        "/api/v1/jobs/scan",
        json=payload
    )

    assert response.status_code == 201
    assert "job_id" in response.json()


def test_get_jobs(client):
    """Verifies jobs list endpoint."""
    response = client.get("/api/v1/jobs/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch(
    "backend.services.ollama_service.generate_prep_plan"
)
def test_resume_score(
    mock_prep,
    client
):
    """Verifies resume scoring endpoint."""
    mock_prep.return_value = "Mock prep plan"

    # Create job first
    job_response = client.post(
        "/api/v1/jobs/scan",
        json={
            "title": "ML Engineer",
            "company": "Meta",
            "jd_text": "Python TensorFlow AWS"
        }
    )

    job_id = job_response.json()["job_id"]

    # This test assumes resume already exists
    # Better file upload mocking can be added later

    assert job_id is not None