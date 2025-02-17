from fastapi import FastAPI, APIRouter, Body, Query, Path, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Optional
from api.api_functions.learn_functions import (
    learn_page_recommendations,
    get_learn_page_data,
    get_filtered_learn_courses,
)

learn_router = APIRouter(prefix="/api/learn", tags=["Learn"])


@learn_router.get("/recommendations")
async def get_learn_recommendations():
    return learn_page_recommendations()


# TODO: Added filters and changes to database
@learn_router.get("/courses")
async def get_all_courses(
    level: Optional[str] = Query(None),
    status: Optional[bool] = Query(None),
    topic: Optional[str] = Query(None),
):
    return [
        {"id": "LEPA_1", "courseName": "DSA Intro"},
        {"id": "LEPA_2", "courseName": "Trees"},
        {"id": "LEPA_3", "courseName": "Linked Lists"},
        {"id": "LEPA_4", "courseName": "Arrays"},
        {"id": "LEPA_5", "courseName": "Stacks"},
        {"id": "LEPA_6", "courseName": "DSA Intro"},
        {"id": "LEPA_7", "courseName": "Trees"},
        {"id": "LEPA_8", "courseName": "Linked Lists"},
        {"id": "LEPA_9", "courseName": "Arrays"},
        {"id": "LEPA_10", "courseName": "Stacks"},
    ]


@learn_router.get("/course/{courseId}")
async def get_course_content(courseId: str = Path()):
    return get_learn_page_data(courseId)


class TextChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@learn_router.post("/text-chat")
async def learn_text_chat(data: TextChatLearnRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class VoiceChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@learn_router.post("/voice-chat")
async def learn_voice_chat(data: VoiceChatLearnRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class EndCourseRequest(BaseModel):
    courseId: str
    testResults: Dict[str, Dict[str, str]]


# TODO: Add AI Part
@learn_router.post("/end-course")
async def end_course(data: EndCourseRequest):
    return {"acknowledgement": True}


class MentorHelpTextChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@learn_router.post("/mentor-help/text-chat")
async def learn_mentor_text_chat(data: MentorHelpTextChatLearnRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class MentorHelpVoiceChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@learn_router.post("/mentor-help/voice-chat")
async def learn_mentor_voice_chat(data: MentorHelpVoiceChatLearnRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }
