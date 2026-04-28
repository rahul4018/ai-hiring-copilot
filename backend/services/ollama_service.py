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


# ----------------------------------------
# Check Ollama Connection
# ----------------------------------------
def test_ollama_connection() -> bool:
    try:
        ollama.list()
        return True
    except Exception:
        return False


# ----------------------------------------
# Static fallback prep plan
# ----------------------------------------
def generate_static_prep_plan(
    missing_skills: List[str],
    job_title: str
) -> str:
    """
    Generates fallback prep plan when Ollama/Groq fails.
    """

    plan = f"""
7-Day Interview Prep Plan for {job_title}

Missing Skills:
{", ".join(missing_skills)}

Day 1:
Learn fundamentals of {missing_skills[0] if len(missing_skills) > 0 else "core concepts"}
Watch YouTube tutorials + read docs

Day 2:
Build small hands-on project using {missing_skills[1] if len(missing_skills) > 1 else "Python"}

Day 3:
Practice interview questions on:
{", ".join(missing_skills[:3])}

Day 4:
Solve implementation problems

Day 5:
Revise system design basics

Day 6:
Mock interview practice

Day 7:
Build final mini project + resume revision
"""

    return plan.strip()


# ----------------------------------------
# Generate Prep Plan
# ----------------------------------------
@lru_cache(maxsize=100)
def generate_prep_plan(
    missing_skills_tuple: tuple,
    job_title: str,
    experience_level: str = "junior"
) -> str:

    missing_skills = list(missing_skills_tuple)

    if not missing_skills:
        return (
            "No missing skills detected. "
            "Your resume aligns well with this job."
        )

    prompt = f"""
Create a concise 7-day interview prep plan for a {experience_level}
{job_title} candidate.

Missing skills:
{', '.join(missing_skills)}

For each day provide:
- Topic
- One learning resource
- One hands-on task

Keep output plain text only.
"""

    try:
        # -----------------------------
        # Groq fallback
        # -----------------------------
        if GROQ_FALLBACK:
            if not Groq:
                print("Groq SDK not installed → using static fallback")
                return generate_static_prep_plan(
                    missing_skills,
                    job_title
                )

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

        # -----------------------------
        # Ollama local
        # -----------------------------
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

    except Exception as e:
        print(f"AI model failed: {str(e)}")
        print("Using static fallback prep plan")

        return generate_static_prep_plan(
            missing_skills,
            job_title
        )


# ----------------------------------------
# Interview Questions
# ----------------------------------------
def generate_interview_questions(
    job_title: str,
    skills: List[str]
) -> List[str]:

    if not skills:
        return [
            "No skills provided for interview questions."
        ]

    prompt = f"""
Generate exactly 5 interview questions for a {job_title} role.

Focus on:
{', '.join(skills)}

Return only the questions.
"""

    try:
        if GROQ_FALLBACK:
            if not Groq:
                return [
                    "Groq SDK missing. Using manual preparation."
                ]

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
            f"Explain your experience with {skill}"
            for skill in skills[:5]
        ]


# ----------------------------------------
# Test
# ----------------------------------------
if __name__ == "__main__":
    print("Testing Ollama connection:")
    print(test_ollama_connection())

    sample_missing_skills = (
        "docker",
        "fastapi",
        "aws"
    )

    print("\nPrep Plan:\n")
    print(
        generate_prep_plan(
            sample_missing_skills,
            "Backend Engineer"
        )
    )

    print("\nInterview Questions:\n")
    questions = generate_interview_questions(
        "Backend Engineer",
        ["python", "fastapi", "sql"]
    )

    for q in questions:
        print(q)