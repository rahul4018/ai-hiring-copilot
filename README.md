# AI Hiring Copilot

AI-powered platform that helps candidates optimize job applications by automating:

- Job description analysis
- Resume scoring
- Skill gap detection
- Interview preparation
- Application tracking
- Hiring insights

Instead of manually comparing resumes with job descriptions and tracking applications in spreadsheets, this platform handles everything in one workflow.

---

# Live Demo

## Frontend (Streamlit)
https://ai-hiring-copilot-m9pc6ioapmv5h9zvvendsu.streamlit.app

## Backend API (Render)
https://ai-hiring-copilot-qj5t.onrender.com

## API Documentation
https://ai-hiring-copilot-qj5t.onrender.com/docs

---

# Problem Statement

Job applications are inefficient.

Candidates typically:

- manually read job descriptions
- compare skills manually
- guess missing skills
- prepare randomly for interviews
- track applications in spreadsheets

This platform automates that workflow.

---

# System Architecture

```bash
User
 ↓
Streamlit Frontend
 ↓
FastAPI Backend
 ↓
-------------------------------------------
| PostgreSQL Database
| NLP Skill Extraction Engine
| Resume Matching Engine
| AI Prep Plan Generator
-------------------------------------------
```

---

# Core Features

## 1. Job Description Scanner

Users paste job descriptions.

System:

- extracts technical skills
- stores job data
- tracks hiring requirements

Example extracted skills:

- Python
- FastAPI
- SQL
- AWS
- Docker
- NLP
- PyTorch

---

## 2. Resume Scorer

Users upload resume PDF.

System:

- extracts resume text
- identifies candidate skills
- compares against job requirements
- generates match percentage

Output:

- match score
- matched skills
- missing skills

---

## 3. AI Interview Prep Plan

Generates personalized preparation roadmap based on missing skills.

Supports:

- Ollama (local development)
- Groq fallback
- static fallback for production reliability

Example:

- Day 1 → Learn FastAPI
- Day 2 → Build Docker project
- Day 3 → SQL practice

---

## 4. Application Tracker

Tracks:

- Applied
- Interview
- Rejected
- Offer
- Follow-up dates

---

## 5. Insights Dashboard

Shows:

- total applications
- interview count
- average match %
- top missing skills
- application funnel

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

## Frontend

- Streamlit

## NLP / ML

- spaCy
- TF-IDF
- Scikit-learn
- Regex matching

## AI Layer

- Ollama
- Groq

## Deployment

- Render
- Streamlit Cloud

---

# Project Structure

```bash
backend/
 ├── routers/
 ├── services/
 ├── models.py
 ├── database.py
 └── main.py

frontend/
 └── app.py

tests/
docs/
```

---

# API Endpoints

## Jobs

POST `/api/v1/jobs/`

GET `/api/v1/jobs/`

---

## Resume

POST `/api/v1/resume/upload`

POST `/api/v1/resume/score/{job_id}/{resume_id}`

---

## Applications

POST `/api/v1/applications/`

GET `/api/v1/applications/`

---

## Insights

GET `/api/v1/insights/dashboard`

---

# Local Setup

```bash
git clone https://github.com/rahul4018/ai-hiring-copilot.git
cd ai-hiring-copilot
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn backend.main:app --reload
```

Run frontend:

```bash
streamlit run frontend/app.py
```

---

# Real Problems Solved During Development

### Render deployment failure

Problem:

- spaCy model installation issues
- Python version conflicts

Fix:

- added runtime.txt
- added spaCy fallback logic

---

### PostgreSQL production failure

Problem:

- tables missing in production

Fix:

- automatic table creation on startup

---

### Resume scoring bug

Problem:

- PDF extraction returned empty text

Fix:

- switched to `BytesIO` parsing

---

### Ollama production failure

Problem:

- local models cannot run on Render free tier

Fix:

- added Groq + static fallback

---

# Future Improvements

- OCR support for scanned resumes
- semantic embeddings for better matching
- user authentication
- job scraping integrations
- email reminders

---

# Author

Rahul N

GitHub:
https://github.com/rahul4018

LinkedIn:
https://linkedin.com/in/rahul-n-in

---

# License

MIT License