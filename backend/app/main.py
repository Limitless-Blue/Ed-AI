from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import tutor, courses, practice, interview, progress, search, notes, settings

app = FastAPI(title="Ed-AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tutor.router,     prefix="/tutor")
app.include_router(courses.router,   prefix="/courses")
app.include_router(practice.router,  prefix="/practice")
app.include_router(interview.router, prefix="/interview")
app.include_router(progress.router,  prefix="/progress")
app.include_router(search.router,    prefix="/search")
app.include_router(notes.router,     prefix="/notes")
app.include_router(settings.router,  prefix="/settings")
