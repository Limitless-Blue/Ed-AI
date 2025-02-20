from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from api.api_functions.landing_functions import landing_page_mentor_voice_chat_response

landing_router = APIRouter(prefix="/api/landing", tags=["Landing"])


class VoiceChatLandingRequest(BaseModel):
    audioFile: str
    conversationHistory: List[Dict[str, Any]]


@landing_router.post("/voice-chat")
async def landing_voice_chat(data: VoiceChatLandingRequest):
    return landing_page_mentor_voice_chat_response(
        data.audioFile, data.conversationHistory
    )
