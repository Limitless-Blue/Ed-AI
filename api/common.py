from fastapi import APIRouter
from pydantic import BaseModel

common_router = APIRouter(prefix="/api/common", tags=["Common"])


@common_router.get("/streak")
async def get_streak_data():
    return {
        "streak": 5,
        "streakData": [
            {"date": "1-03-2024", "status": False},
            {"date": "2-03-2024", "status": True},
            {"date": "3-03-2024", "status": True},
            {"date": "4-03-2024", "status": False},
            {"date": "5-03-2024", "status": True},
        ],
    }


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
