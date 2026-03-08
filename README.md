Overview
NOVA ESTEEM (REZUAI) is a full-stack AI-powered resume analysis and optimization platform that helps job seekers maximize their chances of landing interviews. It combines NLP-based semantic analysis, machine learning models, and LLM-powered rewriting to provide deep insights into how well a resume matches a specific job description — and then automatically tailors it for maximum impact.

"Don't just submit your resume. Submit the right resume."

Key Features
Intelligent Resume Analysis
Hybrid Scoring Engine — Combines semantic similarity (Sentence Transformers + Cosine Similarity) with skill-match ratios for a nuanced overall score
Technical Score — Measures hard skill alignment between resume and job description
Personality Score — Evaluates soft skill signals (leadership, teamwork, communication, etc.) using NLP trait matching
Domain Detection — Automatically identifies the target role domain (Data/AI, Web Dev, DevOps, etc.)
Dynamic Gap Analysis
Contextual Gap Detection — Identifies missing skills, quantification gaps, and content weaknesses with severity ratings (Critical to Low)
JD Priority Extraction — Parses job descriptions to determine what the employer values most
Score Explanations — Natural language explanations for each score, so you know why you scored what you did
Rejection Risk Assessment
Risk Level Calculation — Evaluates your rejection risk (Low / Medium / High / Critical) based on gaps and section scores
Risk Factor Breakdown — Detailed factors with severity, impact, and actionable details
Dynamic Risk Summary — Context-aware summaries explaining your biggest vulnerabilities
Personalized Recommendations
Prioritized Action Items — Ranked recommendations with severity, reasoning, and estimated impact
Actionable Suggestions — Specific steps like "Add Python to your skills section" rather than generic advice
AI-Powered Resume Tailoring
LLM Resume Rewriting — Uses GPT-4o / Ollama (Llama) with OpenAI-fallback to intelligently rewrite your resume
Keyword Saturation — Post-processing ensures all critical missing keywords are naturally integrated
Structured Output — Generates a fully structured JSON representation with sections, entries, and bullet points
High-Fidelity PDF Export — Downloads a professionally formatted PDF resume via ReportLab
User Authentication & History
JWT-Based Auth — Secure registration and login with bcrypt password hashing
Analysis History Dashboard — Track your scores over time with visual trend charts
Persistent Storage — SQLite database via SQLModel ORM
Smart Document Classification
AI-Powered Validation — Uses Google Gemini to classify uploaded documents and reject non-resumes (research papers, cover letters, etc.)
Fallback Classification — Keyword-based heuristic when LLM is unavailable
Architecture
NOVA_ESTEEM/
├── backend/                        # FastAPI Python Backend
│   ├── main.py                     # API entry point & route definitions
│   ├── models.py                   # Pydantic request/response schemas
│   ├── database.py                 # SQLModel ORM (User, AnalysisHistory)
│   ├── auth.py                     # JWT authentication & password hashing
│   └── services/
│       ├── analyzer.py             # Core ML analysis engine (Sentence Transformers)
│       ├── analyzer_dynamic.py     # Dynamic gap analysis & risk assessment
│       ├── document_classifier.py  # Gemini-powered document classification
│       ├── llm_rewriter.py         # Gemini-powered resume rewriting
│       ├── tailor.py               # LLM resume tailoring + keyword saturation
│       └── pdf_generator.py        # ReportLab PDF generation
│
├── frontend/                       # Next.js 16 + React 19 Frontend
│   └── app/
│       ├── page.tsx                # Main analysis & tailoring interface
│       ├── login/page.tsx          # Authentication page
│       ├── dashboard/page.tsx      # Analysis history & trends
│       ├── services/api.ts         # Axios API client with auth interceptors
│       └── components/
│           ├── UploadZone.tsx          # PDF/text file upload with client-side parsing
│           ├── ScoreGauge.tsx          # Animated circular score gauges (Recharts)
│           ├── SkillRadar.tsx          # Radar chart for personality profile
│           ├── PersonalityBars.tsx     # Soft skill progress bars
│           ├── GapAnalysis.tsx         # Gap cards grouped by severity
│           ├── RejectionRiskCard.tsx   # Risk assessment display
│           ├── RecommendationsList.tsx # Prioritized action items
│           └── TailorView.tsx         # Tailored resume preview + PDF download
│
├── .env.example                    # Environment variable template
├── requirements.txt                # Root Python dependencies
└── README.md
Tech Stack
Layer	Technology
Frontend	Next.js 16, React 19, TypeScript, Tailwind CSS 4
Charts & Visualizations	Recharts (Pie, Radar, Area charts)
PDF Parsing	pdf.js (client-side PDF text extraction)
Backend	FastAPI, Uvicorn, Python 3.10+
NLP / ML	Sentence Transformers (all-MiniLM-L6-v2), scikit-learn (Cosine Similarity)
LLM Integration	Google Gemini 1.5 Flash, OpenAI GPT-4o, Ollama (local Llama)
PDF Generation	ReportLab
Database	SQLite + SQLModel ORM
Authentication	JWT (python-jose) + bcrypt (passlib)
HTTP Client	Axios (with auth interceptors)
Getting Started
Prerequisites
Python 3.10+
Node.js 18+ & npm
Google Gemini API Key (free from Google AI Studio)
(Optional) OpenAI API Key for GPT-4o tailoring
(Optional) Ollama running locally for offline LLM support
1. Clone the Repository
bash
git clone https://github.com/Sairam15ravula/NOVA_ESTEEM.git
cd NOVA_ESTEEM
2. Set Up Environment Variables
bash
cp .env.example .env
Edit 

.env
 and add your API keys:

env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_key_here     # Optional
OLLAMA_URL=http://localhost:11434/v1     # Optional, for local LLM
JWT_SECRET=your_random_secret_key
3. Install & Run the Backend
bash
# Create a virtual environment
python -m venv .venv
# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
# Install dependencies
pip install -r backend/requirements.txt
# Run the server
python -m backend.main
The API will be available at http://localhost:8000

4. Install & Run the Frontend
bash
cd frontend
npm install
npm run dev
The app will be available at http://localhost:3000

API Endpoints
Method	Endpoint	Description
GET	/	Health check
POST	/auth/register	Register a new user
POST	/auth/login	Login & receive JWT token
POST	/analyze	Analyze resume against job description
POST	/tailor	AI-tailor resume for a specific JD
POST	/download-pdf	Generate & download tailored resume as PDF
GET	/history	Get logged-in user's analysis history
How It Works
Valid Resume
Not a Resume
Upload Resume + JD
Document Classification
NLP Analysis Engine
Error Message
Semantic SimilaritySentence Transformers
Skill Extraction& Domain Detection
Personality TraitAnalysis
Score CalculationTechnical + Personality + Overall
Dynamic Gap Analysis
Rejection Risk Assessment
Personalized Recommendations
Interactive Dashboard
AI TailoringGPT-4o / Gemini / Llama
PDF Download
Analysis Pipeline
Document Classification — Validates the uploaded document is actually a resume using Gemini AI
Text Cleaning & Preprocessing — Normalizes text, extracts sections (Experience, Education, Skills, etc.)
Semantic Similarity — Encodes resume and JD using all-MiniLM-L6-v2 Sentence Transformer model, computes cosine similarity (weighted 60% of technical score)
Skill Matching — Extracts skills from both documents using a curated multi-domain skill database, computes match ratio (weighted 40% of technical score)
Personality Analysis — Matches resume language against trait-specific anchor sentences using semantic similarity
Dynamic Analysis — Identifies contextual gaps, calculates rejection risk, and generates prioritized recommendations
AI Tailoring — Rewrites the resume using LLM with keyword saturation post-processing to guarantee ATS optimization
Contributing
Contributions are welcome! Here's how to get started:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request
License
This project is licensed under the MIT License — see the 

LICENSE
 file for details.

Team
Built by the NOVA ESTEEM team.
