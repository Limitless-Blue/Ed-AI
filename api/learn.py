from fastapi import APIRouter, Query, Path
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

learn_router = APIRouter(prefix="/api/learn", tags=["Learn"])


@learn_router.get("/recommendations")
async def get_learn_recommendations():
    return {
        "recommendations": [
            {"id": "LEPA_1", "courseName": "DSA Intro"},
            {"id": "LEPA_2", "courseName": "Trees"},
        ],
        "filters": {
            "level": ["Easy", "Medium", "Hard"],
            "topic": ["Linked_List", "Trees", "Stacks", "Queues", "Arrays", "Strings"],
        },
    }


@learn_router.get("/course/{courseId}")
async def get_course_content(courseId: str = Path()):
    return {
        "course": [
            r"API_Endpoint\Temp_Static_data\Learn Page\DSA_Intro_1.md",
        ],
        "bookmark": True,
        "completed": True,
    }
