from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from api.api_functions.common_functions import (
    streak_data,
    get_user_website_data,
    save_bookmark_to_database,
)

common_router = APIRouter(prefix="/api/common", tags=["Common"])


@common_router.get("/streak")
async def get_streak_data():
    return streak_data()


@common_router.get("/greeting-audio")
async def get_greeting_audio():
    return {"audioFilePath": "Database\\user_data\\greeting_audio.mp3"}


@common_router.get("/user-details")
async def get_user_details():
    return get_user_website_data()


class SaveBookmarkRequest(BaseModel):
    id: str
    value: bool


@common_router.post("/save")
async def save_bookmark(data: SaveBookmarkRequest):
    return save_bookmark_to_database(data.id, data.value)
