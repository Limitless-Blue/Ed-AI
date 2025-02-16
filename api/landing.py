from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

landing_router = APIRouter(prefix="/api/landing", tags=["Landing"])


class VoiceChatLandingRequest(BaseModel):
    audioFile: str
    conversationHistory: List[Dict[str, Any]]


@landing_router.post("/voice-chat")
async def landing_voice_chat(data: VoiceChatLandingRequest):
    return {
        "responseAudio": r"API_Endpoint\Temp_Static_data\Chat\Response.opus",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }
