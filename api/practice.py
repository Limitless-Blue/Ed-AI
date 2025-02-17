from fastapi import FastAPI, APIRouter, Body, Query, Path, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from api.api_functions.practice_functions import (
    practice_page_recommendations,
    get_filtered_practice_courses,
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
    return {
        "testFile": r"API_Endpoint\Temp_Static_data\Practice Page\MCQ\Programming_Fundamentals_000001.json"
    }


@practice_router.get("/coding-problem/{problemId}")
async def get_coding_problem(problemId: str = Path()):
    return {
        "problemDescription": r"API_Endpoint\Temp_Static_data\Practice Page\CodingProblem\Concatenation_of_Array.md",
        "problemSolution": r"API_Endpoint\Temp_Static_data\Practice Page\CodingProblem\Concatenation_of_Array_solution.py",
        "testCases": [
            ["1 2 1", [1, 2, 1, 1, 2, 1]],
            ["1 3 2 1", [1, 3, 2, 1, 1, 3, 2, 1]],
            ["5 6", [5, 6, 5, 6]],
            ["9", [9, 9]],
        ],
    }


class SubmitPracticeRequest(BaseModel):
    courseId: str
    score: str


# TODO: Add AI Part
@practice_router.post("/submit")
async def submit_practice(data: SubmitPracticeRequest):
    return {"acknowledgement": True}


class MentorHelpTextChatPracticeRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@practice_router.post("/mentor-help/text-chat")
async def practice_mentor_text_chat(data: MentorHelpTextChatPracticeRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class MentorHelpVoiceChatPracticeRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@practice_router.post("/mentor-help/voice-chat")
async def practice_mentor_voice_chat(data: MentorHelpVoiceChatPracticeRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class EndPracticeRequest(BaseModel):
    courseId: str
    score: str


# TODO: Add AI Part
@practice_router.post("/end")
async def end_practice(data: EndPracticeRequest):
    return {"acknowledgement": True}


class MentorHelpMCQTextChatRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@practice_router.post("/mentor-help/mcqs/text-chat")
async def practice_mentor_mcq_text_chat(data: MentorHelpMCQTextChatRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class MentorHelpMCQVoiceChatRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@practice_router.post("/mentor-help/mcqs/voice-chat")
async def practice_mentor_mcq_voice_chat(data: MentorHelpMCQVoiceChatRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }
