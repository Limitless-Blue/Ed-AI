from fastapi import FastAPI, APIRouter, Body, Query, Path, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from api.api_functions.practice_functions import (
    practice_page_recommendations,
    get_filtered_practice_courses,
    get_all_mcq_test,
    get_all_coding_problem,
    submit_practice_function,
    end_practice_function,
)
from api.api_functions.learn_functions import (
    side_text_chat_function,
    side_voice_chat_function,
)

practice_router = APIRouter(prefix="/api/practice", tags=["Practice"])


@practice_router.get("/recommendations")
async def get_practice_recommendations():
    return practice_page_recommendations()


@practice_router.get("/items")
async def get_practice_items(
    type: str = Query(...),
    level: Optional[str] = Query(None),
    status: Optional[bool] = Query(None),
    topic: Optional[str] = Query(None),
):
    return get_filtered_practice_courses(type, level, status, topic)


@practice_router.get("/mcq/{testId}")
async def get_mcq_test(testId: str = Path()):
    return get_all_mcq_test(testId)


@practice_router.get("/coding-problem/{problemId}")
async def get_coding_problem(problemId: str = Path()):
    return get_all_coding_problem(problemId)


class SubmitPracticeRequest(BaseModel):
    courseId: str
    score: str


@practice_router.post("/submit")
async def submit_practice(data: SubmitPracticeRequest):
    return submit_practice_function(data.courseId, data.score)


class MentorHelpTextChatPracticeRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/text-chat")
async def practice_mentor_text_chat(data: MentorHelpTextChatPracticeRequest):
    return side_text_chat_function(
        data.socraticAI, data.additionalInfo, data.user, data.conversationHistory
    )


class MentorHelpVoiceChatPracticeRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/voice-chat")
async def practice_mentor_voice_chat(data: MentorHelpVoiceChatPracticeRequest):
    return side_voice_chat_function(
        data.socraticAI, data.additionalInfo, data.audioFile, data.conversationHistory
    )


class EndPracticeRequest(BaseModel):
    courseId: str
    score: str


@practice_router.post("/end")
async def end_practice(data: EndPracticeRequest):
    return end_practice_function(data.courseId, data.score)


class MentorHelpMCQTextChatRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/mcqs/text-chat")
async def practice_mentor_mcq_text_chat(data: MentorHelpMCQTextChatRequest):
    return side_text_chat_function(
        data.socraticAI, data.additionalInfo, data.user, data.conversationHistory
    )


class MentorHelpMCQVoiceChatRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/mcqs/voice-chat")
async def practice_mentor_mcq_voice_chat(data: MentorHelpMCQVoiceChatRequest):
    return side_voice_chat_function(
        data.socraticAI, data.additionalInfo, data.audioFile, data.conversationHistory
    )
