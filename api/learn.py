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


@learn_router.get("/courses")
async def get_all_courses(
    level: Optional[str] = Query(None),
    status: Optional[bool] = Query(None),
    topic: Optional[str] = Query(None),
):
    return get_filtered_learn_courses(level, status, topic)


@learn_router.get("/course/{courseId}")
async def get_course_content(courseId: str = Path()):
    return get_learn_page_data(courseId)


class TextChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@learn_router.post("/text-chat")
async def learn_text_chat(data: TextChatLearnRequest):
    return learn_text_chat(
        data.socraticAI, data.additionalInfo, data.user, data.conversationHistory
    )


class VoiceChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@learn_router.post("/voice-chat")
async def learn_voice_chat(data: VoiceChatLearnRequest):
    return learn_voice_chat(
        data.socraticAI, data.additionalInfo, data.audioFile, data.conversationHistory
    )


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


@learn_router.post("/mentor-help/text-chat")
async def learn_mentor_text_chat(data: MentorHelpTextChatLearnRequest):
    return learn_text_chat(
        data.socraticAI, data.additionalInfo, data.user, data.conversationHistory
    )


class MentorHelpVoiceChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@learn_router.post("/mentor-help/voice-chat")
async def learn_mentor_voice_chat(data: MentorHelpVoiceChatLearnRequest):
    return learn_voice_chat(
        data.socraticAI, data.additionalInfo, data.audioFile, data.conversationHistory
    )
