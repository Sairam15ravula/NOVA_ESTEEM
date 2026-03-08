NOVA ESTEEM (REZUAI)

NOVA ESTEEM is a full-stack AI-powered resume analysis and optimization platform designed to help job seekers maximize their chances of landing interviews.

The system analyzes how well a resume aligns with a specific job description using NLP-based semantic analysis, machine learning scoring models, and LLM-powered rewriting. It then identifies gaps, evaluates rejection risk, and automatically tailors the resume for stronger alignment with employer expectations.

Don't just submit your resume. Submit the right resume.

Key Features
Intelligent Resume Analysis

Hybrid Scoring Engine

Combines multiple analytical signals to evaluate resume alignment:

Semantic Similarity — Sentence Transformers with cosine similarity measure contextual alignment between resume and job description.

Skill Match Ratio — Extracted technical skills from both documents are compared to quantify skill overlap.

Technical Score

Measures how well the resume’s hard skills match the requirements of the job description.

Personality Score

Evaluates soft skill indicators such as:

leadership

teamwork

communication

problem solving

using NLP-based trait matching.

Domain Detection

Automatically identifies the professional domain of the job description (Data/AI, Web Development, DevOps, etc.).

Dynamic Gap Analysis

The system identifies weaknesses in a resume with contextual severity levels.

Contextual Gap Detection

Detects issues such as:

missing skills

lack of quantifiable achievements

weak content in critical sections

Each gap is assigned a severity rating:

Critical

High

Medium

Low

Job Description Priority Extraction

Analyzes job descriptions to determine the most important skills and requirements for the role.

Score Explanations

Natural language explanations clarify why a resume received a specific score, improving transparency and user understanding.

Rejection Risk Assessment

The platform estimates the likelihood that a resume may be rejected by recruiters or ATS systems.

Risk Level Calculation

Classifies rejection probability into:

Low

Medium

High

Critical

Risk Factor Breakdown

Provides detailed explanations for risk contributors including severity, impact, and reasoning.

Dynamic Risk Summary

A context-aware summary explaining the largest weaknesses affecting the resume.

Personalized Recommendations

The system generates prioritized, actionable guidance to improve resume performance.

Prioritized Action Items

Suggestions are ranked by expected impact and severity.

Actionable Improvements

Examples include:

adding missing skills to the skills section

quantifying experience bullet points

restructuring sections for better ATS compatibility

AI-Powered Resume Tailoring

LLM-Based Resume Rewriting

Uses large language models to intelligently rewrite resume content based on the job description.

Keyword Saturation

Post-processing ensures important missing keywords are naturally integrated to improve ATS performance.

Structured Output

The tailored resume is generated as a structured representation containing sections, entries, and bullet points.

High-Fidelity PDF Export

Users can download a professionally formatted resume generated using programmatic PDF rendering.

User Authentication and History

Secure Authentication

User authentication is implemented using JWT-based sessions with encrypted password storage.

Analysis History Dashboard

Users can track past resume analyses and visualize performance trends.

Persistent Storage

Analysis data is stored using an ORM-backed relational database.

Smart Document Classification

Before analysis begins, uploaded documents are validated to ensure they are actual resumes.

AI-Powered Classification

A language model classifies documents and filters out:

research papers

cover letters

unrelated documents

Fallback Validation

When LLM validation is unavailable, a heuristic keyword-based classifier is used.

System Architecture
NOVA_ESTEEM/
│
├── backend/                 # FastAPI backend
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   └── services/
│       ├── analyzer.py
│       ├── analyzer_dynamic.py
│       ├── document_classifier.py
│       ├── llm_rewriter.py
│       ├── tailor.py
│       └── pdf_generator.py
│
├── frontend/                # Next.js frontend
│   └── app/
│       ├── page.tsx
│       ├── login/page.tsx
│       ├── dashboard/page.tsx
│       ├── services/api.ts
│       └── components/
│           ├── UploadZone.tsx
│           ├── ScoreGauge.tsx
│           ├── SkillRadar.tsx
│           ├── PersonalityBars.tsx
│           ├── GapAnalysis.tsx
│           ├── RejectionRiskCard.tsx
│           ├── RecommendationsList.tsx
│           └── TailorView.tsx
│
├── requirements.txt
└── README.md
Technology Stack
Layer	Technology
Frontend	Next.js, React, TypeScript, Tailwind CSS
Visualization	Recharts
Backend	FastAPI, Python
NLP / ML	Sentence Transformers, scikit-learn
LLM Integration	Gemini, GPT-4o, Llama
Database	SQLite with SQLModel ORM
Authentication	JWT
PDF Generation	ReportLab
HTTP Client	Axios
Analysis Pipeline

1. Document Validation

Uploaded files are classified to ensure they are valid resumes.

2. Text Processing

Resume content is cleaned, normalized, and segmented into sections.

3. Semantic Similarity

Both resume and job description are encoded using a transformer model and compared using cosine similarity.

4. Skill Extraction

Skills are extracted from both documents and compared using a curated skill database.

5. Personality Trait Analysis

Language patterns are matched against trait anchor sentences to evaluate soft skills.

6. Gap Detection

The system identifies weaknesses and assigns severity levels.

7. Rejection Risk Calculation

Risk scores are generated based on detected gaps and section performance.

8. Recommendation Engine

Actionable improvement suggestions are produced.

9. AI Resume Tailoring

The resume is rewritten to better match the job description while maintaining natural language.

10. PDF Generation

A final tailored resume can be exported as a formatted PDF.

API Overview
Method	Endpoint	Description
GET	/	Health check
POST	/auth/register	Register a new user
POST	/auth/login	Authenticate user
POST	/analyze	Analyze resume against job description
POST	/tailor	Tailor resume for a specific role
POST	/download-pdf	Download tailored resume
GET	/history	Retrieve analysis history
Contributing

Contributions are welcome.

Typical workflow:

Fork the repository

Create a feature branch

Commit your changes

Push the branch

Open a Pull Request

License

This project is licensed under the MIT License.

Team

Built by the NOVA ESTEEM team.
