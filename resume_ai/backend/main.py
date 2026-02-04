from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from resume_ai.ml.analyzer import analyze_resume
import pdfplumber
import io

app = FastAPI(title="Resume AI API")


# Input Schema
class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


# Health Check
@app.get("/")
def home():
    return {"message": "Resume AI Backend Running"}


# Main Analysis Endpoint
from fastapi import File, UploadFile, Form

@app.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    resume_text: str = Form(None),
    resume_file: UploadFile = File(None)
):

    try:

        # If PDF uploaded → extract text
        if resume_file:

            if not resume_file.filename.endswith(".pdf"):
                raise HTTPException(400, "Only PDF allowed")

            with pdfplumber.open(io.BytesIO(await resume_file.read())) as pdf:

                resume_text = ""

                for page in pdf.pages:
                    resume_text += page.extract_text() + "\n"


        # Validation
        if not resume_text or not resume_text.strip():
            raise HTTPException(400, "Resume is empty")

        if not job_description.strip():
            raise HTTPException(400, "Job Description is empty")


        result = analyze_resume(resume_text, job_description)

        return result


    except Exception as e:
        raise HTTPException(500, str(e))

