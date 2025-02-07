# TODO: Remove unccesry commas

from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

app = FastAPI(title="💻Placeholder API Application")

# ======================================================
# 1. Common API
# ======================================================

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


# ======================================================
# 2. Landing Page
# ======================================================

landing_router = APIRouter(prefix="/api/landing", tags=["Landing"])


class VoiceChatLandingRequest(BaseModel):
    audioFile: str
    conversationHistory: List[Dict[str, Any]]


@landing_router.post("/voice-chat")
async def landing_voice_chat(data: VoiceChatLandingRequest):
    return {
        "responseAudio": r"API_Endpoint\Temp_Static_data\Chat\Response.opus",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "" "text": "AI's text response"},
        ],
    }


# ======================================================
# 3. Learn Section
# ======================================================

learn_router = APIRouter(prefix="/api/learn", tags=["Learn"])


@learn_router.get("/recommendations")
async def get_learn_recommendations():
    return {
        "recommendations": [
            {"id": "1", "courseName": "DSA Intro"},
            {"id": "2", "courseName": "Trees"},
            {"id": "3", "courseName": "Linked Lists"},
            {"id": "4", "courseName": "Arrays"},
            {"id": "5", "courseName": "Stacks"},
        ],
        "filters": {
            "level": ["Easy", "Medium", "Hard"],
            "topic": ["Linked_List", "Trees", "Stacks", "Queues", "Arrays", "Strings"],
            "status": [True, False],
        },
    }


@learn_router.get("/courses")
async def get_all_courses(
    level: Optional[str] = Query(None),
    status: Optional[bool] = Query(None),
    topic: Optional[str] = Query(None),
):
    return [
        {"id": "1", "courseName": "DSA Intro"},
        {"id": "2", "courseName": "Trees"},
        {"id": "3", "courseName": "Linked Lists"},
        {"id": "4", "courseName": "Arrays"},
        {"id": "5", "courseName": "Stacks"},
    ]


@learn_router.get("/course/{courseId}")
async def get_course_content(courseId: str = Path()):
    return {
        "course": [
            r"API_Endpoint\Temp_Static_data\Learn Page\DSA_Intro_1.md",
            r"API_Endpoint\Temp_Static_data\Learn Page\DSA_Intro_2.md",
            r"API_Endpoint\Temp_Static_data\Learn Page\DSA_Intro_3.md",
        ],
        "test": [
            r"API_Endpoint\Temp_Static_data\Learn Page\DSA_Intro_1.json",
            r"API_Endpoint\Temp_Static_data\Learn Page\DSA_Intro_2.json",
            r"API_Endpoint\Temp_Static_data\Learn Page\DSA_Intro_3.json",
        ],
        "bookmark": True,
        "completed": True,
    }


class TextChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@learn_router.post("/text-chat")
async def learn_text_chat(data: TextChatLearnRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class VoiceChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@learn_router.post("/voice-chat")
async def learn_voice_chat(data: VoiceChatLearnRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class EndCourseRequest(BaseModel):
    courseId: str
    testResults: Dict[str, Dict[str, str]]


@learn_router.post("/end-course")
async def end_course(data: EndCourseRequest):
    return {"acknowledgement": True}


class MentorHelpTextChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@learn_router.post("/mentor-help/text-chat")
async def learn_mentor_text_chat(data: MentorHelpTextChatLearnRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class MentorHelpVoiceChatLearnRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@learn_router.post("/mentor-help/voice-chat")
async def learn_mentor_voice_chat(data: MentorHelpVoiceChatLearnRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


# ======================================================
# 4. Practice Section
# ======================================================

practice_router = APIRouter(prefix="/api/practice", tags=["Practice"])


@practice_router.get("/recommendations")
async def get_practice_recommendations():
    return {
        "mcqRecommendations": [
            {"id": "1", "practiceName": "Queues"},
            {"id": "2", "practiceName": "Trees"},
            {"id": "3", "practiceName": "Linked Lists"},
            {"id": "4", "practiceName": "Arrays"},
            {"id": "5", "practiceName": "Stacks"},
        ],
        "codingRecommendations": [
            {"id": "1", "practiceName": "Queues"},
            {"id": "2", "practiceName": "Trees"},
            {"id": "3", "practiceName": "Linked Lists"},
            {"id": "4", "practiceName": "Arrays"},
            {"id": "5", "practiceName": "Stacks"},
        ],
        "filters": {
            "mcqs": {
                "level": ["Easy", "Medium", "Hard"],
                "topic": ["Queues", "Trees", "Linked Lists"],
                "status": [True, False],
            },
            "codingQuestions": {
                "level": ["Easy", "Medium", "Hard"],
                "topic": ["Queues", "Trees", "Linked Lists"],
                "status": [True, False],
            },
        },
    }


@practice_router.get("/items")
async def get_practice_items(
    type: str = Query(...),
    level: Optional[str] = Query(None),
    status: Optional[bool] = Query(None),
    topic: Optional[str] = Query(None),
):
    return [
        {"id": "1", "practiceName": "Queues", "status": True, "difficulty": "easy"},
        {"id": "2", "practiceName": "Trees", "status": True, "difficulty": "easy"},
        {
            "id": "3",
            "practiceName": "Linked Lists",
            "status": True,
            "difficulty": "easy",
        },
        {"id": "4", "practiceName": "Arrays", "status": False, "difficulty": "easy"},
        {"id": "5", "practiceName": "Stacks", "status": False, "difficulty": "easy"},
    ]


@practice_router.get("/mcq/{testId}")
async def get_mcq_test(testId: str = Path()):
    return {
        "testFile": r"API_Endpoint\Temp_Static_data\Practice Page\MCQ\Programming_Fundamentals_000001.json"
    }


@practice_router.get("/coding-problem/{problemId}")
async def get_coding_problem(problemId: str = Path()):
    return {
        "problemDescription": r"API_Endpoint\Temp_Static_data\Practice Page\CodingProblem\Concatenation_of_Array.md",
        "problemSolution": r"API_Endpoint\Temp_Static_data\Practice Page\CodingProblem\Concatenation_of_Array_solution.py",
        "testCases": [
            ["1 2 1", [1, 2, 1, 1, 2, 1]],
            ["1 3 2 1", [1, 3, 2, 1, 1, 3, 2, 1]],
            ["5 6", [5, 6, 5, 6]],
            ["9", [9, 9]],
        ],
    }


class SubmitPracticeRequest(BaseModel):
    courseId: str
    score: str


@practice_router.post("/submit")
async def submit_practice(data: SubmitPracticeRequest):
    return {"acknowledgement": True}


class MentorHelpTextChatPracticeRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/text-chat")
async def practice_mentor_text_chat(data: MentorHelpTextChatPracticeRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class MentorHelpVoiceChatPracticeRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/voice-chat")
async def practice_mentor_voice_chat(data: MentorHelpVoiceChatPracticeRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class EndPracticeRequest(BaseModel):
    courseId: str
    score: str


@practice_router.post("/end")
async def end_practice(data: EndPracticeRequest):
    return {"acknowledgement": True}


class MentorHelpMCQTextChatRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/mcqs/text-chat")
async def practice_mentor_mcq_text_chat(data: MentorHelpMCQTextChatRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class MentorHelpMCQVoiceChatRequest(BaseModel):
    socraticAI: bool
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@practice_router.post("/mentor-help/mcqs/voice-chat")
async def practice_mentor_mcq_voice_chat(data: MentorHelpMCQVoiceChatRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


# ======================================================
# 5. Interview Simulation Section
# ======================================================

interview_router = APIRouter(prefix="/api/interview", tags=["Interview"])


@interview_router.get("/filters")
async def get_interview_filters():
    return {
        "interviewType": ["HR", "TR"],
        "level": ["Easy", "Medium", "Hard"],
        "topic": ["Linked_List", "Trees", "Stacks", "Queues", "Arrays", "Strings"],
    }


class StartInterviewRequest(BaseModel):
    resumeFile: str
    InterviewType: str
    Level: str
    JobDescriptions: str
    Topics: List[str]
    OthersData: Optional[str] = None


@interview_router.post("/start")
async def start_interview(data: StartInterviewRequest):
    return {"acknowledgement": True}


@interview_router.get("/results")
async def get_interview_results():
    return [
        {
            "date": "1-03-2024",
            "result": "good",
            "review": "The product performed well and met expectations.  I was particularly impressed with its durability and ease of use.  Highly recommend.",
        },
        {
            "date": "2-03-2024",
            "result": "average",
            "review": "The product is okay. It functions as described, but there are some minor issues. The build quality could be better, and the instructions were a bit unclear.  Overall, a decent value for the price.",
        },
        {
            "date": "4-03-2024",
            "result": "bad",
            "review": "I am very disappointed with this product. It malfunctioned within a few days of use. The customer service was unhelpful.  I would not recommend this product to anyone.",
        },
    ]


class VoiceChatInterviewRequest(BaseModel):
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@interview_router.post("/voice-chat")
async def interview_voice_chat(data: VoiceChatInterviewRequest):
    return {
        "responseAudio": r"API_Endpoint\Temp_Static_data\Chat\Response.opus",
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class EndInterviewRequest(BaseModel):
    conversationHistory: List[Dict[str, str]]


@interview_router.post("/end")
async def end_interview(data: EndInterviewRequest):
    return {"result": "good", "review": "Detailed feedback"}


# ======================================================
# 6. Chat Page
# ======================================================

chat_router = APIRouter(prefix="/api/chat", tags=["Chat"])


class TextChatRequest(BaseModel):
    socraticAI: bool
    user: str
    conversationHistory: List[Dict[str, str]]


@chat_router.post("/text")
async def chat_text(data: TextChatRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class VoiceChatRequest(BaseModel):
    socraticAI: bool
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@chat_router.post("/voice")
async def chat_voice(data: VoiceChatRequest):
    return {
        "user": r"API_Endpoint\Temp_Static_data\Chat\Response.opus",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


# ======================================================
# 7. Resume Optimization Page
# ======================================================

resume_router = APIRouter(prefix="/api/resume", tags=["Resume"])


class ResumeAnalysisRequest(BaseModel):
    jobDescription: str


@resume_router.post("/analysis")
async def analyze_job_match(data: ResumeAnalysisRequest):
    return {
        "match": "Good",
        "skillGapAnalysis": """Analysis details...""",
        "salaryInsights": """Insights details...""",
        "linkedinPeople": [
            {
                "name": "Katoro",
                "url": "https://www.linkedin.com/in/chaitanya-venkata-a5a908212/",
            },
            {"name": "person_2", "url": None},
            {"name": "person_3", "url": None},
        ],
    }


@resume_router.post("/generate-cover-letter")
async def generate_cover_letter(data: ResumeAnalysisRequest):
    return {
        "coverLetter": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt"
    }


@resume_router.post("/generate-talore")
async def generate_talore_resume(data: ResumeAnalysisRequest):
    return {
        "pdfFile": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\generated_resume.pdf"
    }


class CoverLetterChatRequest(BaseModel):
    jobDescription: str
    coverLetter: str
    userMessage: Optional[str] = None


@resume_router.post("/cover-letter-chat")
async def cover_letter_chat(data: CoverLetterChatRequest):
    return {
        "coverLetter": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt"
    }


class TaloreChatRequest(BaseModel):
    jobDescription: str
    pdfFile: str
    userMessage: Optional[str] = None


@resume_router.post("/talore-chat")
async def talore_chat(data: TaloreChatRequest):
    return {
        "pdfFile": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\generated_resume.pdf"
    }


@resume_router.get("/previous-cover-letters")
async def get_previous_cover_letters():
    return [
        {
            "date": "1-03-2024",
            "result": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt",
        },
        {
            "date": "2-03-2024",
            "result": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt",
        },
        {
            "date": "3-03-2024",
            "result": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt",
        },
    ]


# ======================================================
# 8. Job Tracker
# ======================================================

jobs_router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@jobs_router.get("")
async def render_job_tracker_page():
    return [
        {
            "id": "job_id_1",
            "title": "Software Engineer",
            "status": "In Progress",
            "deadlineDate": "1-03-2024",
            "description": """Develop and maintain web applications using React and Node.js.""",
        },
        {
            "id": "job_id_2",
            "title": "Data Scientist",
            "status": "Completed",
            "deadlineDate": "2-03-2024",
            "description": """Analyze large datasets to identify trends and insights.""",
        },
        {
            "id": "job_id_3",
            "title": "Project Manager",
            "status": "Pending",
            "deadlineDate": "3-03-2024",
            "description": """Oversee the planning and execution of software development projects.""",
        },
        {
            "id": "job_id_4",
            "title": "UX Designer",
            "status": "In Progress",
            "deadlineDate": "4-03-2024",
            "description": """Design user interfaces for web and mobile applications.""",
        },
        {
            "id": "job_id_5",
            "title": "QA Engineer",
            "status": "Completed",
            "deadlineDate": "5-03-2024",
            "description": """Test software applications to ensure quality and identify bugs.""",
        },
    ]


class EditJobEventRequest(BaseModel):
    id: str
    title: str
    status: str
    deadlineDate: str
    description: str


@jobs_router.put("")
async def edit_job_event(data: List[EditJobEventRequest]):
    return {"acknowledgement": True}


class DeleteJobEventRequest(BaseModel):
    id: str


@jobs_router.delete("")
async def delete_job_event(data: DeleteJobEventRequest):
    return {"acknowledgement": True}


class JobsMentorTextChatRequest(BaseModel):
    additionalInfo: Dict[str, Any]
    user: str
    conversationHistory: List[Dict[str, str]]


@jobs_router.post("/mentor-help/text-chat")
async def jobs_mentor_text_chat(data: JobsMentorTextChatRequest):
    return {
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


class JobsMentorVoiceChatRequest(BaseModel):
    additionalInfo: Dict[str, Any]
    audioFile: str
    conversationHistory: List[Dict[str, str]]


@jobs_router.post("/mentor-help/voice-chat")
async def jobs_mentor_voice_chat(data: JobsMentorVoiceChatRequest):
    return {
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


# ======================================================
# 9. Saved Pages
# ======================================================

saved_router = APIRouter(prefix="/api/saved", tags=["Saved"])


@saved_router.get("/filters")
async def get_saved_filters():
    return {"type": ["Course", "MCQ", "Coding"]}


@saved_router.get("/courses")
async def get_saved_courses(type: str = Query(...)):
    return ["id_1", "id_2", "id_3"]


# ======================================================
# 10. Settings
# ======================================================

settings_router = APIRouter(prefix="/api/settings", tags=["Settings"])


class ChangePasswordRequest(BaseModel):
    OldPassword: str
    newPassword: str


@settings_router.put("/change-password")
async def change_password(data: ChangePasswordRequest):
    return {"acknowledgement": True}


class ChangeUsernameRequest(BaseModel):
    OldUsername: str
    newUsername: str


@settings_router.put("/change-username")
async def change_username(data: ChangeUsernameRequest):
    return {"acknowledgement": True}


class ResetProgressRequest(BaseModel):
    Password: str


@settings_router.post("/reset-progress")
async def reset_progress(data: ResetProgressRequest):
    return {"acknowledgement": True}


# ======================================================
# Include Routers in the Main App
# ======================================================

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

# ======================================================
# Main
# ======================================================


@app.get("/")
async def root():
    return {"message": "💻 Welcome to the Placeholder API Application!"}
