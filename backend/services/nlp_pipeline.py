import re
import spacy
from typing import List, Set

# Load spaCy model ONCE at module level
nlp = spacy.load("en_core_web_md")


# Common technical skills taxonomy
SKILLS_TAXONOMY = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "fastapi", "flask", "django", "spring boot", "node.js", "express.js",
    "react", "angular", "vue", "html", "css", "bootstrap", "tailwind",
    "docker", "kubernetes", "git", "github", "gitlab", "jenkins",
    "aws", "azure", "gcp", "terraform", "linux", "bash",
    "machine learning", "deep learning", "nlp", "computer vision",
    "scikit-learn", "tensorflow", "pytorch", "keras",
    "pandas", "numpy", "matplotlib", "seaborn",
    "rest api", "graphql", "microservices",
    "spark", "hadoop", "airflow", "etl",
    "data analysis", "data engineering", "data science",
    "excel", "tableau", "power bi",
    "pytest", "unittest", "ci/cd",
    "oauth", "jwt", "postgres", "api development"
]


def normalize_text(text: str) -> str:
    """
    Normalize input text for easier matching.
    """
    if not text:
        return ""
    return text.lower().strip()


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract technical skills from job descriptions or resumes.

    Uses:
    - spaCy noun chunks
    - named entities
    - regex pattern matching
    - taxonomy lookup

    Returns:
        Sorted deduplicated list of skills
    """
    if not text or not text.strip():
        return []

    text = normalize_text(text)
    doc = nlp(text)

    found_skills: Set[str] = set()

    # Match noun chunks
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()

        if chunk_text in SKILLS_TAXONOMY:
            found_skills.add(chunk_text)

    # Match named entities
    for ent in doc.ents:
        ent_text = ent.text.lower().strip()

        if ent_text in SKILLS_TAXONOMY:
            found_skills.add(ent_text)

    # Direct taxonomy matching
    for skill in SKILLS_TAXONOMY:
        if skill in text:
            found_skills.add(skill)

    # Regex patterns
    regex_patterns = [
        r"experience with ([a-zA-Z0-9\+\#\.\- ]+)",
        r"(\d+\+?\s+years?\s+of\s+([a-zA-Z0-9\+\#\.\- ]+))",
        r"proficient in ([a-zA-Z0-9\+\#\.\- ]+)",
        r"knowledge of ([a-zA-Z0-9\+\#\.\- ]+)"
    ]

    for pattern in regex_patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            if isinstance(match, tuple):
                extracted = match[-1].strip().lower()
            else:
                extracted = match.strip().lower()

            for skill in SKILLS_TAXONOMY:
                if skill in extracted:
                    found_skills.add(skill)

    return sorted(found_skills)


def get_missing_skills(
    jd_skills: List[str],
    resume_skills: List[str]
) -> List[str]:
    """
    Find skills required in JD but missing in resume.

    Args:
        jd_skills: Skills extracted from job description
        resume_skills: Skills extracted from resume

    Returns:
        Missing skills list
    """
    if not jd_skills:
        return []

    jd_set = set(skill.lower() for skill in jd_skills)
    resume_set = set(skill.lower() for skill in resume_skills)

    missing = jd_set - resume_set

    return sorted(list(missing))


if __name__ == "__main__":
    sample_jd = """
    We are hiring a Backend Engineer with 3+ years of Python experience.
    Must have experience with FastAPI, PostgreSQL, Docker, AWS, Git,
    REST APIs, Pandas, and Machine Learning.
    NLP experience is a plus.
    """

    extracted = extract_skills_from_text(sample_jd)

    print("Extracted Skills:")
    print(extracted)

    sample_resume = [
        "python",
        "sql",
        "git",
        "pandas"
    ]

    missing = get_missing_skills(extracted, sample_resume)

    print("\nMissing Skills:")
    print(missing)

    print("\nAccuracy Note:")
    print(
        "This pipeline works well for explicit technical keywords, "
        "common frameworks, cloud tools, and programming languages. "
        "It may miss highly niche tools, abbreviations, spelling mistakes, "
        "or implicit skills not explicitly mentioned."
    )