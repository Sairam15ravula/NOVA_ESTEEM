import streamlit as st
import requests

st.set_page_config(page_title="Resume AI Screener", layout="wide")

st.title("📄 Resume AI Screening Tool")

# Input Section
st.subheader("Input")
resume_text = st.text_area("Paste Resume", height=200)
job_description = st.text_area("Paste Job Description", height=200)

analyze_btn = st.button("Analyze")

if analyze_btn:
    if not resume_text or not job_description:
        st.error("Please provide both Resume and Job Description")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={
                        "resume_text": resume_text,
                        "job_description": job_description
                    },
                    timeout=30
                )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.subheader("📊 Scores")
                    st.metric("Overall Score", f"{data['overall_score']}%")
                    st.metric("Technical Score", f"{data['technical_score']}%")
                    st.metric("Personality Score", f"{data['personality_score']}%")

                    st.subheader("🧠 Traits")
                    for trait, score in data["traits"].items():
                        st.progress(score / 100, text=f"{trait.capitalize()} — {score}%")

                    st.subheader("⚠️ Missing Skills")
                    for skill in data["missing_skills"]:
                        st.write(f"- {skill}")

            except Exception:
                st.error("Failed to connect to backend")
