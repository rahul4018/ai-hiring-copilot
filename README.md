# AI Hiring Copilot

> AI-powered job application assistant — resume scoring, skill gap analysis, LLM interview prep, and application tracking in one self-hostable platform.

**[Live Demo](https://your-app.streamlit.app)** · [Report a Bug](https://github.com/rahul4018/ai-hiring-copilot/issues) · [API Docs](http://localhost:8000/docs)

---

## Why I built this

Job applications are repetitive and slow. I was manually reading job descriptions, comparing them against my resume, figuring out missing skills, preparing for interviews, and tracking everything in spreadsheets.

I built this to automate that workflow — paste a JD, upload your resume, get a match score, see your gaps, generate a prep plan, and track everything in one dashboard.

---

## Features

**Job description analysis**
Extracts 60+ technical skills from raw JD text using spaCy NLP + regex matching. ~85% extraction accuracy across 50+ tested descriptions.

**Resume match scoring**
TF-IDF cosine similarity scores your resume against a JD from 0–100, with a breakdown of matched vs. missing skills.

**AI interview prep**
Generates a personalised 7-day prep plan with free learning resources and hands-on tasks — powered by Ollama locally or Groq as a cloud fallback.

**Application tracker**
Track applied, interview, offer, and follow-up stages across all your applications.

**Analytics dashboard**
Top missing skills, match score trends, resume performance insights, and application funnel — all in one view.

---

## Architecture

```
                          User
                            │
                            ▼
               ┌────────────────────────┐
               │    Streamlit Frontend   │
               │  Resume upload · UI    │
               └────────────┬───────────┘
                            │
                            ▼
               ┌────────────────────────┐
               │    FastAPI Backend     │
               │  REST API · Business   │
               │  logic · Auth          │
               └────────────┬───────────┘
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼                  ▼
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │  PostgreSQL  │  │  spaCy NLP   │  │  TF-IDF      │  │  Ollama /    │
  │  (storage)   │  │  (skills)    │  │  (scoring)   │  │  Groq (LLM)  │
  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## Tech Stack

| Tool | Purpose | Why |
|---|---|---|
| FastAPI | Backend API | Async, fast, auto-generates `/docs` |
| PostgreSQL | Storage | Reliable relational DB for job + resume data |
| Streamlit | Frontend | Rapid dashboard development without React overhead |
| spaCy | Skill extraction | Lightweight NLP, runs locally |
| scikit-learn TF-IDF | Resume scoring | Interpretable, no GPU needed |
| Ollama | Local LLM | Free inference, no API key, good for dev |
| Groq | Cloud LLM fallback | Required for free-tier cloud deployment |

---

## Quickstart

**6 commands to run locally:**

```bash
git clone https://github.com/rahul4018/ai-hiring-copilot.git
cd ai-hiring-copilot
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run frontend/app.py
```

In a second terminal, start the API:

```bash
uvicorn backend.main:app --reload
```

Open `http://localhost:8501` — API docs at `http://localhost:8000/docs`.

> **Ollama setup (optional):** Install [Ollama](https://ollama.ai) and run `ollama pull mistral` for local LLM inference. Without it, the app uses Groq — add a `GROQ_API_KEY` to your `.env`.

---

## API Reference

### Scan a job description

```
POST /api/v1/jobs/scan
```

```json
{
  "job_title": "Backend Engineer",
  "company": "Acme Corp",
  "description": "We are looking for..."
}
```

Returns extracted skills and a `job_id` for subsequent scoring.

---

### Score a resume

```
POST /api/v1/resume/score/{job_id}/{resume_id}
```

```json
{
  "match_score": 74,
  "matched_skills": ["Python", "FastAPI", "PostgreSQL"],
  "missing_skills": ["Kubernetes", "Redis"],
  "prep_plan": "..."
}
```

---

### Skill gap insights

```
GET /api/v1/insights/skill-gaps
```

Returns top missing skills and frequency trends across all your tracked applications.

---

## Benchmarks

| Metric | Result |
|---|---|
| Skill extraction accuracy | ~85% on 50+ tested JDs |
| Average API response time | 1.4s |
| Resume scoring latency | < 500ms |
| Test suite | 11 passing pytest tests |

---

## What I actually learned building this

**spaCy noun chunks alone don't work for skill extraction.** My first version missed obvious mentions like `Python`, `AWS`, and `TensorFlow` because they appear as standalone tokens, not noun phrases. Fixed by adding direct keyword matching and regex fallback on top of the NLP layer.

**Local LLMs don't survive free cloud deployment.** Ollama works great locally but can't run on free hosting platforms — there's no way to spin up a local model process. Redesigned the architecture to treat Ollama as a dev-only path and Groq as the deployment path, switchable via environment variable.

**Testing exposes things manual QA misses.** PostgreSQL schema permissions broke my API tests in a way that never surfaced during manual use. Debugging it properly forced me to treat the test environment as a first-class concern — not an afterthought.

---

## Roadmap

- [ ] DOCX resume support (currently PDF only)
- [ ] Semantic matching with sentence embeddings (upgrade from TF-IDF)
- [ ] Multi-user auth — makes this viable as a SaaS product
- [ ] Browser extension for one-click JD capture
- [ ] Export prep plan to PDF

---

## License

MIT
