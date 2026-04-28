import re
import string
from typing import List, Dict, Set

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ----------------------------------------
# Skill Alias Mapping
# ----------------------------------------
SKILL_ALIASES = {
    "machine learning": ["ml", "ml models"],
    "artificial intelligence": ["ai"],
    "nlp": ["natural language processing"],
    "aws": ["amazon web services", "sagemaker"],
    "fastapi": ["rest api", "api development", "backend api"],
    "postgresql": ["postgres", "postgres db"],
    "pytorch": ["torch"],
    "docker": ["containerization"],
    "javascript": ["js"],
    "typescript": ["ts"]
}


# ----------------------------------------
# Text Cleaning
# ----------------------------------------
def preprocess_text(text: str) -> str:
    """
    Clean text before TF-IDF processing
    """
    if not text or not text.strip():
        return ""

    text = text.lower()

    # remove numbers
    text = re.sub(r"\d+", "", text)

    # remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ----------------------------------------
# Expand Skill Aliases
# ----------------------------------------
def expand_skill_set(skills: List[str]) -> Set[str]:
    expanded = set()

    for skill in skills:
        skill = skill.lower().strip()
        expanded.add(skill)

        # expand aliases
        for main_skill, aliases in SKILL_ALIASES.items():

            if skill == main_skill:
                expanded.update(aliases)

            elif skill in aliases:
                expanded.add(main_skill)
                expanded.update(aliases)

    return expanded


# ----------------------------------------
# TF-IDF Resume Score
# ----------------------------------------
def score_resume(jd_text: str, resume_text: str) -> float:
    """
    Calculate semantic similarity using TF-IDF
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


# ----------------------------------------
# Match Details
# ----------------------------------------
def compute_match_details(
    jd_text: str,
    resume_text: str,
    jd_skills: List[str],
    resume_skills: List[str]
) -> Dict:
    """
    Returns:
    - overall similarity score
    - matched skills
    - missing skills
    """

    match_score = score_resume(jd_text, resume_text)

    expanded_jd_skills = expand_skill_set(jd_skills)
    expanded_resume_skills = expand_skill_set(resume_skills)

    matched_skills = []
    missing_skills = []

    for skill in jd_skills:
        skill_lower = skill.lower()

        matched = False

        if skill_lower in expanded_resume_skills:
            matched = True

        else:
            aliases = SKILL_ALIASES.get(skill_lower, [])

            for alias in aliases:
                if alias in expanded_resume_skills:
                    matched = True
                    break

        if matched:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    return {
        "match_percent": match_score,
        "match_label": interpret_score(match_score),
        "matched_skills": sorted(list(set(matched_skills))),
        "missing_skills": sorted(list(set(missing_skills))),
        "total_jd_skills": len(jd_skills),
        "matched_count": len(set(matched_skills)),
        "missing_count": len(set(missing_skills))
    }


# ----------------------------------------
# Human-readable Score Labels
# ----------------------------------------
def interpret_score(score: float) -> str:
    if score >= 80:
        return "Excellent Match"

    elif score >= 65:
        return "Strong Match"

    elif score >= 50:
        return "Moderate Match"

    elif score >= 30:
        return "Weak Match"

    return "Poor Match"


# ----------------------------------------
# Test
# ----------------------------------------
if __name__ == "__main__":

    sample_jd = """
    Looking for a Python backend engineer with experience in FastAPI,
    PostgreSQL, Docker, AWS, REST APIs, machine learning,
    pandas, and Git.
    """

    sample_resume = """
    Software engineer with strong Python experience.
    Built APIs using FastAPI and Flask.
    Worked with Postgres, Docker, Git,
    pandas, ML models, and AWS SageMaker.
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
        "postgres",
        "docker",
        "git",
        "pandas",
        "ml",
        "sagemaker"
    ]

    result = compute_match_details(
        sample_jd,
        sample_resume,
        jd_skills,
        resume_skills
    )

    print("\nResume Match Results")
    print("----------------------")
    print(result)