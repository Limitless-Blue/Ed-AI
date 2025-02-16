from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

interview_router = APIRouter(prefix="/api/interview", tags=["Interview"])


class StartInterviewRequest(BaseModel):
    resumeFile: str
    InterviewType: str
    Level: str
    JobDescriptions: str
    Topics: List[str]


@interview_router.post("/start")
async def start_interview(data: StartInterviewRequest):
    return {"acknowledgement": True}
