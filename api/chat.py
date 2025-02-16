from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

chat_router = APIRouter(prefix="/api/chat", tags=["Chat"])


class TextChatRequest(BaseModel):
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
