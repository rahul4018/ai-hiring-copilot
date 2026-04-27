import os
from functools import lru_cache
from typing import List

import ollama
from dotenv import load_dotenv

# Optional Groq fallback
try:
    from groq import Groq
except ImportError:
    Groq = None


load_dotenv()

OLLAMA_MODEL = "mistral"
GROQ_FALLBACK = os.getenv("GROQ_FALLBACK", "False").lower() == "true"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def test_ollama_connection() -> bool:
    """
    Test if local Ollama server is running.

    Example:
        >>> test_ollama_connection()
        True
    """
    try:
        ollama.list()
        return True
    except Exception:
        return False


@lru_cache(maxsize=100)
def generate_prep_plan(
    missing_skills_tuple: tuple,
    job_title: str,
    experience_level: str = "junior"
) -> str:
    """
    Generate a 7-day interview prep plan.

    Example:
        Input:
            missing_skills = ["docker", "aws", "fastapi"]
            job_title = "Backend Engineer"

        Output:
            Day 1: Docker basics...
            Day 2: AWS deployment...
    """

    missing_skills = list(missing_skills_tuple)

    if not missing_skills:
        return (
            "No missing skills detected. Your resume aligns well "
            "with this job description."
        )

    prompt = f"""
    Create a concise 7-day interview prep plan for a {experience_level}
    {job_title} candidate.

    Missing skills:
    {', '.join(missing_skills)}

    For each day provide:
    - Topic
    - One free learning resource
    - One hands-on task

    Keep output plain text only.
    """

    try:
        if GROQ_FALLBACK:
            if not Groq:
                return "Groq SDK not installed."

            client = Groq(api_key=GROQ_API_KEY)

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response.choices[0].message.content.strip()

        else:
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response["message"]["content"].strip()

    except Exception:
        return (
            "Could not generate prep plan because Ollama "
            "is not running. Start Ollama and try again."
        )


def generate_interview_questions(
    job_title: str,
    skills: List[str]
) -> List[str]:
    """
    Generate likely interview questions.

    Example:
        Input:
            job_title = "Backend Engineer"
            skills = ["python", "fastapi"]

        Output:
            [
                "Explain FastAPI dependency injection",
                ...
            ]
    """

    if not skills:
        return ["No skills provided for interview question generation."]

    prompt = f"""
    Generate exactly 5 interview questions for a {job_title} role.

    Focus on:
    {', '.join(skills)}

    Return only the questions.
    """

    try:
        if GROQ_FALLBACK:
            if not Groq:
                return ["Groq SDK not installed."]

            client = Groq(api_key=GROQ_API_KEY)

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            raw_output = response.choices[0].message.content.strip()

        else:
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            raw_output = response["message"]["content"].strip()

        questions = [
            q.strip("- ").strip()
            for q in raw_output.split("\n")
            if q.strip()
        ]

        return questions[:5]

    except Exception:
        return [
            "Unable to generate interview questions. "
            "Ensure Ollama is running."
        ]


if __name__ == "__main__":
    print("Testing Ollama connection...")
    print(test_ollama_connection())

    sample_missing_skills = (
        "docker",
        "aws",
        "kubernetes"
    )

    print("\nGenerating prep plan...\n")
    plan = generate_prep_plan(
        sample_missing_skills,
        "Backend Engineer"
    )
    print(plan)

    print("\nGenerating interview questions...\n")
    questions = generate_interview_questions(
        "Backend Engineer",
        ["python", "fastapi", "postgresql"]
    )

    for q in questions:
        print(q)