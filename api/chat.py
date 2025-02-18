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


# TODO: Add AI Part
@chat_router.post("/text")
async def chat_text(data: TextChatRequest):
    if data.socraticAI:
        return chat_text_text_socraticAI(data.user, data.conversationHistory)
        # return {
        #     "user": "Transcribed user speech",
        #     "AI": "AI's text response",
        #     "conversationHistory": [
        #         {"speaker": "user", "text": "Transcribed user speech"},
        #         {"speaker": "AI", "text": "AI's text response"},
        #     ],
        # }
    else:
        return chat_text_text_Non_socraticAI(data.user, data.conversationHistory)
        # return {
        #     "user": "Transcribed user speech",
        #     "AI": "AI's text response",
        #     "conversationHistory": [
        #         {"speaker": "user", "text": "Transcribed user speech"},
        #         {"speaker": "AI", "text": "AI's text response"},
        #     ],
        # }


class VoiceChatRequest(BaseModel):
    socraticAI: bool
    audioFile: str
    conversationHistory: List[Dict[str, str]]


# TODO: Add AI Part
@chat_router.post("/voice")
async def chat_voice(data: VoiceChatRequest):
    if data.socraticAI:
        return chat_text_voice_socraticAI(data.audioFile, data.conversationHistory)
        # return {
        #     "user": "Transcribed user speech",
        #     "AI": "AI's text response",
        #     "conversationHistory": [
        #         {"speaker": "user", "text": "Transcribed user speech"},
        #         {"speaker": "AI", "text": "AI's text response"},
        #     ],
        # }
    else:
        return chat_text_voice_Non_socraticAI(data.audioFile, data.conversationHistory)
        # return {
        #     "user": "Transcribed user speech",
        #     "AI": "AI's text response",
        #     "conversationHistory": [
        #         {"speaker": "user", "text": "Transcribed user speech"},
        #         {"speaker": "AI", "text": "AI's text response"},
        #     ],
        # }
