from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional

practice_router = APIRouter(prefix="/api/practice", tags=["Practice"])


@practice_router.get("/recommendations")
async def get_practice_recommendations():
    return {
        "mcqRecommendations": [
            {"id": "MCPA_1", "practiceName": "Queues"},
        ],
        "filters": {
            "mcqs": {"level": ["Easy", "Medium", "Hard"]},
        },
    }
