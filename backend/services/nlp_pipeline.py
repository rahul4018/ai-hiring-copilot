import re
import spacy
from typing import List, Set

# -----------------------------------------
# Load lightweight spaCy model for Render
# -----------------------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None
    print("spaCy model not found. Install using:")
    print("python -m spacy download en_core_web_sm")


# -----------------------------------------
# Tech Skills Taxonomy
# -----------------------------------------
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


# -----------------------------------------
# Normalize text
# -----------------------------------------
def normalize_text(text: str) -> str:
    if not text:
        return ""

    return text.lower().strip()


# -----------------------------------------
# Extract skills
# -----------------------------------------
def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract technical skills from JD/resume text.
    """

    if not text or not text.strip():
        return []

    text = normalize_text(text)
    found_skills: Set[str] = set()

    # -----------------------------
    # Direct keyword matching
    # -----------------------------
    for skill in SKILLS_TAXONOMY:
        if " " in skill:
            if skill in text:
                found_skills.add(skill)
        else:
            pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, text):
                found_skills.add(skill)

    # -----------------------------
    # spaCy matching (only if model loaded)
    # -----------------------------
    if nlp:
        doc = nlp(text)

        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower().strip()
            if chunk_text in SKILLS_TAXONOMY:
                found_skills.add(chunk_text)

        for ent in doc.ents:
            ent_text = ent.text.lower().strip()
            if ent_text in SKILLS_TAXONOMY:
                found_skills.add(ent_text)

    # -----------------------------
    # Regex patterns
    # -----------------------------
    regex_patterns = [
        r"experience with ([a-zA-Z0-9\+\#\.\- ]+)",
        r"proficient in ([a-zA-Z0-9\+\#\.\- ]+)",
        r"knowledge of ([a-zA-Z0-9\+\#\.\- ]+)"
    ]

    for pattern in regex_patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            extracted = match.strip().lower()

            for skill in SKILLS_TAXONOMY:
                if skill in extracted:
                    found_skills.add(skill)

    return sorted(found_skills)


# -----------------------------------------
# Missing skills
# -----------------------------------------
def get_missing_skills(
    jd_skills: List[str],
    resume_skills: List[str]
) -> List[str]:

    if not jd_skills:
        return []

    jd_set = set(jd_skills)
    resume_set = set(resume_skills)

    missing = jd_set - resume_set

    return sorted(list(missing))


# -----------------------------------------
# Test
# -----------------------------------------
if __name__ == "__main__":
    sample_jd = """
    Looking for AI Engineer with Python,
    TensorFlow, PyTorch, AWS, SQL, Git.
    """

    skills = extract_skills_from_text(sample_jd)
    print("Extracted Skills:", skills)  