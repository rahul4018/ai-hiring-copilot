import os
import requests
import streamlit as st
import pandas as pd

# ----------------------------
# Streamlit Config
# ----------------------------
st.set_page_config(
    page_title="AI Hiring Copilot",
    layout="wide"
)

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000/api/v1"
)


# ----------------------------
# Cached GET APIs
# ----------------------------
@st.cache_data(ttl=60)
def get_jobs():
    try:
        res = requests.get(f"{API_BASE_URL}/jobs/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to fetch jobs: {e}")
        return []


@st.cache_data(ttl=60)
def get_applications():
    try:
        res = requests.get(f"{API_BASE_URL}/applications/")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to fetch applications: {e}")
        return []


@st.cache_data(ttl=60)
def get_skill_gaps():
    try:
        res = requests.get(f"{API_BASE_URL}/insights/skill-gaps")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to fetch skill gaps: {e}")
        return []


@st.cache_data(ttl=60)
def get_funnel():
    try:
        res = requests.get(f"{API_BASE_URL}/insights/funnel")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to fetch funnel data: {e}")
        return []


@st.cache_data(ttl=60)
def get_match_trend():
    try:
        res = requests.get(f"{API_BASE_URL}/insights/match-trend")
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Failed to fetch match trend: {e}")
        return []


# ----------------------------
# Sidebar Navigation
# ----------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "JD Scanner",
        "Resume Scorer",
        "Application Tracker",
        "Insights Dashboard"
    ]
)


# =====================================================
# PAGE 1 — JD Scanner
# =====================================================
if page == "JD Scanner":
    st.title("Job Description Scanner")

    title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    jd_text = st.text_area("Paste Job Description")

    if st.button("Scan JD"):
        if not title or not company or not jd_text:
            st.error("All fields are required.")
            st.stop()

        try:
            with st.spinner("Scanning job description..."):
                payload = {
                    "title": title,
                    "company": company,
                    "jd_text": jd_text
                }

                res = requests.post(
                    f"{API_BASE_URL}/jobs/scan",
                    json=payload
                )
                res.raise_for_status()

                data = res.json()

                st.success("JD scanned successfully")
                st.write(f"Skills found: {len(data['extracted_skills'])}")

                for skill in data["extracted_skills"]:
                    st.success(skill)

                # refresh cached data
                st.cache_data.clear()
                st.rerun()

        except Exception as e:
            st.error(f"JD scan failed: {e}")

    st.subheader("Previously Scanned Jobs")
    jobs = get_jobs()

    if jobs:
        st.dataframe(pd.DataFrame(jobs))


# =====================================================
# PAGE 2 — Resume Scorer
# =====================================================
elif page == "Resume Scorer":
    st.title("Resume Scorer")

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    jobs = get_jobs()

    if jobs:
        job_map = {
            f"{job['title']} - {job['company']}": job["id"]
            for job in jobs
        }

        selected_job = st.selectbox(
            "Select Job",
            list(job_map.keys())
        )

        if st.button("Score My Resume"):

            if uploaded_file is None:
                st.error("Please upload a resume PDF first.")
                st.stop()

            try:
                # Upload Resume
                with st.spinner("Uploading resume..."):
                    files = {
                        "file": uploaded_file
                    }

                    upload_res = requests.post(
                        f"{API_BASE_URL}/resume/upload",
                        files=files
                    )
                    upload_res.raise_for_status()

                    resume_data = upload_res.json()
                    resume_id = resume_data["resume_id"]

                # Score Resume
                with st.spinner("Scoring resume..."):
                    job_id = job_map[selected_job]

                    score_res = requests.post(
                        f"{API_BASE_URL}/resume/score/{job_id}/{resume_id}"
                    )
                    score_res.raise_for_status()

                    score_data = score_res.json()

                    score = score_data["match_percent"]

                    # Score color logic
                    if score >= 70:
                        st.success(f"Match Score: {score}%")
                    elif score >= 50:
                        st.warning(f"Match Score: {score}%")
                    else:
                        st.error(f"Match Score: {score}%")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Matched Skills")
                        if score_data["matched_skills"]:
                            for skill in score_data["matched_skills"]:
                                st.success(skill)
                        else:
                            st.info("No matched skills found")

                    with col2:
                        st.subheader("Missing Skills")
                        if score_data["missing_skills"]:
                            for skill in score_data["missing_skills"]:
                                st.error(skill)
                        else:
                            st.success("No missing skills")

                    with st.expander("Prep Plan"):
                        st.write(score_data["prep_plan"])

                    st.cache_data.clear()

            except Exception as e:
                st.error(f"Resume scoring failed: {e}")


# =====================================================
# PAGE 3 — Application Tracker
# =====================================================
elif page == "Application Tracker":
    st.title("Application Tracker")

    jobs = get_jobs()

    if jobs:
        job_map = {
            f"{job['title']} - {job['company']}": job["id"]
            for job in jobs
        }

        with st.form("application_form"):
            selected_job = st.selectbox(
                "Select Job",
                list(job_map.keys())
            )

            status = st.selectbox(
                "Status",
                ["Applied", "Interview", "Rejected", "Offer"]
            )

            applied_date = st.date_input("Applied Date")
            followup_date = st.date_input("Followup Date")

            submitted = st.form_submit_button(
                "Track Application"
            )

            if submitted:
                try:
                    payload = {
                        "job_id": job_map[selected_job],
                        "status": status,
                        "applied_date": str(applied_date),
                        "followup_date": str(followup_date)
                    }

                    res = requests.post(
                        f"{API_BASE_URL}/applications/",
                        json=payload
                    )

                    res.raise_for_status()

                    st.success("Application added successfully")

                    st.cache_data.clear()
                    st.rerun()

                except Exception as e:
                    st.error(f"Application tracking failed: {e}")

    st.subheader("Tracked Applications")

    apps = get_applications()

    if apps:
        for app in apps:
            with st.expander(
                f"{app['company']} | {app['job_title']} | {app['status']}"
            ):
                st.write(app)
    else:
        st.info("No applications tracked yet.")


# =====================================================
# PAGE 4 — Insights Dashboard
# =====================================================
elif page == "Insights Dashboard":
    st.title("Insights Dashboard")

    apps = get_applications()
    funnel = get_funnel()
    gaps = get_skill_gaps()
    trend = get_match_trend()

    total_apps = len(apps)

    interviews = len([
        app for app in apps
        if app["status"] == "Interview"
    ])

    avg_match = 0
    if trend:
        avg_match = round(
            sum(item["avg_match"] for item in trend) / len(trend),
            2
        )

    top_skill = gaps[0]["skill"] if gaps else "N/A"

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Applications", total_apps)
    c2.metric("Interviews", interviews)
    c3.metric("Avg Match %", avg_match)
    c4.metric("Top Missing Skill", top_skill)

    # Skill Gap Chart
    if gaps:
        st.subheader("Top Skill Gaps")
        gap_df = pd.DataFrame(gaps)
        st.bar_chart(
            gap_df.set_index("skill")["frequency"]
        )

    # Funnel Chart
    if funnel:
        st.subheader("Application Funnel")
        funnel_df = pd.DataFrame(funnel)
        st.dataframe(funnel_df)

    # Match Trend
    if trend:
        st.subheader("Match Trend")
        trend_df = pd.DataFrame(trend)
        st.line_chart(
            trend_df.set_index("week")["avg_match"]
        )