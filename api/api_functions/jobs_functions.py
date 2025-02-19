import json
import os
import google.generativeai as genai
import speech_recognition as sr
import subprocess
from pydub import AudioSegment
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")


def generate_ai_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


def get_all_job_tracker_board_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = "Database/Redirection/job_tracker_board_database.json"
    file_path = os.path.join(base_dir, json_file_path)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        output_list = []

        for item in data:
            extracted_data = {
                "id": item.get("id"),
                "title": item.get("title"),
                "status": item.get("status"),
                "deadlineDate": item.get("deadlineDate"),
                "description": item.get("description"),
            }
            output_list.append(extracted_data)

        print(json.dumps(output_list, indent=4))

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def edit_job_event_data(new_data):
    file_path = "Database/Redirection/job_tracker_board_database.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)
    try:
        if not os.path.exists(json_file_path):
            print(f"Error: File not found at {json_file_path}")
            return

        with open(json_file_path, "r") as f:
            job_data = json.load(f)

        job_found = False

        for job in job_data:
            if job["id"] == new_data.get("id"):
                job_found = True
                for key, value in new_data.items():
                    if key in job:
                        job[key] = value
                break

        if not job_found:
            new_job = {
                "id": None,
                "title": None,
                "status": None,
                "deadlineDate": None,
                "description": None,
            }

            for key, value in new_data.items():
                if key in new_job:
                    new_job[key] = value

            job_data.append(new_job)

        with open(json_file_path, "w") as f:
            json.dump(job_data, f, indent=4)

        return {"acknowledgement": True}

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete_job_event_data(id: str):
    file_path = "Database\\Redirection\\job_tracker_board_database.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)

        updated_data = [event for event in data if event.get("id") != id]

        if len(data) != len(updated_data):
            with open(json_file_path, "w") as f:
                json.dump(updated_data, f, indent=4)
            return {"acknowledgement": True}
        else:
            return {"acknowledgement": False}

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return {"acknowledgement": False}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return {"acknowledgement": False}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"acknowledgement": False}


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


def jobs_mentor_text_chat_response(user_input, conversationHistory, additionalInfo):
    generate_ai_response_prompt = f"""Answer the user's question about tasks, questions, and jobs using the provided additional information. If no additional information is provided, ignore it and answer the user's question directly.  Be as detailed as possible. NOTE: Answer directly to the user's question wihtout any additional information.

    User Question: {user_input}

    Additional Information: {additionalInfo if additionalInfo else "None"}"""

    response = generate_ai_response(generate_ai_response_prompt)
    conversationHistory.append({"speaker": "user", "text": user_input})
    conversationHistory.append({"speaker": "AI", "text": response})
    return {
        "AI": response,
        "conversationHistory": conversationHistory,
    }


def jobs_mentor_voice_chat_response(audioFile, conversationHistory, additionalInfo):
    user_input = transcribe_audio(audioFile)
    response_data = jobs_mentor_text_chat_response(
        user_input, conversationHistory, additionalInfo
    )
    return {
        "user": user_input,
        "AI": response_data["AI"],
        "conversationHistory": response_data["conversationHistory"],
    }
