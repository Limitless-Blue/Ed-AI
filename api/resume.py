from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

resume_router = APIRouter(prefix="/api/resume", tags=["Resume"])


class ResumeAnalysisRequest(BaseModel):
    jobDescription: str


@resume_router.post("/analysis")
async def analyze_job_match(data: ResumeAnalysisRequest):
    return {
        "match": "Good",
        "skillGapAnalysis": "Analysis details...",
        "salaryInsights": "Insights details...",
        "linkedinPeople": [
            {"name": "Katoro", "url": "https://www.linkedin.com/in/example"},
            {"name": "person_2", "url": None},
        ],
    }


@resume_router.post("/generate-cover-letter")
async def generate_cover_letter(data: ResumeAnalysisRequest):
    return {
        "coverLetter": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt"
    }


class CoverLetterChatRequest(BaseModel):
    jobDescription: str
    coverLetter: str
    userMessage: Optional[str] = None


@resume_router.post("/cover-letter-chat")
async def cover_letter_chat(data: CoverLetterChatRequest):
    return {
        "coverLetter": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt"
    }


@resume_router.get("/previous-cover-letters")
async def get_previous_cover_letters():
    return [
        {
            "date": "1-03-2024",
            "result": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt",
        },
    ]
