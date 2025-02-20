from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from api.api_functions.resume_functions import (
    analyze_job_match_response,
    generate_cover_letter_response,
    cover_letter_chat_response,
)

resume_router = APIRouter(prefix="/api/resume", tags=["Resume"])


class ResumeAnalysisRequest(BaseModel):
    jobDescription: str


@resume_router.post("/analysis")
async def analyze_job_match(data: ResumeAnalysisRequest):
    analyze_job_match_response(data.jobDescription)


@resume_router.post("/generate-cover-letter")
async def generate_cover_letter(data: ResumeAnalysisRequest):
    generate_cover_letter_response(data.jobDescription)


class CoverLetterChatRequest(BaseModel):
    jobDescription: str
    coverLetter: str
    userMessage: Optional[str] = None


@resume_router.post("/cover-letter-chat")
async def cover_letter_chat(data: CoverLetterChatRequest):
    cover_letter_chat_response(data.jobDescription, data.coverLetter, data.userMessage)


class TaloreChatRequest(BaseModel):
    jobDescription: str
    pdfFile: str
    userMessage: Optional[str] = None
