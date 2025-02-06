# API Endpoints Plan

---

## 1. Common API

### 1.1. Default Login Data

#### 1.1.1. Get Streak Data
- **Method:** GET
- **URL:** `/api/common/streak`
- **Input:** None
- **Output:**
```json
{
  "streak": 5,
  "streakData": [
    { "date": "dd-mm-yyyy", "status": true },
    { "date": "dd-mm-yyyy", "status": false },
    { "date": "dd-mm-yyyy", "status": true },
    { "date": "dd-mm-yyyy", "status": true },
    { "date": "dd-mm-yyyy", "status": false },
    { "date": "dd-mm-yyyy", "status": true }
  ]
}
```

#### 1.1.2. Get Greeting Audio
- **Method:** GET
- **URL:** `/api/common/greeting-audio`
- **Input:** None
- **Output:**
```json
{
  "audioFilePath": "/path/to/greeting_audio.mp3"
}
```

#### 1.1.3. Get User Details
- **Method:** GET
- **URL:** `/api/common/user-details`
- **Input:** None
- **Output:**
```json
{
  "firstName": "Katoro",
  "lastName": "Kamado",
  "image": "/path/to/user_image.png"
}
```

### 1.2. Save Book mark
- **Method:** POST
- **URL:** `/api/common/save`
- **Input:**
```json
{
  "id": "course_Or_pratice_id",
  "value": true
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

---

## 2. Landing Page

### 2.1. Voice Chat Endpoint
- **Method:** POST
- **URL:** `/api/landing/voice-chat`
- **Input:**
```json
{
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "responseAudio": "/path/to/response_audio.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

---

## 3. Learn Section

### 3.1. Learn Page 1

#### 3.1.1. Get Recommendations & Filters for Courses
- **Method:** GET
- **URL:** `/api/learn/recommendations`
- **Input:** None
- **Output:**
```json
{
  "recommendations": [
    { "id": "1", "courseName": "DSA Intro" },
    { "id": "2", "courseName": "Trees" },
    { "id": "3", "courseName": "Linked Lists" }
  ],
  "filters": {
    "level": ["Easy", "Medium", "Hard"],
    "topic": ["Linked_List", "Trees", "Stacks", "Queues", "Arrays", "Strings"],
    "status": [true, false]
  }
}
```

#### 3.1.2. Get All Courses (with optional filters)
- **Method:** GET
- **URL:** `/api/learn/courses`
- **Input:** (Query Parameters)
```json
{
  "level": "Optional[string]",
  "status": "Optional[boolean]",
  "topic": "Optional[string]"
}
```
- **Output:**
```json
[
  { "id": "1", "courseName": "DSA Intro" },
  { "id": "2", "courseName": "Trees" },
  { "id": "3", "courseName": "Linked Lists" }
]
```

#### 3.1.3. Get Course Content and Test Data
- **Method:** GET
- **URL:** `/api/learn/course/{courseId}`
- **Input:** URL Parameter: `courseId`
- **Output:**
```json
{
  "course": [
    "{filePath}/DSA_Intro_1.md",
    "{filePath}/DSA_Intro_2.md",
    "{filePath}/DSA_Intro_3.md"
  ],
  "test": [
    "{filePath}/DSA_Intro_1.json",
    "{filePath}/DSA_Intro_2.json",
    "{filePath}/DSA_Intro_3.json"
  ],
  "bookmark": true,
  "completed": true
}
```

---

### 3.2. Learn Page 2
> NOTHING

### 3.3. Learn Page 2.5

#### 3.3.1. Text Chat Endpoint for Learn
- **Method:** POST
- **URL:** `/api/learn/text-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "courseChapterData": """...""" },
  "user": "User message",
  "conversationHistory": [
    { "speaker": "user", "text": "User speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

#### 3.3.2. Voice Chat Endpoint for Learn
- **Method:** POST
- **URL:** `/api/learn/voice-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "courseChapterData": """...""" },
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "user": "Transcribed user speech",
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

---

### 3.4. Learn Page 3

#### 3.4.1. End Course Endpoint
- **Method:** POST
- **URL:** `/api/learn/end-course`
- **Input:**
```json
{
  "courseId": "DSA_Intro",
  "testResults": {
    "{filePath}/DSA_Intro_1.json": { "score": "100/150", "timeTaken": "300" },
    "{filePath}/DSA_Intro_2.json": { "score": "100/150", "timeTaken": "300" },
    "{filePath}/DSA_Intro_3.json": { "score": "100/150", "timeTaken": "300" }
  }
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

---

### 3.5. Learn Page 3.5 – Mentor Help

#### 3.5.1. Text Chat for Mentor Help
- **Method:** POST
- **URL:** `/api/learn/mentor-help/text-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "codingQAData": """...""" },
  "user": "User message",
  "conversationHistory": [
    { "speaker": "user", "text": "User message" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

#### 3.4.2. Voice Chat for Mentor Help
- **Method:** POST
- **URL:** `/api/learn/mentor-help/voice-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "mcqData": """...""" },
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "user": "Transcribed user speech",
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

---

## 4. Practice Section

### 4.1. Practice Page 1

#### 4.1.1. Get Practice Recommendations & Filters
- **Method:** GET
- **URL:** `/api/practice/recommendations`
- **Input:** None
- **Output:**
```json
{
  "mcqRecommendations": [
    { "id": "1", "practiceName": "Queues" },
    { "id": "2", "practiceName": "Trees" },
    { "id": "3", "practiceName": "Linked Lists" }
  ],
  "codingRecommendations": [
    { "id": "1", "practiceName": "Queues" },
    { "id": "2", "practiceName": "Trees" },
    { "id": "3", "practiceName": "Linked Lists" }
  ],
  "filters": {
    "mcqs": {
      "level": ["Easy", "Medium", "Hard"],
      "topic": ["Queues", "Trees", "Linked Lists"],
      "status": [true, false]
    },
    "codingQuestions": {
      "level": ["Easy", "Medium", "Hard"],
      "topic": ["Queues", "Trees", "Linked Lists"],
      "status": [true, false]
    }
  }
}
```

#### 4.1.2. Get All Practice Items (with filters)
- **Method:** GET
- **URL:** `/api/practice/items`
- **Input:** (Query Parameters)
```json
{
  "type": "string",
  "level": "Optional[string]",
  "status": "Optional[boolean]",
  "topic": "Optional[string]"
}
```
- **Output:**
```json
[
  { "id": "1", "practiceName": "Queues", "status": true, "difficulty": "easy" },
  { "id": "2", "practiceName": "Trees", "status": true, "difficulty": "easy" },
  { "id": "3", "practiceName": "Linked Lists", "status": true, "difficulty": "easy" }
]
```

#### 4.1.3. Get MCQ Test File
- **Method:** GET
- **URL:** `/api/practice/mcq/{testId}`
- **Input:** URL Parameter: `testId`
- **Output:**
```json
{
  "testFile": "{filePath}/Programming_Fundamentals_000001.json"
}
```

---

### 4.2. Practice Page 2 – Coding Problem

#### 4.2.1. Get Coding Problem
- **Method:** GET
- **URL:** `/api/practice/coding-problem/{problemId}`
- **Input:** URL Parameter: `problemId`
- **Output:**
```json
{
  "problemDescription": "{filePath}/Concatenation_of_Array.md",
  "problemSolution": "{filePath}/Concatenation_of_Array_solution.py",
  "testCases": [
    ["1 2 1", "[1, 2, 1, 1, 2, 1]"],
    ["1 3 2 1", "[1, 3, 2, 1, 1, 3, 2, 1]"],
    ["5 6", "[5, 6, 5, 6]"],
    ["9", "[9, 9]"]
  ]
}
```

---

### 4.3. Practice Page 3 – Submit Practice
- **Method:** POST
- **URL:** `/api/practice/submit`
- **Input:**
```json
{
  "courseId": "23klj4",
  "score": "10/10"
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

---

### 4.4. Practice Page 3.5 – Mentor Help

#### 4.4.1. Text Chat for Mentor Help
- **Method:** POST
- **URL:** `/api/practice/mentor-help/text-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "codingQAData": """...""" },
  "user": "User message",
  "conversationHistory": [
    { "speaker": "user", "text": "User message" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

#### 4.4.2. Voice Chat for Mentor Help
- **Method:** POST
- **URL:** `/api/practice/mentor-help/voice-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "codingQAData": """...""" },
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "user": "Transcribed user speech",
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

---

### 4.5. Practice Page 4 – End Practice
- **Method:** POST
- **URL:** `/api/practice/end`
- **Input:**
```json
{
  "courseId": "DSA_Intro",
  "score": "100/150"
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

---

### 4.6. Practice Page 4.5 – Mentor Help (MCQs)
#### 4.6.1. Text Chat for Mentor Help on MCQs
- **Method:** POST
- **URL:** `/api/practice/mentor-help/mcqs/text-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "mcqsData": """...""" },
  "user": "User message",
  "conversationHistory": [
    { "speaker": "user", "text": "User message" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

#### 4.6.2. Voice Chat for Mentor Help on MCQs
- **Method:** POST
- **URL:** `/api/practice/mentor-help/mcqs/voice-chat`
- **Input:**
```json
{
  "socraticAI": true,
  "additionalInfo": { "mcqsData": """...""" },
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "user": "Transcribed user speech",
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

---

## 5. Interview Simulation Section

### 5.1. Interview Simulation Page 1

#### 5.1.1. Get Interview Filters
- **Method:** GET
- **URL:** `/api/interview/filters`
- **Input:** None
- **Output:**
```json
{
  "interviewType": ["HR", "TR"],
  "level": ["Easy", "Medium", "Hard"],
  "topic": ["Linked_List", "Trees", "Stacks", "Queues", "Arrays", "Strings"]
}
```

#### 5.1.2. Start Interview (Upload Resume and Data)
- **Method:** POST
- **URL:** `/api/interview/start`
- **Input:**
```json
{
  "resumeFile": "/path/to/resume.pdf",
  "InterviewType": "str", 
  "Level": "str", 
  "JobDescriptions": "str", 
  "Topics": ["str", "str"],
  "OthersData": "Optional[string]" 
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

#### 5.1.3. View Previous Interview Results
- **Method:** GET
- **URL:** `/api/interview/results`
- **Input:** None
- **Output:**
```json
[
  {
    "date": "dd-mm-yyyy",
    "result": "good",
    "review": "Detailed review text"
  },
  {
    "date": "dd-mm-yyyy",
    "result": "good",
    "review": "Detailed review text"
  },
  {
    "date": "dd-mm-yyyy",
    "result": "good",
    "review": "Detailed review text"
  }
]
```

### 5.2. Interview Simulation Page 2

#### 5.2.1. Voice Chat for Interview
- **Method:** POST
- **URL:** `/api/interview/voice-chat`
- **Input:**
```json
{
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "responseAudio": "/path/to/response_audio.mp3",
  "user": "Transcribed user speech",
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

#### 5.2.2. End Interview
- **Method:** POST
- **URL:** `/api/interview/end`
- **Input:**
```json
{
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "result": "good",
  "review": "Detailed feedback"
}
```

---

## 6. Chat Page

### 6.1. Text Chat Endpoint
- **Method:** POST
- **URL:** `/api/chat/text`
- **Input:**
```json
{
  "socraticAI": true,
  "user": "User text",
  "conversationHistory": [
    { "speaker": "user", "text": "User speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

### 6.2. Voice Chat Endpoint
- **Method:** POST
- **URL:** `/api/chat/voice`
- **Input:**
```json
{
  "socraticAI": true,
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "user": "Transcribed user speech",
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

---

## 7. Resume Optimization Page

### 7.1. Analyze Job Match
- **Method:** POST
- **URL:** `/api/resume/analysis`
- **Input:**
```json
{
  "jobDescription": """Detailed job description text..."""
}
```
- **Output:**
```json
{
  "match": "Good",
  "skillGapAnalysis": """Analysis details...""",
  "salaryInsights": """Insights details...""",
  "linkedinPeople": [
    {"name": "person_1", "url": "URL OF THE PERSON"},
    {"name": "person_2", "url": "URL OF THE PERSON"},
    {"name": "person_3", "url": "URL OF THE PERSON"}
  ]
}
```

### 7.2. Generate Cover Letter
- **Method:** POST
- **URL:** `/api/resume/generate-cover-letter`
- **Input:**
```json
{
  "jobDescription": """Detailed job description text..."""
}
```
- **Output:**
```json
{
  "coverLetter": "File Path to cover letter.txt"
}
```

### 7.3. Generate Talore Resume
- **Method:** POST
- **URL:** `/api/resume/generate-talore`
- **Input:**
```json
{
  "jobDescription": """Detailed job description text..."""
}
```
- **Output:**
```json
{
  "pdfFile": "/path/to/generated_resume.pdf"
}
```

### 7.4. Chat for Cover Letter
- **Method:** POST
- **URL:** `/api/resume/cover-letter-chat`
- **Input:**
```json
{
  "jobDescription": """Detailed job description text...""",
  "coverLetter": "Initial File Path to cover letter.txt",
  "userMessage": "Optional message from user"
}
```
- **Output:**
```json
{
  "coverLetter": "Updated File Path to cover letter.txt"
}
```

### 7.5. Chat for Talore Resume
- **Method:** POST
- **URL:** `/api/resume/talore-chat`
- **Input:**
```json
{
  "jobDescription": """Detailed job description text...""",
  "pdfFile": "/path/to/resume.pdf",
  "userMessage": "Optional message from user"
}
```
- **Output:**
```json
{
  "pdfFile": "/path/to/updated_resume.pdf"
}
```

### 7.6. View Previous Cover Letter Results
- **Method:** GET
- **URL:** `/api/resume/previous-cover-letters`
- **Input:** None
- **Output:**
```json
[
  {
    "date": "dd-mm-yyyy",
    "result": "cover letter.txt"
  },
  {
    "date": "dd-mm-yyyy",
    "result": "cover letter.txt"
  },
  {
    "date": "dd-mm-yyyy",
    "result": "cover letter.txt"
  }
]
```

---

## 8. Job Tracker

### 8.1. Job Tracker Page 1

#### 8.1.1. Render Job Tracker Page
- **Method:** GET
- **URL:** `/api/jobs`
- **Input:** None
- **Output:**
```json
[
  {
    "id": "job_id_1",
    "title": "Job Title 1",
    "status": "In Progress",
    "deadlineDate": "dd-mm-yyyy",
    "description": """Job description..."""
  },
  {
    "id": "job_id_2",
    "title": "Job Title 2",
    "status": "Completed",
    "deadlineDate": "dd-mm-yyyy",
    "description": """Job description..."""
  }
]
```

#### 8.1.2. Edit a Job Event
- **Method:** PUT
- **URL:** `/api/jobs`
- **Input:**
```json
[
  {
    "id": "job_id_1",
    "title": "Job Title 1",
    "status": "Updated Status",
    "deadlineDate": "dd-mm-yyyy",
    "description": "Updated description..."
  }
]
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

#### 8.1.3. Delete a Job Event
- **Method:** DELETE
- **URL:** `/api/jobs`
- **Input:**
```json
{
  "id": "job_id_1"
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

### 8.2. Job Tracker Page 1.5

#### 8.2.1. Text Chat Mentor Help
- **Method:** POST
- **URL:** `/api/jobs/mentor-help/text-chat`
- **Input:**
```json
{
  "additionalInfo": { "nearTasks": """...""" },
  "user": "User message",
  "conversationHistory": [
    { "speaker": "user", "text": "User message" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

#### 8.2.2. Voice Chat Mentor Help
- **Method:** POST
- **URL:** `/api/jobs/mentor-help/voice-chat`
- **Input:**
```json
{
  "additionalInfo": { "nearTasks": """...""" },
  "audioFile": "/path/to/audio_file.mp3",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```
- **Output:**
```json
{
  "user": "Transcribed user speech",
  "ai": "AI's text response",
  "conversationHistory": [
    { "speaker": "user", "text": "Transcribed user speech" },
    { "speaker": "ai", "text": "AI's text response" }
  ]
}
```

---

## 9. Saved Pages

### 9.1. Get Saved Page Filters
- **Method:** GET
- **URL:** `/api/saved/filters`
- **Input:** None
- **Output:**
```json
{
  "type": ["Course", "MCQ", "Coding"]
}
```

### 9.2. Get Saved Course IDs
- **Method:** GET
- **URL:** `/api/saved/courses`
- **Input:** (Query Parameter)
```json
{
  "type": "Course"
}
```
- **Output:**
```json
[
  "id_1",
  "id_2",
  "id_3"
]
```

---


## 10. Settings

### 10.1. Change Password
- **Method:** PUT
- **URL:** `/api/settings/change-password`
- **Input:**
```json
{
  "OldPassword": "Old_password_here",
  "newPassword": "new_password_here"
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

### 10.2. Change Username
- **Method:** PUT
- **URL:** `/api/settings/change-username`
- **Input:**
```json
{
  "OldUsername": "Old_username_here",
  "newUsername": "new_username_here"
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

### 10.3. Reset Progress
- **Method:** POST
- **URL:** `/api/settings/reset-progress`
- **Input:**
```json
{
  "Password": "password_here",
}
```
- **Output:**
```json
{
  "acknowledgement": true
}
```

---