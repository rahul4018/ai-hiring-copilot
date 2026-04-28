# [LIVE DEMO](https://your-app.streamlit.app)

> Replace the link above after deploying your Streamlit app.

---

# AI Hiring Copilot

I built AI Hiring Copilot because job applications are painfully inefficient. I was manually reading job descriptions, comparing them against my resume, figuring out missing skills, preparing for interviews, and tracking applications in spreadsheets. It was repetitive and slow. I built this platform to automate that workflow using NLP, machine learning, and LLMs so a candidate can upload a resume, paste a job description, instantly see their match score, identify skill gaps, generate a personalized prep plan, and track applications in one dashboard.

---

# Dashboard Screenshot

![Dashboard Screenshot](./docs/dashboard-placeholder.png)

> Replace this image with actual screenshots after deployment.

---

# Architecture

```bash
                        +------------------+
                        |      User        |
                        +--------+---------+
                                 |
                                 v
                    +--------------------------+
                    |   Streamlit Frontend     |
                    | Resume Upload + Dashboard|
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    |      FastAPI Backend     |
                    |   REST API + Business    |
                    |         Logic            |
                    +------------+-------------+
                                 |
        ---------------------------------------------------------
        |                     |                 |                |
        v                     v                 v                v

+---------------+   +----------------+   +----------------+   +----------------+
| PostgreSQL DB |   | spaCy NLP      |   | TF-IDF Scorer  |   | Ollama / Groq |
| Job Storage   |   | Skill Extraction|  | Resume Match   |   | Prep Plans     |
+---------------+   +----------------+   +----------------+   +----------------+
```

---

# Key Features

### 1. Job Description Skill Extraction
Extracts technical skills from job descriptions using :contentReference[oaicite:0]{index=0} + regex matching.

- Supports 60+ predefined technical skills
- ~85% extraction accuracy on tested job descriptions

---

### 2. Resume Match Scoring
Scores resumes using TF-IDF cosine similarity via :contentReference[oaicite:1]{index=1}.

- Returns score from 0–100
- Identifies matched + missing skills

---

### 3. AI Interview Prep Plans
Generates personalized prep plans using:

- Local :contentReference[oaicite:2]{index=2} + :contentReference[oaicite:3]{index=3} (local development)
- :contentReference[oaicite:4]{index=4} fallback for deployment

Creates:

- 7-day learning plan
- free learning resources
- hands-on tasks

---

### 4. Application Tracking Dashboard
Tracks:

- Applied jobs
- Interviews
- Offers
- Follow-ups

Built using :contentReference[oaicite:5]{index=5} + :contentReference[oaicite:6]{index=6}.

---

### 5. Analytics Dashboard

Tracks:

- top missing skills
- match trends
- application funnel
- resume performance insights

---

# Tech Stack

| Tool | Purpose | Why I Chose It |
|--------|----------|----------------|
| :contentReference[oaicite:7]{index=7} | Backend APIs | Fast async APIs + automatic docs |
| :contentReference[oaicite:8]{index=8} | Database | Reliable relational storage |
| :contentReference[oaicite:9]{index=9} | Frontend | Fast dashboard development |
| :contentReference[oaicite:10]{index=10} | NLP | Lightweight skill extraction |
| :contentReference[oaicite:11]{index=11} | Resume scoring | Simple interpretable ML |
| :contentReference[oaicite:12]{index=12} | Local LLM | Free local experimentation |
| :contentReference[oaicite:13]{index=13} | Cloud LLM fallback | Required for deployment |

---

# Local Setup (Exactly 6 Commands)

```bash
git clone https://github.com/rahul4018/ai-hiring-copilot.git
cd ai-hiring-copilot
py -3.11 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
streamlit run frontend/app.py
```

Run backend separately:

```bash
uvicorn backend.main:app --reload
```

---

# API Documentation

### Scan Job Description

```bash
POST /api/v1/jobs/scan
```

Input:

- job title
- company
- job description text

Output:

- extracted skills
- job ID

---

### Score Resume

```bash
POST /api/v1/resume/score/{job_id}/{resume_id}
```

Output:

- match %
- missing skills
- prep plan

---

### Application Insights

```bash
GET /api/v1/insights/skill-gaps
```

Output:

- top missing skills
- frequency trends

---

# Benchmarks

| Metric | Result |
|---------|----------|
| Skill extraction accuracy | ~85% |
| Average API response time | 1.4s |
| Resume scoring latency | <500ms |
| Tested job descriptions | 50+ |
| Pytest coverage | 11 passing tests |

---

# What I Learned

Building NLP systems sounds easier than it is. My first version of skill extraction completely failed on obvious job descriptions because I relied too heavily on spaCy noun chunks. It missed explicit skill mentions like Python, AWS, and TensorFlow. I fixed this by adding direct keyword matching and regex fallback logic.

Managing local AI infrastructure was more annoying than expected. :contentReference[oaicite:14]{index=14} worked great locally, but it became useless for free cloud deployment because you can’t run local models on free hosting platforms. I had to redesign the architecture to support :contentReference[oaicite:15]{index=15} as a deployment fallback.

Testing exposed problems I would’ve missed manually. My PostgreSQL test database permissions broke API tests, and I had to debug schema permissions before all tests passed. That forced me to treat deployment and testing as actual engineering work—not an afterthought.

---

# Roadmap

### 1. Resume Parsing Improvements
Current parsing is PDF-only. I want DOCX support and better formatting retention.

---

### 2. Fine-Tuned Resume Matching
TF-IDF works well for MVPs, but embeddings could improve semantic understanding.

---

### 3. Authentication + User Accounts
Currently single-user only. Multi-user support would make this usable as a SaaS product.

---

# License

MIT License
