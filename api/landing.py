from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

landing_router = APIRouter(prefix="/api/landing", tags=["Landing"])


class VoiceChatLandingRequest(BaseModel):
    audioFile: str
    conversationHistory: List[Dict[str, Any]]


@landing_router.post("/voice-chat")
async def landing_voice_chat(data: VoiceChatLandingRequest):
    return {
        "responseAudio": r"API_Endpoint\Temp_Static_data\Chat\Response.mp3",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }
