from fastapi import APIRouter
from pydantic import BaseModel

jobs_router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@jobs_router.get("")
async def render_job_tracker_page():
    return [
        {"id": "job_id_1", "title": "Software Engineer"},
    ]
