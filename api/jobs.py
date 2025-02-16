from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

jobs_router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@jobs_router.get("")
async def render_job_tracker_page():
    return [
        {
            "id": "job_id_1",
            "title": "Software Engineer",
            "status": "In Progress",
            "deadlineDate": "1-03-2024",
            "description": """Develop and maintain web applications using React and Node.js.""",
        },
        {
            "id": "job_id_2",
            "title": "Data Scientist",
            "status": "Completed",
            "deadlineDate": "2-03-2024",
            "description": """Analyze large datasets to identify trends and insights.""",
        },
        {
            "id": "job_id_3",
            "title": "Project Manager",
            "status": "Pending",
            "deadlineDate": "3-03-2024",
            "description": """Oversee the planning and execution of software development projects.""",
        },
        {
            "id": "job_id_4",
            "title": "UX Designer",
            "status": "In Progress",
            "deadlineDate": "4-03-2024",
            "description": """Design user interfaces for web and mobile applications.""",
        },
        {
            "id": "job_id_5",
            "title": "QA Engineer",
            "status": "Completed",
            "deadlineDate": "5-03-2024",
            "description": """Test software applications to ensure quality and identify bugs.""",
        },
    ]


class EditJobEventRequest(BaseModel):
    id: str
    title: str
    status: str
    deadlineDate: str
    description: str


@jobs_router.put("")
async def edit_job_event(data: List[EditJobEventRequest]):
    return {"acknowledgement": True}


class DeleteJobEventRequest(BaseModel):
    id: str


@jobs_router.delete("")
async def delete_job_event(data: DeleteJobEventRequest):
    return {"acknowledgement": True}


class JobsMentorTextChatRequest(BaseModel):
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


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
