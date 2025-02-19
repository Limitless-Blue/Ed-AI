from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from api.api_functions.interview_functions import (
    update_Current_Interview,
    get_previous_results,
    interview_voice_chat_reply,
    end_interview_results,
)

interview_router = APIRouter(prefix="/api/interview", tags=["Interview"])


@interview_router.get("/filters")
async def get_interview_filters():
    return {
        "interviewType": ["TR", "HR"],
        "level": ["Easy", "Medium", "Hard"],
        "topic": ["Linked_List", "Trees", "Stacks", "Queues", "Arrays", "Strings"],
    }


class StartInterviewRequest(BaseModel):
    resumeFile: str
    InterviewType: str
    Level: str
    JobDescriptions: str
    Topics: List[str]
    OthersData: Optional[str] = None


@interview_router.post("/start")
async def start_interview(data: StartInterviewRequest):
    return update_Current_Interview(
        data.resumeFile,
        data.InterviewType,
        data.Level,
        data.JobDescriptions,
        data.Topics,
        data.OthersData,
    )


@interview_router.get("/results")
async def get_interview_results():
    return get_previous_results()


class VoiceChatInterviewRequest(BaseModel):
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@interview_router.post("/voice-chat")
async def interview_voice_chat(data: VoiceChatInterviewRequest):
    return interview_voice_chat_reply(data.audioFile, data.conversationHistory)


class EndInterviewRequest(BaseModel):
    conversationHistory: List[Dict[str, str]]


@interview_router.post("/end")
async def end_interview(data: EndInterviewRequest):
    return end_interview_results(data.conversationHistory)
