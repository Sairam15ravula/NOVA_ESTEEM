# NOVA ESTEEM
NOVA ESTEEM is an AI-powered resume intelligence platform that analyzes how well a candidate's resume aligns with a job description using natural language processing and machine learning.

The platform combines semantic similarity scoring, skill extraction, personality trait analysis, and LLM-powered rewriting to provide actionable feedback and automatically generate optimized resumes.

---

## Key Highlights

• Semantic resume-job matching using Sentence Transformers  
• Hybrid scoring system combining embeddings and keyword analysis  
• Personality trait inference from resume language  
• Automated gap detection and rejection risk assessment  
• LLM-powered resume rewriting and ATS optimization

---

## Problem Statement

Job seekers often submit resumes that are poorly aligned with job descriptions, leading to automatic rejection by Applicant Tracking Systems (ATS).

Without automated analysis tools, candidates lack visibility into:

- which required skills are missing
- how well their experience matches the role
- how their resume language aligns with employer expectations

NOVA ESTEEM provides a data-driven system that quantifies resume alignment and generates actionable recommendations.

---

## System Architecture


Resume Upload
↓
PDF Parsing
↓
Text Preprocessing
↓
Skill Extraction
↓
Semantic Similarity Analysis
↓
Personality Trait Analysis
↓
Gap Detection
↓
Rejection Risk Assessment
↓
LLM Resume Tailoring


---

## Machine Learning Methodology

### Sentence Embeddings

Model: `all-MiniLM-L6-v2`

Used to compute semantic similarity between resume and job description.

### Technical Score


Technical Score =
0.6 × Semantic Similarity

0.4 × Skill Match Ratio


### Personality Trait Analysis

Traits evaluated:

- leadership
- teamwork
- communication
- learning ability
- problem solving

Scores computed using cosine similarity against anchor sentences.

---

## Core Features

• Resume-JD semantic similarity scoring  
• Skill extraction across multiple domains  
• Section-level resume quality evaluation  
• Gap analysis with severity levels  
• Rejection risk classification  
• AI-generated resume tailoring  
• PDF export for optimized resumes

---

## Tech Stack

Backend  
- FastAPI  
- Sentence Transformers  
- SQLite  
- JWT Authentication  

Frontend  
- Next.js  
- React  
- Recharts  

AI  
- Sentence Transformers  
- GPT-4o-mini  
- Ollama (fallback)

---

## Repository Structure


NOVA_ESTEEM
│
├── backend
│ ├── main.py
│ ├── models.py
│ ├── database.py
│ └── services
│
├── frontend
│ ├── app
│ ├── components
│ └── services
│
└── README.md


---

## Future Improvements

• Fine-tuned embedding models for resume-JD similarity  
• Expanded skill taxonomy using external datasets  
• Multi-language resume analysis  
• ATS platform simulation

---

## Authors

NOVA ESTEEM Team
