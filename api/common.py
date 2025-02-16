from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from api.api_functions.common_functions import streak_data

common_router = APIRouter(prefix="/api/common", tags=["Common"])


@common_router.get("/streak")
async def get_streak_data():
    return streak_data()


# TODO: added Gretting Audio
@common_router.get("/greeting-audio")
async def get_greeting_audio():
    return {
        "audioFilePath": r"API_Endpoint\Temp_Static_data\Profile\greeting_audio.opus"
    }


@common_router.get("/user-details")
async def get_user_details():
    return {
        "firstName": "Katoro",
        "lastName": "Kamado",
        "image": r"API_Endpoint\Temp_Static_data\Profile\user_image.png",
    }


class SaveBookmarkRequest(BaseModel):
    id: str
    value: bool


@common_router.post("/save")
async def save_bookmark(data: SaveBookmarkRequest):
    return {"acknowledgement": True}
