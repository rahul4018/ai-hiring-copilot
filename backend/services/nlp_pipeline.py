import re
import spacy
from typing import List, Set

# Load spaCy model once
nlp = spacy.load("en_core_web_md")


# ---------------------------------------------------
# Tech Skills Taxonomy
# ---------------------------------------------------
SKILLS_TAXONOMY = [
    "python", "java", "javascript", "typescript",
    "c++", "c#", "go", "rust",

    "sql", "mysql", "postgresql", "postgres",
    "mongodb", "redis", "sqlite",

    "fastapi", "flask", "django",
    "spring boot", "node.js", "express.js",

    "react", "angular", "vue",
    "html", "css", "bootstrap", "tailwind",

    "docker", "kubernetes",
    "git", "github", "gitlab", "jenkins",

    "aws", "azure", "gcp", "google cloud",
    "terraform", "linux", "bash",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "computer vision",

    "scikit-learn",
    "tensorflow",
    "pytorch",
    "keras",

    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",

    "rest api",
    "graphql",
    "microservices",

    "spark",
    "hadoop",
    "hive",
    "airflow",
    "etl",

    "data analysis",
    "data engineering",
    "data science",

    "excel",
    "tableau",
    "power bi",

    "pytest",
    "unittest",
    "ci/cd",

    "oauth",
    "jwt",
    "api development",

    "agile",
    "scrum",
    "algorithms",
    "data structures",
    "predictive modeling",
    "statistical analysis"
]


# ---------------------------------------------------
# Normalize text
# ---------------------------------------------------
def normalize_text(text: str) -> str:
    """
    Normalize input text.
    """
    if not text:
        return ""

    return text.lower().strip()


# ---------------------------------------------------
# Extract skills
# ---------------------------------------------------
def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract technical skills from job descriptions/resumes.

    Uses:
    - spaCy noun chunks
    - named entities
    - regex pattern matching
    - direct taxonomy keyword matching

    Returns:
        Sorted deduplicated skill list
    """

    if not text or not text.strip():
        return []

    text = normalize_text(text)
    doc = nlp(text)

    found_skills: Set[str] = set()

    # -----------------------------------
    # 1. Noun chunks
    # -----------------------------------
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()

        if chunk_text in SKILLS_TAXONOMY:
            found_skills.add(chunk_text)

    # -----------------------------------
    # 2. Named entities
    # -----------------------------------
    for ent in doc.ents:
        ent_text = ent.text.lower().strip()

        if ent_text in SKILLS_TAXONOMY:
            found_skills.add(ent_text)

    # -----------------------------------
    # 3. Direct keyword matching
    # -----------------------------------
    for skill in SKILLS_TAXONOMY:

        # multi-word skill
        if " " in skill:
            if skill in text:
                found_skills.add(skill)

        # single-word skill → use word boundaries
        else:
            pattern = rf"\b{re.escape(skill)}\b"

            if re.search(pattern, text):
                found_skills.add(skill)

    # -----------------------------------
    # 4. Regex skill patterns
    # -----------------------------------
    regex_patterns = [
        r"experience with ([a-zA-Z0-9\+\#\.\- ]+)",
        r"(\d+\+?\s+years?\s+of\s+([a-zA-Z0-9\+\#\.\- ]+))",
        r"proficient in ([a-zA-Z0-9\+\#\.\- ]+)",
        r"knowledge of ([a-zA-Z0-9\+\#\.\- ]+)",
        r"experience in ([a-zA-Z0-9\+\#\.\- ]+)"
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


# ---------------------------------------------------
# Missing skills
# ---------------------------------------------------
def get_missing_skills(
    jd_skills: List[str],
    resume_skills: List[str]
) -> List[str]:
    """
    Find missing skills between JD and resume.
    """

    if not jd_skills:
        return []

    jd_set = {skill.lower() for skill in jd_skills}
    resume_set = {skill.lower() for skill in resume_skills}

    missing = jd_set - resume_set

    return sorted(list(missing))


# ---------------------------------------------------
# Test block
# ---------------------------------------------------
if __name__ == "__main__":

    sample_jd = """
    We are hiring an AI/ML Engineer.

    Requirements:
    - Python
    - TensorFlow
    - PyTorch
    - NLP
    - AWS
    - SQL
    - Git
    - Spark
    - Hadoop
    - Tableau
    - Deep Learning
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

    missing = get_missing_skills(
        extracted,
        sample_resume
    )

    print("\nMissing Skills:")
    print(missing)

    print("\nAccuracy Note:")
    print(
        "Works well for explicit technical skills, frameworks, cloud tools, "
        "and programming languages. May still miss niche tools, misspellings, "
        "or highly implicit skill mentions."
    )