from fastapi import APIRouter, Query

saved_router = APIRouter(prefix="/api/saved", tags=["Saved"])


@saved_router.get("/filters")
async def get_saved_filters():
    return {"type": ["Course", "MCQ", "Coding"]}


@saved_router.get("/courses")
async def get_saved_courses(type: str = Query(...)):
    return ["id_1", "id_2", "id_3"]
