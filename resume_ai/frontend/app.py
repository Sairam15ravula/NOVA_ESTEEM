import streamlit as st
import requests


# -------------------------------
# CONFIG
# -------------------------------

API_URL = "http://localhost:8000/analyze"

st.set_page_config(
    page_title="Resume AI Analyzer",
    layout="wide"
)


# -------------------------------
# HEADER
# -------------------------------

st.title("📄 AI Resume Screening Tool")
st.write("Analyze resumes using AI-powered NLP")


# -------------------------------
# INPUT SECTION
# -------------------------------

st.header("📝 Input Details")

job_title = st.text_input(
    "Job Title (Optional)",
    placeholder="e.g. Data Scientist"
)

job_description = st.text_area(
    "Job Description (Required)",
    height=200,
    placeholder="Paste full job description here..."
)


st.subheader("Resume Input")

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = st.text_area(
    "Or Paste Resume Text",
    height=200,
    placeholder="Paste resume here..."
)


analyze_btn = st.button("🚀 Analyze Resume")


# -------------------------------
# ANALYSIS
# -------------------------------

if analyze_btn:

    if not job_description.strip() and not resume_file and not resume_text.strip():
        st.error("Please provide Job Description and Resume.")

    else:

        with st.spinner("🤖 AI is analyzing the profile..."):

            try:

                files = {}
                data = {
                    "job_description": job_description
                }

                # If PDF uploaded → send file
                if resume_file:
                    files["resume_file"] = resume_file

                # Else → send pasted text
                else:
                    data["resume_text"] = resume_text


                # Send request
                response = requests.post(
                    API_URL,
                    data=data,
                    files=files
                )


                if response.status_code != 200:
                    st.error("Backend Error: " + response.text)

                else:

                    data = response.json()

                    st.success("✅ Analysis Complete!")


                    # -------------------------------
                    # RESULTS
                    # -------------------------------

                    st.header("📊 Overall Match")

                    st.metric(
                        "Overall Score",
                        f"{data['overall_score']}%"
                    )


                    # Technical & Personality & Quality
                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Technical Score",
                        f"{data['technical_score']}%"
                    )

                    col2.metric(
                        "Personality Score",
                        f"{data['personality_score']}%"
                    )

                    col3.metric(
                        "Resume Quality",
                        f"{data['resume_quality']}/100"
                    )


                    # Domain
                    if "detected_domain" in data:
                        st.info(
                            f"Detected Domain: {data['detected_domain']}"
                        )


                    # -------------------------------
                    # SECTION SCORES
                    # -------------------------------

                    st.header("📌 Section Analysis")

                    section_scores = data["section_scores"]

                    for sec, score in section_scores.items():
                        st.progress(score / 100)
                        st.write(f"{sec.title()}: {score}%")


                    # -------------------------------
                    # PERSONALITY TRAITS
                    # -------------------------------

                    st.header("🧠 Personality Traits")

                    traits = data["traits"]

                    for t, v in traits.items():
                        st.progress(v / 100)
                        st.write(f"{t.title()}: {v}%")


                    # -------------------------------
                    # CONFIDENCE
                    # -------------------------------

                    st.subheader("Confidence Level")
                    st.write(data["confidence"])


                    # -------------------------------
                    # SKILLS
                    # -------------------------------

                    st.header("⚠️ Missing Skills")

                    if data["missing_skills"]:
                        for s in data["missing_skills"]:
                            st.write("❌", s)
                    else:
                        st.write("✅ No major skill gaps")


                    # -------------------------------
                    # SUGGESTIONS
                    # -------------------------------

                    st.header("💡 AI Suggestions")

                    for sug in data["suggestions"]:
                        st.write("👉", sug)


            except Exception as e:
                st.error(f"Connection Error: {e}")


