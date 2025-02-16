from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

chat_router = APIRouter(prefix="/api/chat", tags=["Chat"])


class TextChatRequest(BaseModel):
    socraticAI: bool
    user: str
    conversationHistory: List[Dict[str, str]]


@chat_router.post("/text")
async def chat_text(data: TextChatRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class VoiceChatRequest(BaseModel):
    socraticAI: bool
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@chat_router.post("/voice")
async def chat_voice(data: VoiceChatRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }
