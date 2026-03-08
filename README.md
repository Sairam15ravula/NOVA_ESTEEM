NOVA ESTEEM - AI-Powered Resume Intelligence Platform
NOVA ESTEEM is a full-stack resume analysis and optimization system that uses natural language processing and machine learning to quantify how well a candidate's resume aligns with a given job description. The platform addresses the challenge of resume-to-JD matching by combining semantic similarity scoring via Sentence Transformers, keyword-based skill extraction, personality trait inference, and LLM-powered resume rewriting. It produces actionable gap analyses, rejection risk assessments, and tailored resumes optimized for Applicant Tracking Systems (ATS).

Problem Statement
Job seekers frequently submit resumes that are poorly aligned with the specific requirements of a job description. Recruiters and ATS platforms filter candidates primarily on keyword presence and contextual relevance, leading to qualified candidates being rejected due to formatting or phrasing mismatches rather than lack of capability.

Without an automated analysis tool, candidates have no objective way to measure how their resume compares to a JD. They cannot identify which critical skills are missing, which sections are underperforming, or how their soft skill language maps to employer expectations. Manual resume tailoring is time-consuming, subjective, and inconsistent.

This platform provides a data-driven, ML-powered alternative that scores resumes across multiple dimensions, identifies specific gaps, quantifies rejection risk, and generates optimized versions using large language models.

Project Overview
The system operates as a two-tier application with a FastAPI backend and a Next.js frontend.

End-to-end flow:

The user uploads a resume (PDF or text) and pastes a job description through the frontend interface.
The uploaded PDF is parsed client-side using pdf.js to extract raw text.
The backend validates the document type using Google Gemini (or a keyword-based fallback classifier) to reject non-resume documents such as research papers, cover letters, or academic notes.
The resume text is cleaned and normalized (lowercased, special characters removed, whitespace collapsed).
Skills are extracted from both the resume and the JD using regex matching against a curated multi-domain skill database covering Data/AI, Web Development, Cloud/DevOps, and General categories.
The job description domain is detected by counting skill category matches.
A hybrid technical score is computed: 60% from semantic cosine similarity (Sentence Transformers) and 40% from skill match ratio.
Personality traits (leadership, teamwork, learning, communication, problem solving) are scored by computing semantic similarity between resume text and predefined anchor sentences for each trait.
Section-level quality scores are calculated using a composite of content length, quantification presence, action verb usage, and JD keyword density.
A dynamic analysis module extracts JD priorities, identifies contextual gaps with severity levels, calculates rejection risk, and generates prioritized recommendations.
Natural language explanations are generated for each score.
Optionally, the user can trigger AI-powered tailoring, which sends the resume, JD, and NLP analysis results to an LLM (OpenAI GPT-4o-mini primary, Ollama Llama 3.2 fallback) to produce a restructured, keyword-saturated resume.
A post-processing step verifies keyword coverage and injects any keywords the LLM missed into a skills section.
The tailored resume can be previewed in the frontend and exported as a formatted PDF via ReportLab.
Authenticated users have their analysis results persisted to a SQLite database for historical tracking.
Key Features
Hybrid Technical Scoring Combines semantic similarity (via all-MiniLM-L6-v2 Sentence Transformer embeddings and cosine similarity) with keyword-level skill match ratios. The weighting is 60% semantic, 40% keyword match.

Personality Trait Analysis Evaluates five soft skill dimensions (leadership, teamwork, learning, communication, problem solving) by computing cosine similarity between the first 1000 characters of the resume and a set of 4 anchor sentences per trait. Returns per-trait and aggregate personality scores.

Multi-Domain Skill Extraction Maintains a curated database of 60+ skills across four domains (Data/AI, Web Development, Cloud/DevOps, General). Extracts skills from both resume and JD using word-boundary regex matching.

Domain Detection Automatically classifies the target role domain by counting skill category matches in the job description.

Section-Level Quality Scoring Parses the resume into sections (summary, skills, projects, experience) and scores each based on word count, presence of quantified metrics, action verb usage, and JD keyword density.

Dynamic Gap Analysis Identifies contextual gaps between resume and JD, categorized as skill gaps (critical or medium severity), quantification gaps, and content length gaps. Each gap includes context extracted from the JD and a specific suggestion.

JD Priority Extraction Parses the job description to identify critical requirements (keywords mentioned 2+ times), nice-to-have skills (mentioned once), and explicit requirement/preference sentences.

Rejection Risk Assessment Computes a risk level (LOW, MEDIUM, HIGH, CRITICAL) based on the count of critical gaps, high-priority gaps, and low-scoring sections. Returns detailed risk factors with severity, affected items, and impact descriptions.

Personalized Recommendations Generates up to 10 prioritized, actionable recommendations sorted by severity, each with an action, reason, item, and estimated impact level.

Natural Language Score Explanations Produces human-readable explanations for each score (overall, technical, personality, and per-section) based on threshold-driven templates.

LLM-Powered Resume Tailoring Sends the resume, JD, full NLP analysis results (gaps, rejection risks, JD priorities), and detected section headers to an LLM with a structured JSON output prompt. Returns a fully structured resume with name, contact info, and sections with entries and bullet points.

Keyword Saturation Post-Processing After LLM tailoring, verifies that all missing keywords appear in the output. Injects any still-missing keywords into a skills section and enhances the summary with JD-aligned phrases.

Structured Fallback (No LLM) When no LLM is available, parses the resume into structured sections using regex-based header detection, date pattern matching, and bullet extraction. Enriches the output with NLP analysis insights.

Document Classification Uses Google Gemini 1.5 Flash to classify uploaded documents into resume, research paper, cover letter, or other. Includes a multi-signal keyword-based fallback classifier with separate indicator sets for research papers, resumes (strong and weak indicators), cover letters, and academic notes.

PDF Generation Generates formatted PDF resumes using ReportLab with custom styles for name, contact info, section titles, organization/date rows (table layout for right-aligned dates), entry titles, and bullet points.

Authentication and History JWT-based authentication (python-jose, bcrypt via passlib) with user registration, login, and token-based session management. Analysis results are stored as JSON in a SQLite database via SQLModel ORM. Users can retrieve historical analyses with scores and timestamps.

System Architecture
Data Flow:
[PDF Upload] --> [Client-Side PDF Parsing (pdf.js)]
     |
     v
[FastAPI Backend]
     |
     +--> [Document Classifier (Gemini / Keyword Fallback)]
     |         |
     |         +--> Reject (non-resume) --> Error Response
     |         +--> Accept (resume) --> Continue
     |
     +--> [Text Preprocessing (clean_text)]
     |
     +--> [Skill Extraction (regex against SKILLS_DB)]
     |
     +--> [Domain Detection (category match counting)]
     |
     +--> [Technical Score Calculation]
     |         +--> Semantic Similarity (Sentence Transformer + Cosine)
     |         +--> Skill Match Ratio
     |         +--> Weighted Combination (60/40)
     |
     +--> [Personality Analysis]
     |         +--> Anchor Sentence Similarity per Trait
     |         +--> Aggregate Personality Score
     |
     +--> [Section Parsing and Quality Scoring]
     |         +--> Length + Metrics + Action Verbs + Keywords
     |
     +--> [Dynamic Analysis Module]
     |         +--> JD Priority Extraction
     |         +--> Contextual Gap Identification
     |         +--> Rejection Risk Calculation
     |         +--> Personalized Recommendation Generation
     |         +--> Score Explanation Generation
     |
     +--> [Analysis Response --> Frontend Dashboard]
     |
     +--> [Tailor Endpoint (optional)]
               +--> LLM Rewriting (GPT-4o-mini / Ollama Llama 3.2)
               +--> Keyword Saturation Post-Processing
               +--> Structured JSON Output
               +--> PDF Generation (ReportLab) --> Download
Backend Components:


main.py
 - FastAPI application with route definitions, CORS middleware, authentication dependency, and endpoint handlers for analyze, tailor, download-pdf, history, login, and register.

models.py
 - Pydantic schemas for all request/response types including AnalyzeRequest, AnalyzeResponse (with gaps, rejection risk, recommendations), TailorRequest, TailorResponse (with structured sections and entries), and auth models.

database.py
 - SQLModel ORM definitions for User and AnalysisHistory tables with SQLite backend.

auth.py
 - JWT token creation/decoding (HS256) and bcrypt password hashing/verification.

services/analyzer.py
 - Core ML analysis engine containing the Sentence Transformer model loading, skill extraction, domain detection, personality analysis, technical score calculation, section parsing, and the main 

analyze_resume
 orchestration function.

services/analyzer_dynamic.py
 - Dynamic analysis module for JD priority extraction, contextual gap identification, rejection risk calculation, recommendation generation, and score explanation generation.

services/document_classifier.py
 - Gemini-based document classification with multi-signal keyword fallback.

services/tailor.py
 - LLM-powered resume tailoring with OpenAI/Ollama integration, keyword saturation post-processing, and regex-based structured fallback.

services/llm_rewriter.py
 - Gemini-based resume rewriting service (standalone, not used in main pipeline but available as a module).

services/pdf_generator.py
 - ReportLab-based PDF generation with custom paragraph styles and table layouts.
Frontend Components:


page.tsx
 - Main application page with resume upload, JD input, analysis trigger, and results display.

login/page.tsx
 - Authentication page with login/register toggle.

dashboard/page.tsx
 - Historical analysis dashboard with trend charts.

services/api.ts
 - Axios HTTP client with JWT interceptor for all API calls.

components/UploadZone.tsx
 - PDF/text file upload with client-side PDF parsing via pdf.js.

components/ScoreGauge.tsx
 - Circular gauge visualization using Recharts PieChart.

components/SkillRadar.tsx
 - Radar chart for personality trait visualization using Recharts RadarChart.

components/PersonalityBars.tsx
 - Horizontal progress bars for personality trait scores with color-coded severity.

components/GapAnalysis.tsx
 - Gap cards grouped and styled by severity (critical, high, medium, low).

components/RejectionRiskCard.tsx
 - Risk assessment card with level, summary, and factor breakdown.

components/RecommendationsList.tsx
 - Prioritized action items with severity badges and impact labels.

components/TailorView.tsx
 - Tailored resume preview with copy-to-clipboard and PDF download functionality.
Machine Learning Methodology
Sentence Embedding Model

The system uses the all-MiniLM-L6-v2 model from the Sentence Transformers library. This is a lightweight, 384-dimensional embedding model trained on a large corpus of sentence pairs. It is loaded once at application startup and used for all similarity computations.

Technical Score Computation

The technical score is a weighted combination of two signals:

Semantic Similarity (60% weight) - The full resume text and JD text are each encoded into a 384-dimensional vector using the Sentence Transformer. Cosine similarity between these vectors produces a score from 0-100, capturing how semantically aligned the resume content is with the JD regardless of exact keyword overlap.

Skill Match Ratio (40% weight) - Skills are extracted from both documents using word-boundary regex matching against a curated database of 60+ skills organized into 4 domains. The match ratio is computed as |intersection(resume_skills, jd_skills)| / |jd_skills| * 100.

The final technical score is 0.6 * semantic_score + 0.4 * skill_match_ratio.

Personality Trait Scoring

Five personality traits are evaluated: leadership, teamwork, learning, communication, and problem solving. For each trait, 4 anchor sentences are defined that exemplify the trait (e.g., "I take initiative and lead teams" for leadership). The first 1000 characters of the resume are cleaned and compared against each anchor sentence using cosine similarity of Sentence Transformer embeddings. The trait score is the mean similarity across all 4 anchors. The aggregate personality score is the mean across all 5 traits.

Additionally, JD-specific trait adaptations are applied: if the JD mentions "research", "startup", or "client", extra anchor sentences are injected.

Overall Score

The overall score is computed as 0.7 * technical_score + 0.3 * personality_score.

Section Quality Scoring

Each resume section (summary, skills, projects, experience) is scored using a composite metric:

Base score from word count (20 words = 30 points, 50 words = 80 points, 150+ words = 100 points)
+10 points for presence of quantified metrics (percentages, dollar amounts, year counts)
+2 points per action verb detected (led, managed, developed, etc.), capped at +10
+3 points per JD keyword found in the section, capped at +15
Gap Identification

Gaps are categorized by type and severity:

Critical skill gaps: Skills mentioned 2+ times in the JD but absent from the resume
Medium skill gaps: Skills mentioned once in the JD but absent from the resume
Quantification gaps (high severity): Resume contains no measurable metrics
Content gaps (medium severity): Resume is under 200 words
Rejection Risk Calculation

Risk level is determined by gap counts:

CRITICAL: 3+ critical gaps
HIGH: Any critical gaps OR 2+ high gaps
MEDIUM: Any high gaps OR any low-scoring sections (below 50%)
LOW: No significant gaps
LLM Integration for Tailoring

The tailoring pipeline uses a dual-LLM strategy:

Primary: OpenAI GPT-4o-mini via the OpenAI Python SDK
Fallback: Ollama (Llama 3.2) via local HTTP API
The LLM receives a structured prompt containing the original resume, JD, NLP analysis results (missing keywords, gaps, rejection risks, JD priorities), and detected section headers. It is instructed to return a JSON object with preserved structure and enhanced content. Temperature is set to 0.3 for consistency.

Post-LLM processing verifies keyword coverage by serializing the output to text and checking for each missing keyword. Any keywords not found are injected into the skills section. The summary section is enhanced with JD-aligned phrases extracted via regex.

When no LLM is available, a regex-based fallback parser segments the resume using uppercase header detection, date pattern matching, and bullet point extraction.

Dataset
This system does not train on a static dataset. It operates as an inference-time analysis tool where the input data is provided by the user at runtime:

Resume: Uploaded as PDF (parsed via pdf.js) or plain text. Typical length is 200-600 words.
Job Description: Pasted as plain text by the user.
Predefined knowledge bases used:

Skill Database (SKILLS_DB): A curated dictionary of 60+ skills organized into 4 domains (Data/AI: 18 skills, Web Development: 19 skills, Cloud/DevOps: 13 skills, General: 13 skills). Used for skill extraction and domain detection.
Personality Trait Templates (TRAITS): 5 traits with 4 anchor sentences each (20 total anchor sentences). Used to evaluate soft skill signals in resume text.
Document Classification Indicators: Separate keyword lists for research papers (15 indicators), strong resume indicators (9), weak resume indicators (4), structural patterns (5 regex patterns), cover letter indicators (8), and academic notes indicators (10).
No model fine-tuning or training occurs within this application. The Sentence Transformer model (all-MiniLM-L6-v2) is used as a pretrained feature extractor.

Results and Observations
Scoring Behavior

The semantic similarity component (Sentence Transformers) typically produces scores in the 30-70% range for unrelated resume-JD pairs and 60-85% for well-matched pairs. This provides meaningful discrimination.
The skill match ratio component is binary per skill (present or absent) and is sensitive to the completeness of the SKILLS_DB. Skills not in the database are not detected.
Personality scores are generally in the 40-70% range. Resumes with explicit leadership and teamwork language score higher. The anchor sentence approach provides reasonable soft skill signal but is limited to lexical similarity rather than deep semantic understanding.
Section quality scores effectively penalize thin sections and reward quantified, keyword-rich, action-verb-heavy content.
Gap Analysis

Critical gaps are the most actionable signal. A resume missing skills mentioned 2+ times in the JD has a strong correlation with ATS rejection.
The quantification gap detection (absence of numbers/percentages) is a simple but effective heuristic for identifying resumes that lack impact metrics.
Tailoring

LLM-generated tailored resumes consistently include more JD-aligned language and integrated missing keywords.
The keyword saturation post-processing step is necessary because LLMs do not reliably include every specified keyword even when explicitly instructed.
The regex-based fallback produces structurally reasonable output but lacks the semantic enhancement of the LLM path.
Limitations

The skill database is manually curated and does not cover all possible skills or emerging technologies.
Personality trait analysis uses surface-level semantic similarity rather than deep behavioral analysis.
The system does not perform OCR, so scanned image PDFs cannot be processed.
Section parsing uses heuristics (uppercase headers, date patterns) that may fail on non-standard resume formats.
The LLM tailoring depends on external API availability and may produce inconsistent results across runs.
Repository Structure
NOVA_ESTEEM/
|
├── backend/                           # FastAPI Python backend
│   ├── main.py                        # API entry point, route definitions, CORS, auth
│   ├── models.py                      # Pydantic request/response schemas
│   ├── database.py                    # SQLModel ORM (User, AnalysisHistory, SQLite)
│   ├── auth.py                        # JWT authentication, bcrypt password hashing
│   ├── requirements.txt               # Python dependencies
│   └── services/
│       ├── __init__.py
│       ├── analyzer.py                # Core ML engine (Sentence Transformers, scoring)
│       ├── analyzer_dynamic.py        # Gap analysis, risk assessment, recommendations
│       ├── document_classifier.py     # Gemini + fallback document classification
│       ├── llm_rewriter.py            # Gemini-based resume rewriting module
│       ├── tailor.py                  # LLM tailoring pipeline with post-processing
│       └── pdf_generator.py           # ReportLab PDF generation
│
├── frontend/                          # Next.js 16 + React 19 frontend
│   ├── package.json                   # Node.js dependencies
│   ├── next.config.ts                 # Next.js configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   └── app/
│       ├── page.tsx                   # Main analysis and tailoring page
│       ├── layout.tsx                 # Root layout
│       ├── globals.css                # Global styles
│       ├── login/page.tsx             # Authentication page
│       ├── dashboard/page.tsx         # Analysis history dashboard
│       ├── services/api.ts            # Axios API client with JWT interceptor
│       └── components/
│           ├── UploadZone.tsx         # File upload with PDF parsing
│           ├── ScoreGauge.tsx         # Circular score visualization
│           ├── SkillRadar.tsx         # Radar chart for traits
│           ├── PersonalityBars.tsx    # Progress bars for soft skills
│           ├── GapAnalysis.tsx        # Gap cards by severity
│           ├── RejectionRiskCard.tsx  # Risk assessment display
│           ├── RecommendationsList.tsx # Prioritized action items
│           └── TailorView.tsx         # Resume preview and PDF download
│
├── .env.example                       # Environment variable template
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Root Python dependencies
└── README.md
Installation
Prerequisites
Python 3.10 or higher
Node.js 18 or higher with npm
A Google Gemini API key (free tier available at https://aistudio.google.com/app/apikey)
(Optional) An OpenAI API key for GPT-4o-mini tailoring
(Optional) Ollama installed locally for offline LLM fallback
Steps
Clone the repository:
bash
git clone https://github.com/Sairam15ravula/NOVA_ESTEEM.git
cd NOVA_ESTEEM
Create and configure environment variables:
bash
cp .env.example .env
Edit 

.env
 with your API keys:

GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_key          # Optional
OLLAMA_URL=http://localhost:11434/v1     # Optional
JWT_SECRET=your_random_secret_key
Set up the Python backend:
bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r backend/requirements.txt
Set up the frontend:
bash
cd frontend
npm install
Usage
Running the Backend
bash
python -m backend.main
The API server starts at http://localhost:8000. On first startup, the Sentence Transformer model (all-MiniLM-L6-v2) is downloaded and loaded into memory. The SQLite database and tables are created automatically.

Running the Frontend
bash
cd frontend
npm run dev
The frontend is available at http://localhost:3000.

API Endpoints
Method	Endpoint	Description
GET	/	Health check
POST	/auth/register	Register a new user account
POST	/auth/login	Authenticate and receive JWT token
POST	/analyze	Analyze a resume against a job description
POST	/tailor	Generate an ATS-optimized tailored resume
POST	/download-pdf	Generate and download a formatted PDF
GET	/history	Retrieve authenticated user's analysis history
Workflow
Open http://localhost:3000 in a browser.
Upload a resume (PDF or text file) and paste a job description.
Click "Analyze" to receive scores, gap analysis, rejection risk, and recommendations.
Click "Tailor Resume" to generate an ATS-optimized version.
Preview the tailored resume and download it as a PDF.
Optionally register/login to save analysis history.
Future Improvements
Expanded Skill Database: Integrate with external skill taxonomies (e.g., ESCO, O*NET) for broader and more current skill coverage.
Fine-Tuned Embedding Model: Fine-tune the Sentence Transformer on resume-JD pairs to improve domain-specific similarity scoring.
OCR Support: Integrate Tesseract or cloud OCR APIs to handle scanned image-based PDFs.
Multi-Language Support: Extend analysis to resumes and JDs in languages other than English.
Batch Processing: Support analyzing multiple resumes against a single JD for recruiter-side usage.
Real-Time ATS Simulation: Simulate specific ATS platforms (Workday, Greenhouse, Lever) to provide platform-specific optimization guidance.
Feedback Loop: Collect user feedback on analysis accuracy to iteratively improve scoring heuristics and thresholds.
Production Deployment: Containerize with Docker, add CI/CD pipelines, migrate to PostgreSQL, and deploy behind a load balancer.
Monitoring and Observability: Add structured logging, request tracing, and model performance monitoring.
Author
NOVA ESTEEM Team

GitHub: https://github.com/Sairam15ravula/NOVA_ESTEEM
