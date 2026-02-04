from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ml.analyzer import analyze_resume

app = FastAPI(title="Resume AI Backend")

class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    try:
        if not data.resume_text.strip() or not data.job_description.strip():
            raise HTTPException(status_code=400, detail="Resume or Job Description is empty")

        result = analyze_resume(
            resume=data.resume_text,
            jd=data.job_description
        )

        return result

    except HTTPException as e:
        return {"error": e.detail}

    except Exception as e:
        return {"error": "Internal Server Error"}
