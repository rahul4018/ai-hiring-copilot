# AI Hiring Copilot Deployment Guide

This guide deploys:

- FastAPI backend → Render
- PostgreSQL → Render database
- Streamlit frontend → Streamlit Community Cloud
- LLM → Groq API fallback

---

# Step 1: Push latest code to GitHub

Run:

```bash
git status
git add .
git commit -m "deployment config added"
git push
```

Verify code exists on GitHub:
https://github.com/rahul4018/ai-hiring-copilot

---

# Step 2: Create Render account

Go to:

https://render.com

Sign up using GitHub.

Authorize Render to access your repo.

---

# Step 3: Create PostgreSQL database

In Render dashboard:

- Click **New**
- Click **PostgreSQL**
- Name: `ai-hiring-copilot-db`
- Select region closest to you
- Choose free plan (if available)

Click:

**Create Database**

After database is created:

- Open database dashboard
- Copy **External Database URL**

Example:

postgresql://user:password@host:5432/dbname

Save this.

---

# Step 4: Deploy FastAPI backend

In Render:

- Click **New**
- Click **Blueprint**
- Select GitHub repo
- Select `ai-hiring-copilot`

Render automatically detects:

`render.yaml`

Click:

**Apply**

---

# Step 5: Add environment variables

Open backend service → Environment

Add:

DATABASE_URL=your_render_database_url
GROQ_API_KEY=your_groq_api_key
GROQ_FALLBACK=True
ENVIRONMENT=production

Click Save Changes.

---

# Step 6: Get Groq API key

Go to:

https://console.groq.com

Sign up.

Generate API key.

Copy key.

Paste into Render environment variables.

Model used:

mixtral-8x7b-32768

---

# Step 7: Verify backend deployment

Open:

https://your-backend-name.onrender.com/docs

Check:

- /health
- /jobs
- /resume
- /applications

Test endpoints.

---

# Step 8: Deploy Streamlit frontend

Go to:

https://share.streamlit.io

Login with GitHub.

Click:

New App

Select:

- repo: ai-hiring-copilot
- branch: main
- file path: frontend/app.py

---

# Step 9: Add Streamlit secrets

In Streamlit app settings:

Secrets → Edit

Paste:

```toml
API_BASE_URL="https://your-render-backend-url.onrender.com/api/v1"
