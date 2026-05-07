# NOVA ESTEEM — NLP Resume-to-Job Similarity Platform

> A semantic intelligence engine that analyses how well a resume matches a job description — and tells you exactly what's missing.

---

## The problem

Generic resume advice ("add more keywords") doesn't work because it ignores context. A resume for a "Data Scientist at a fintech startup" should read very differently from one for a "Data Scientist at a research lab" — even if the job titles are identical. NOVA ESTEEM treats this as an NLP similarity problem, not a keyword matching problem.

---

## How it works

### Stage 1 — Semantic embedding
Both the resume and the job description are encoded using **Sentence Transformers** (`all-MiniLM-L6-v2`). This captures contextual meaning, not just surface keywords — so "built anomaly detection systems" correctly aligns with "experience in unsupervised ML" even though no words overlap.

### Stage 2 — Hybrid scoring
A pure cosine similarity score can be gamed by padding a resume with buzzwords. NOVA ESTEEM uses a **hybrid scoring system**:

| Component | Method | Weight |
|---|---|---|
| Contextual similarity | Sentence Transformer cosine similarity | 60% |
| Keyword coverage | TF-IDF keyword extraction + overlap | 25% |
| Skill gap penalty | Named entity matching on technical terms | 15% |

### Stage 3 — Skill gap report
The output isn't just a score — it's a **ranked skill-gap report**:
- Skills present in the JD but absent from the resume (critical gaps)
- Skills partially matched (contextually similar but not explicit)
- Skills present in the resume that are irrelevant to this JD

---

## Architecture

```
Resume (PDF / text)     Job Description (text / URL)
        ↓                          ↓
   Text Extraction            Text Cleaning
        ↓                          ↓
        └──────── Sentence Transformer Encoder ────────┘
                            ↓
                  Cosine Similarity Score
                            ↓
                  TF-IDF Keyword Extraction
                            ↓
                  Skill Gap Analysis (NER)
                            ↓
                  Hybrid Score Calculation
                            ↓
              Ranked Skill-Gap Report (JSON + UI)
```

---

## Tech stack

| Component | Technology |
|---|---|
| Semantic embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Keyword extraction | TF-IDF (Scikit-learn) |
| NER for skill matching | spaCy / regex patterns |
| PDF parsing | PyMuPDF |
| Backend API | FastAPI |
| Frontend | React |

---

## Getting started

```bash
git clone https://github.com/Bhuvan1205/nova-esteem.git
cd nova-esteem

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the API
uvicorn main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

---

## Example output

```json
{
  "overall_match_score": 0.73,
  "contextual_similarity": 0.81,
  "keyword_coverage": 0.58,
  "critical_gaps": [
    "PyTorch",
    "model deployment",
    "A/B testing"
  ],
  "partial_matches": [
    "anomaly detection ↔ unsupervised learning",
    "feature engineering ↔ data preprocessing"
  ],
  "irrelevant_resume_sections": [
    "C programming"
  ]
}
```

---

## Why this matters

This project is self-referential in the best way: I built a resume analysis tool while actively job searching, which means I could iterate on it using real job descriptions I was applying to. Every design decision was validated against actual hiring signal.

---

## Future improvements

- Fine-tune the embedding model on a domain-specific (tech job) corpus
- Add support for multi-role comparison ("which of these 5 JDs am I best suited for?")
- Integrate ATS simulation to flag formatting issues alongside content gaps
- Build a browser extension that scores the current job listing page against your stored resume

---

## Author

**Bhuvanesh Vinjamuri** · [GitHub](https://github.com/Bhuvan1205) · [LinkedIn](https://linkedin.com/in/bhuvaneshvinjamuri)
