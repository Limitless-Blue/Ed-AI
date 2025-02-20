import json
import os
import sys
from typing import List, Optional, Dict, Any
import google.generativeai as genai
import speech_recognition as sr
import subprocess
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from api.api_functions.common_functions import extract_recommendation_list


def learn_page_recommendations():
    input_ids = extract_recommendation_list("Learn_Page")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(
        base_dir, "Database/Redirection/Redirecting_learn_page_(dynamic_version).json"
    )

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    id_to_course_name = {entry["ID"]: entry["title"] for entry in data}

    recommendations = [
        {
            "id": course_id,
            "courseName": id_to_course_name.get(course_id, "Unknown Course"),
        }
        for course_id in input_ids
    ]

    filters = {
        "level": ["Easy", "Medium", "Hard"],
        "topic": [
            "Advanced Problem Solving",
            "Algorithm Analysis",
            "Array",
            "Control Structures",
            "DSA Basics",
            "Data Structures",
            "Functions",
            "Graph",
            "Hashing",
            "Heap",
            "Linked List",
            "Programming Basics",
            "Problem Solving",
            "Queue",
            "Sorting Algorithms",
            "Stack",
            "Tree",
        ],
        "status": [True, False],
    }

    output = {"recommendations": recommendations, "filters": filters}

    return output


def get_learn_page_data(input_id):
    try:
        current_dir = os.path.dirname(__file__)
        base_dir = os.path.join(current_dir, "..", "..")
        file_path = os.path.join(
            base_dir,
            "Database\\Redirection\\Redirecting_learn_page_(dynamic_version).json",
        )

        with open(file_path, "r") as f:
            data = json.load(f)

    except FileNotFoundError:
        print("Error: JSON file not found.")
        return {}

    for page_data in data:
        try:
            if page_data["ID"] == input_id:
                return {
                    "course": page_data["Course"],
                    "test": page_data["Test"],
                    "bookmark": page_data["Saved"],
                    "completed": page_data["Completed"],
                }
        except KeyError:
            print(f"Warning: Missing 'ID' key in page data: {page_data}")

    return {"message": f"Learn page with ID '{input_id}' not found."}


def get_filtered_learn_courses(
    level: Optional[str] = None,
    status: Optional[bool] = None,
    topic: Optional[str] = None,
):

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(
        base_dir, "Database\\Redirection\\Redirecting_learn_page_(dynamic_version).json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        courses = json.load(file)

    filtered_courses = []
    for course in courses:
        if level and course.get("level") != level:
            continue
        if status is not None and course.get("Completed") != status:
            continue
        if topic and topic not in course.get("topic", []):
            continue

        filtered_courses.append({"id": course["ID"], "courseName": course["title"]})

    return filtered_courses


def generate_ai_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


def check_ffmpeg():
    try:
        subprocess.check_output(["ffmpeg", "-version"])
    except FileNotFoundError:
        print("ffmpeg is not installed or not in your system's PATH.")
        return False
    return True


def convert_mp3_to_wav(mp3_file: str) -> str:
    if check_ffmpeg():
        wav_file = mp3_file.replace(".mp3", ".wav")
        sound = AudioSegment.from_mp3(mp3_file)
        sound.export(wav_file, format="wav")
        return wav_file
    else:
        raise RuntimeError("Cannot convert MP3 to WAV. ffmpeg is required.")


def transcribe_audio(audio_file: str) -> str:
    recognizer = sr.Recognizer()
    if audio_file.endswith(".mp3"):
        audio_file = convert_mp3_to_wav(audio_file)
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"


def side_text_chat_function(
    socraticAI, additionalInfo, user_input, conversationHistory
):
    if socraticAI:
        prompt_input = f"""Answer the following question of user based upon the conversation history, and provide additional information if necessary:
        user: {user_input}
        conversation history: {conversationHistory}
        additional information: {additionalInfo}

        Respond in a Socratic style.  You are a Socratic tutoring assistant. Your goal is to guide the student to the correct solution through questioning, not by giving direct answers. Focus on understanding the student's reasoning and identifying their misconceptions. Be patient and encouraging. If the student's code has issues (like timeouts or incorrect output), use the Socratic method to lead them to discover the problem and its solution. Avoid simply stating the error.

        Here are some examples of Socratic questions you can ask:

        * "Can you walk me through your code step by step, explaining what each part does?"
        * "What are the different types of sorting algorithms you know, and what are their time and space complexities?"
        * "What are the key differences between this test case and the ones that passed?"
        * "Can you analyze the time complexity of the section of your code that handles this specific type of input?"
        * "What are some ways to optimize that section of code?"
        * "What are the potential edge cases for this algorithm?"
        * "Is there another approach you could try?"
        * "How does your algorithm compare to other sorting algorithms in terms of efficiency?"
        * "Let's consider a slightly different input. How would your algorithm handle it?"

        Remember to tailor your questions to the student's responses and the specific problem they are facing. Be concise and avoid jargon unless the student has demonstrated understanding of it. Prioritize understanding the student's thought process.
        """
    else:
        prompt_input = f"""Answer the following question of user based upon the conversation history, and provide additional information if necessary:
        user: {user_input}
        conversation history: {conversationHistory}
        additional information: {additionalInfo}

        Be detailed in your response.
        """

    response_text = generate_ai_response(prompt_input)
    conversationHistory.append({"speaker": "user", "text": user_input})
    conversationHistory.append({"speaker": "AI", "text": response_text})
    return {
        "AI": response_text,
        "conversationHistory": conversationHistory,
    }


def side_voice_chat_function(
    socraticAI, additionalInfo, audioFile, conversationHistory
):
    user_input = transcribe_audio(audioFile)
    response_text = side_text_chat_function(
        socraticAI, additionalInfo, user_input, conversationHistory
    )
    return {
        "user": user_input,
        "AI": response_text["AI"],
        "conversationHistory": response_text["conversationHistory"],
    }
