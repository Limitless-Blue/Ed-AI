from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

interview_router = APIRouter(prefix="/api/interview", tags=["Interview"])


@interview_router.get("/filters")
async def get_interview_filters():
    return {
        "interviewType": ["HR", "TR"],
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
    return {"acknowledgement": True}


@interview_router.get("/results")
async def get_interview_results():
    return [
        {
            "date": "1-03-2024",
            "result": "good",
            "review": "The product performed well and met expectations.  I was particularly impressed with its durability and ease of use.  Highly recommend.",
        },
        {
            "date": "2-03-2024",
            "result": "average",
            "review": "The product is okay. It functions as described, but there are some minor issues. The build quality could be better, and the instructions were a bit unclear.  Overall, a decent value for the price.",
        },
        {
            "date": "4-03-2024",
            "result": "bad",
            "review": "I am very disappointed with this product. It malfunctioned within a few days of use. The customer service was unhelpful.  I would not recommend this product to anyone.",
        },
    ]


class VoiceChatInterviewRequest(BaseModel):
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@interview_router.post("/voice-chat")
async def interview_voice_chat(data: VoiceChatInterviewRequest):
    return {
        "responseAudio": r"API_Endpoint\Temp_Static_data\Chat\Response.opus",
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class EndInterviewRequest(BaseModel):
    conversationHistory: List[Dict[str, str]]


@interview_router.post("/end")
async def end_interview(data: EndInterviewRequest):
    return {"result": "good", "review": "Detailed feedback"}
