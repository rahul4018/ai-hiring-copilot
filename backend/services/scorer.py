import re
import string
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text: str) -> str:
    """
    Clean text before TF-IDF processing.

    Steps:
    - lowercase
    - remove punctuation
    - remove numbers
    - remove extra spaces
    """
    if not text or not text.strip():
        return ""

    text = text.lower()

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def score_resume(jd_text: str, resume_text: str) -> float:
    """
    Score resume against job description using TF-IDF cosine similarity.

    Why TF-IDF?
    - Lightweight
    - Fast
    - No external API cost
    - Works well for keyword-heavy resumes/JDs

    Cosine similarity measures:
    - How similar two text vectors are
    - Value between 0 and 1
    - Converted here to percentage (0-100)
    """
    if not jd_text.strip() or not resume_text.strip():
        return 0.0

    jd_clean = preprocess_text(jd_text)
    resume_clean = preprocess_text(resume_text)

    documents = [jd_clean, resume_clean]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


def compute_match_details(
    jd_text: str,
    resume_text: str,
    jd_skills: List[str],
    resume_skills: List[str]
) -> Dict:
    """
    Return detailed match breakdown.
    """
    match_score = score_resume(jd_text, resume_text)

    jd_skill_set = set(skill.lower() for skill in jd_skills)
    resume_skill_set = set(skill.lower() for skill in resume_skills)

    matched_skills = sorted(list(jd_skill_set.intersection(resume_skill_set)))
    missing_skills = sorted(list(jd_skill_set - resume_skill_set))

    return {
        "match_percent": round(match_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_jd_skills": len(jd_skill_set)
    }


def interpret_score(score: float) -> str:
    """
    Convert raw score into human-readable label.
    """
    if score >= 75:
        return "Strong match (75-100)"

    elif score >= 50:
        return "Partial match (50-74)"

    return "Weak match (below 50)"


if __name__ == "__main__":
    sample_jd = """
    Looking for a Python backend engineer with experience in FastAPI,
    PostgreSQL, Docker, AWS, REST APIs, machine learning,
    pandas, and Git.
    """

    sample_resume = """
    Software engineer with strong Python experience.
    Built APIs using FastAPI and Flask.
    Worked with PostgreSQL, Docker, Git, and pandas.
    """

    jd_skills = [
        "python",
        "fastapi",
        "postgresql",
        "docker",
        "aws",
        "rest api",
        "machine learning",
        "pandas",
        "git"
    ]

    resume_skills = [
        "python",
        "fastapi",
        "postgresql",
        "docker",
        "git",
        "pandas"
    ]

    score = score_resume(sample_jd, sample_resume)

    details = compute_match_details(
        sample_jd,
        sample_resume,
        jd_skills,
        resume_skills
    )

    print("Resume Score:", score)
    print("Score Interpretation:", interpret_score(score))
    print("\nMatch Details:")
    print(details)