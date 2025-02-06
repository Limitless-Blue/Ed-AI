# later:

## Sign up Page:
<!-- Are there any api endopints -->

## Sign Up Form Page:
<!-- Are there any api endopints -->

## Sign Up Coding Page:
<!-- Are there any api endopints -->

## Sign Up MCQs Page:
<!-- Are there any api endopints -->

## Sign Up Chat Page:
- Mentor Help:
    >???

## Sign Up Welcome Loading:
<!-- Are there any api endopints -->

## LogIn Page:
<!-- Are there any api endopints -->


# Current:

## Common API:
- Default Login Data:
    - Streak Data
        """
            {
            "streak": 1,
            "streakData": [
                {"date": "01-01-2024", "status": true},
                {"date": "02-01-2024", "status": false},
                {"date": "03-01-2024", "status": true},
                {"date": "04-01-2024", "status": true},
                {"date": "05-01-2024", "status": false},
                {"date": "06-01-2024", "status": true}
            ]
            }
        """
    - Greeting Audio:
        """
            "Audio": "Audio File path"
        """
    - User Details:
        """
            "First Name": "Katoro"
            "Last Name": "kamado"
            "Image": "image File path"
        """

- save:
    INPUT: Id, True
    OUTPUT: Acknowledgement

## Landing Page:
- Voice Chat Api end points:
    """
        INPUT:
            {
            "audio_file": "base64 encoded audio data",
            "conversation_history": [ 
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }


        OUTPUT:
            {
                "response_audio": "base64 encoded audio data",
                "conversation_history": [
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }
    """

## Learn Page 1:
- Rendering recomedations and filters api endpoint:
    RECOMENDATIONS: 
    INPUT: NULL
    OUPUT: 
      {
        "recommendations": {
          {"ID": "1", "course_name": "Math"},
          {"ID": "2", "course_name": "Science"},
          {"ID": "3", "course_name": "English"}
        },
        "filters": {
          "level": ["Primary", "Secondary", "Tertiary"],
          "topic": ["Math", "Science", "English"],
          "status": ["True", "False"]
        }
      }

- Rendering all courses api endpoint:
    INPUT:
        {
        "level": "Optional[str]", 
        "Status": "Optional[bool]", 
        "Topic": "Optional[str]"
        }
    OUTPUT:
        [
            {"ID": "1", "course_name": "Math"},
            {"ID": "2", "course_name": "Science"},
            {"ID": "3", "course_name": "English"}
        ]

- Course Api Endpoints:
    INPUT: COURSE_ID
    OUTPUT:
        {
            "Course": [
                "{file_path}/DSA Intro_1.md",
                "{file_path}/DSA Intro_2.md",
                "{file_path}/DSA Intro_3.md"
            ],
            "Test": [
                "{file_path}/DSA Intro_1.json",
                "{file_path}/DSA Intro_2.json",
                "{file_path}/DSA Intro_.json"
            ]
            "Book_mark": True,
            "Completed": True
        }

## Learn Page 2:
<!-- NOTHING -->

## Learn Page 2.5:
- text Chat Api end points:
    """
        INPUT:
            {
            "socratic AI": bool,
            "Additional Info": {Course data},
            "user": "user speech",
            "conversation_history": [ 
                    {"speaker": "user", "text": "user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }


        OUTPUT:
            {
            "ai": "AI's text response",

                "conversation_history": [
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }
    """

- Voice Chat Api end points:
    """
        INPUT:
            {
            "socratic AI": bool,
            "Additional Info": {Course data},
            "audio_file": "base64 encoded audio data",
            "conversation_history": [ 
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }


        OUTPUT:
            {
            "user": "Transcribed user speech",
            "ai": "AI's text response",

                "conversation_history": [
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }
    """

## Learn Page 3:
- End Button of the course api endpoint:
    INPUT: NULL
    OUTPUT:
        COURSE_ID: "DSA Intro"
        "Test_results": [
            "{file_path}/DSA Intro_1.json": {"score":"100/150", "time_taken": "300"},
            "{file_path}/DSA Intro_2.json": {"score":"100/150", "time_taken": "300"},
            "{file_path}/DSA Intro_3.json": {"score":"100/150", "time_taken": "300"}
        ]

## Learn Page 3.5:
- Mentor Help:
    - text Chat Api end points:
        """
            INPUT:
                {
                "socratic AI": bool,
                "Additional Info": {MCQ data},
                "user": "user speech",
                "conversation_history": [ 
                        {"speaker": "user", "text": "user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

    - Voice Chat Api end points:
        """
            INPUT:
                {
                "socratic AI": bool,
                "Additional Info": {MCQ data},
                "audio_file": "base64 encoded audio data",
                "conversation_history": [ 
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "user": "Transcribed user speech",
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

## Practice Page 1:
- Rendering recomedations and filters api endpoint:
    RECOMENDATIONS: 
    INPUT: NULL
    OUPUT: 
      {
        "mcq_recommendations": [
          {"ID": "1", "Practice_name": "Math"},
          {"ID": "2", "Practice_name": "Science"},
          {"ID": "3", "Practice_name": "English"}
        ],
        "coding_recommendations": [
          {"ID": "1", "Practice_name": "Math"},
          {"ID": "2", "Practice_name": "Science"},
          {"ID": "3", "Practice_name": "English"}
        ],
        "filters": {
          "mcqs": {
            "level": ["Primary", "Secondary", "Tertiary"],
            "topic": ["Math", "Science", "English"],
            "status": ["True", "False"]
          },
          "coding_questions": {
            "level": ["Primary", "Secondary", "Tertiary"],
            "topic": ["Math", "Science", "English"],
            "status": ["True", "False"]
          }
        }
      }
    }

- Rendering all Practice api endpoint:
    INPUT:
        {
        "type": "str",
        "level": "Optional[str]", 
        "Status": "Optional[bool]", 
        "Topic": "Optional[str]"
        }
    OUTPUT:
        [
            {"ID": "1", "Practice_name": "Math", "status":"completed", "difficulty": "Primary" },
            {"ID": "2", "Practice_name": "Science", "status":"completed", "difficulty": "Primary" },
            {"ID": "3", "Practice_name": "English", "status":"completed", "difficulty": "Primary" },
        ]

- Mcq api endpoint:
    INPUT: TEST ID
    OUTPUT:
    {
        "Test_file": "{FILE_PATH}/Programming_Fundamentals_000001.json"
    }



## Practice Page 2:
- Coding_problem api endpoint:
    INPUT: Coding_problem_ID
    OUPUT:
        {
            "Problem_Description": "{FILE_PATH}/Concatenation_of_Array.md",
            "Problem_Solution": "{FILE_PATH}/Concatenation_of_Array_solution.py",
            "Test_Cases": [
                ["1 2 1", "[1, 2, 1, 1, 2, 1]"],
                ["1 3 2 1", "[1, 3, 2, 1, 1, 3, 2, 1]"],
                ["5 6", "[5, 6, 5, 6]"],
                ["9", "[9, 9]"]
            ]
        },

## Practice Page 3:
- submit button api endpoint:
    INPUT: NULL
    OUTPUT:
        COURSE_ID: "23klj4"
        {
            "score": "10/10"
        }

## Practice Page 3.5:
- Mentor Help:
    - text Chat Api end points:
        """
            INPUT:
                {
                "socratic AI": bool,
                "Additional Info": {coding question and answer data},
                "user": "user speech",
                "conversation_history": [ 
                        {"speaker": "user", "text": "user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

    - Voice Chat Api end points:
        """
            INPUT:
                {
                "socratic AI": bool,
                "Additional Info": {coding question and answer data},
                "audio_file": "base64 encoded audio data",
                "conversation_history": [ 
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "user": "Transcribed user speech",
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

## Practice Page 4:
- end button api endpoint:
    INPUT: NULL
    OUTPUT:
        COURSE_ID: "DSA Intro"
        {
            "score": "100/150"
        }

## Practice Page 4.5:
- Mentor Help:
    - text Chat Api end points:
        """
            INPUT:
                {
                "socratic AI": bool,
                "Additional Info": {MCQs data},
                "user": "user speech",
                "conversation_history": [ 
                        {"speaker": "user", "text": "user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

    - Voice Chat Api end points:
        """
            INPUT:
                {
                "socratic AI": bool,
                "Additional Info": {MCQs data},
                "audio_file": "base64 encoded audio data",
                "conversation_history": [ 
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "user": "Transcribed user speech",
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

## Interview Simulation Page 1:
- Rendering filters api endpoint:
    INPUT: NULL
    OUPUT: 
        {
          "interview_type": ["HR", "TR"],
          "level": ["Primary", "Secondary", "Tertiary"],
          "topic": ["Math", "Science", "English"]
        }


- lets start interview button:
    INPUT: pdf of resume, other data
    OUPUT: acknowledgement

- View Previous Results:
    INPUT: NULL
    OUTPUT:
    {
    {"date": {
        "result": "good",
        "Review": "str"
        }
    },
    {"date": {
        "result": "good",
        "Review": "str"
        }
    },
    {"date": {
        "result": "good",
        "Review": "str"
        }
    },

    }

## Interview Simulation Page 2:
- Voice Chat Api end points:
    """
        INPUT:
            {
            "audio_file": "base64 encoded audio data",
            "conversation_history": [ 
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }


        OUTPUT:
            {
              "response_audio": "base64 encoded audio data",
              
              "user": "Transcribed user speech",
              "ai": "AI's text response",

                "conversation_history": [
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }
    """

- End Interview end points:
    INPUT:             
        "conversation_history": [ 
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
    OUTPUT: 
        {
            "result": "good",
            "Review": "str"
        }

## Chat Page:
- text Chat Api end points:
    """
        INPUT:
            {
            "socratic AI": bool,
            "user": "user text",
            "conversation_history": [ 
                    {"speaker": "user", "text": "user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }


        OUTPUT:
            {
              "ai": "AI's text response",

                "conversation_history": [
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }
    """

- Voice Chat Api end points:
    """
        INPUT:
            {
            "socratic AI": bool,
            "audio_file": "base64 encoded audio data",
            "conversation_history": [ 
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }


        OUTPUT:
            {
              "user": "Transcribed user speech",
              "ai": "AI's text response",

                "conversation_history": [
                    {"speaker": "user", "text": "Transcribed user speech"},
                    {"speaker": "ai", "text": "AI's text response"},
                ]
            }
    """


## Resume Optimization Page:
- Analyze the Job Match api end point:
    INPUT: Job_Description
    OUTPUT:
        {
            "Match": "Good"
            "Skill_Gap_Analysis": "str"
            "Salary_Insights": "str"
            "Linkedin people": ["person_1","person_2","person_3"]
        }

- genrate Cover letter End points
    INPUT: Job_Description
    OUTPUT:
        {
            "Cover Letter": "str"
        }

- Generate Talore reusme End points
    INPUT: Job_Description
    OUTPUT:
        {
            pdf file
        }

- genrate Cover letter chat End points
    INPUT: "Job_Description", "Cover letter", "User Message"[optional]
    OUTPUT:
        {
            "Cover Letter": "str"
        }

- Generate Talore reusme chat End points
    INPUT: "Job_Description", pdf file, "User Message" [optional]
    OUTPUT:
        {
            pdf file
        }

- View Previous Cover letter Results:
    INPUT: NULL
    OUTPUT:
    {
        {"date": {
            "result": "CV letter"
            }
        },
        {"date": {
            "result": "CV letter"
            }
        },
        {"date": {
            "result": "CV letter"
            }
        }
    }

## Job Tracker Page 1:
- Render the page:
    INPUT: Null
    OUTPUT:
    [
        {
            "ID" : "str",
            "Title" : "str",
            "status" : "str",
            "deadline_date" : "dd-mm-yyyy",
            "description" : "str"
        },
        {
            "ID" : "str",
            "Title" : "str",
            "status" : "str",
            "deadline_date" : "dd-mm-yyyy",
            "description" : "str"
        }
    ]

- Edit the event end points:
    INPUT:
    [
        {
        "id" : "str",
        "Title" : "str",
        "status" : "str",
        "deadline_date" : "dd-mm-yyyy",
        "description" : "str"
        }
    ]

    OUTPUT:
    acknowledgement

- Delete Button:
    INPUT:
    {
    "id" : "str",
    }

    OUTPUT:
    acknowledgement

## Job Tracker Page 1.5:
- Mentor Help:
    - text Chat Api end points:
        """
            INPUT:
                {
                "Additional Info": {near tasks},
                "user": "user speech",
                "conversation_history": [ 
                        {"speaker": "user", "text": "user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

    - Voice Chat Api end points:
        """
            INPUT:
                {
                "Additional Info": {near tasks},
                "audio_file": "base64 encoded audio data",
                "conversation_history": [ 
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }


            OUTPUT:
                {
                "user": "Transcribed user speech",
                "ai": "AI's text response",

                    "conversation_history": [
                        {"speaker": "user", "text": "Transcribed user speech"},
                        {"speaker": "ai", "text": "AI's text response"},
                    ]
                }
        """

## Saved Pages:
- filters api endpoint:
    INPUT: NULL
    OUPUT: 
      {
            "Type": ["Course", "MCQ", "Coding"],
      }

- Saved course:
    INPUT: TYPE
    OUTPUT: ["id_1," "id_2", "id_3"]

## Settings Page:
- Change password API Endpoint:
  Change password:
  INPUT: "Changed password"
  OUTPUT: acknowledgement

- Change username API Endpoint:
  Change username:
  INPUT: "Changed username"
  OUTPUT: acknowledgement

- reset Progress API Endpoint:
  reset Progress:
  INPUT: NULL
  OUTPUT: acknowledgement

