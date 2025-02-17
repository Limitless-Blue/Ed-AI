from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.common import common_router
from api.landing import landing_router
from api.learn import learn_router
from api.practice import practice_router
from api.interview import interview_router
from api.chat import chat_router
from api.resume import resume_router
from api.jobs import jobs_router
from api.saved import saved_router
from api.settings import settings_router

app = FastAPI(title="💻 Placeholder API Application")

# Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(common_router)
app.include_router(landing_router)
app.include_router(learn_router)
app.include_router(practice_router)
app.include_router(interview_router)
app.include_router(chat_router)
app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(saved_router)
app.include_router(settings_router)


# Root Route
@app.get("/")
async def root():
    return {"message": "🎴 Welcome to the ED AI's API Application!"}
