from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

resume_router = APIRouter(prefix="/api/resume", tags=["Resume"])


class ResumeAnalysisRequest(BaseModel):
    jobDescription: str


@resume_router.post("/analysis")
async def analyze_job_match(data: ResumeAnalysisRequest):
    return {
        "match": "Good",
        "skillGapAnalysis": """Analysis details...""",
        "salaryInsights": """Insights details...""",
        "linkedinPeople": [
            {
                "name": "Katoro",
                "url": "https://www.linkedin.com/in/chaitanya-venkata-a5a908212/",
            },
            {"name": "person_2", "url": None},
            {"name": "person_3", "url": None},
        ],
    }


@resume_router.post("/generate-cover-letter")
async def generate_cover_letter(data: ResumeAnalysisRequest):
    return {
        "coverLetter": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt"
    }


@resume_router.post("/generate-talore")
async def generate_talore_resume(data: ResumeAnalysisRequest):
    return {
        "pdfFile": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\generated_resume.pdf"
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


class TaloreChatRequest(BaseModel):
    jobDescription: str
    pdfFile: str
    userMessage: Optional[str] = None


@resume_router.post("/talore-chat")
async def talore_chat(data: TaloreChatRequest):
    return {
        "pdfFile": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\generated_resume.pdf"
    }


@resume_router.get("/previous-cover-letters")
async def get_previous_cover_letters():
    return [
        {
            "date": "1-03-2024",
            "result": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt",
        },
        {
            "date": "2-03-2024",
            "result": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt",
        },
        {
            "date": "3-03-2024",
            "result": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt",
        },
    ]
