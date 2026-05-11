import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.tutor import stream_tutor_response
from app.routes.progress import record_activity

router = APIRouter()


class TutorContext(BaseModel):
    page: str = "general"
    course_id: str | None = None
    course_title: str | None = None
    current_topic: str | None = None
    problem_id: str | None = None
    problem_title: str | None = None
    problem_description: str | None = None
    user_code: str | None = None
    failed_tests: list | None = None
    mcq_question: str | None = None


class TutorRequest(BaseModel):
    message: str
    socratic_mode: bool = True
    context: TutorContext = TutorContext()


@router.post("/message")
async def tutor_message(req: TutorRequest):
    record_activity("messages")

    async def event_stream():
        async for token in stream_tutor_response(
            req.message,
            req.socratic_mode,
            req.context.model_dump(),
        ):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
