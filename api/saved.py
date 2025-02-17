from fastapi import FastAPI, APIRouter, Body, Query, Path, Query
from api.api_functions.saved_functions import retrieve_saved_courses

saved_router = APIRouter(prefix="/api/saved", tags=["Saved"])


@saved_router.get("/filters")
async def get_saved_filters():
    return {"type": ["Course", "MCQ", "Coding"]}


@saved_router.get("/courses")
async def get_saved_courses(type: str | None = Query(None)):
    return retrieve_saved_courses(type)
