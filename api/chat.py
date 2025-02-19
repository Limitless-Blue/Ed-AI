from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from api.api_functions.chat_function import (
    chat_text_text_socraticAI,
    chat_text_text_Non_socraticAI,
    chat_text_voice_socraticAI,
    chat_text_voice_Non_socraticAI,
)

chat_router = APIRouter(prefix="/api/chat", tags=["Chat"])


class TextChatRequest(BaseModel):
    socraticAI: bool
    user: str
    conversationHistory: List[Dict[str, str]]


@chat_router.post("/text")
async def chat_text(data: TextChatRequest):
    if data.socraticAI:
        return chat_text_text_socraticAI(data.user, data.conversationHistory)

    else:
        return chat_text_text_Non_socraticAI(data.user, data.conversationHistory)


class VoiceChatRequest(BaseModel):
    socraticAI: bool
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@chat_router.post("/voice")
async def chat_voice(data: VoiceChatRequest):
    if data.socraticAI:
        return chat_text_voice_socraticAI(data.audioFile, data.conversationHistory)

    else:
        return chat_text_voice_Non_socraticAI(data.audioFile, data.conversationHistory)
