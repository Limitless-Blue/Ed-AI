from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from api.api_functions.jobs_functions import (
    get_all_job_tracker_board_data,
    edit_job_event_data,
    delete_job_event_data,
)

jobs_router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@jobs_router.get("")
async def render_job_tracker_page():
    return get_all_job_tracker_board_data()


class EditJobEventRequest(BaseModel):
    id: str
    title: str
    status: str
    deadlineDate: str
    description: str


@jobs_router.put("")
async def edit_job_event(data: List[EditJobEventRequest]):
    return edit_job_event_data(
        {
            "id": data.id,
            "title": data.title,
            "status": data.status,
            "deadlineDate": data.deadlineDate,
            "description": data.description,
        }
    )
    return {"acknowledgement": True}


class DeleteJobEventRequest(BaseModel):
    id: str


@jobs_router.delete("")
async def delete_job_event(data: DeleteJobEventRequest):
    return delete_job_event_data(data.id)
    return {"acknowledgement": True}


class JobsMentorTextChatRequest(BaseModel):
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@jobs_router.post("/mentor-help/text-chat")
async def jobs_mentor_text_chat(data: JobsMentorTextChatRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class JobsMentorVoiceChatRequest(BaseModel):
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@jobs_router.post("/mentor-help/voice-chat")
async def jobs_mentor_voice_chat(data: JobsMentorVoiceChatRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }
