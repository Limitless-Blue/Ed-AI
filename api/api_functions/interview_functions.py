from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import shutil
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from pydub.effects import speedup
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))


def generate_ai_response(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
    response = model.generate_content(prompt)
    return response.text.strip()


def increase_playback_speed_no_pitch(input_file, output_file, speed_factor=1.3):
    sound = AudioSegment.from_mp3(input_file)
    new_sound = speedup(sound, playback_speed=speed_factor)
    new_sound.export(output_file, format="mp3")


def update_Current_Interview(
    resumeFile: str,
    InterviewType: str,
    Level: str,
    JobDescriptions: str,
    Topics: List[str],
    OthersData: Optional[str] = None,
):
    file_path = "Database\\Redirection\\Interview_simulation.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)

        data["Current_Interview"]["resumeFile"] = resumeFile
        data["Current_Interview"]["InterviewType"] = InterviewType
        data["Current_Interview"]["Level"] = Level
        data["Current_Interview"]["JobDescriptions"] = JobDescriptions
        data["Current_Interview"]["Topics"] = Topics
        data["Current_Interview"]["OthersData"] = (
            OthersData if OthersData is not None else ""
        )

        with open(json_file_path, "w") as f:
            json.dump(data, f, indent=4)

        DATA_PATH = "Database\\AI_Database\\RAG_Database"
        CHROMA_PATH = "Database\\AI_Database\\Vector_Database"
        load_and_store_pdfs_in_chroma(DATA_PATH, CHROMA_PATH)

        return {"acknowledgement": True}

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return {"acknowledgement": False, "error": "File not found"}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return {"acknowledgement": False, "error": "Invalid JSON"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"acknowledgement": False, "error": str(e)}


def get_previous_results():
    file_path = "Database\\Redirection\\Interview_simulation.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data.get("Previous_Results")
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def add_new_result_interview(new_result_data):
    json_file_path = "Database\\Redirection\\Interview_simulation.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, json_file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON format in file: {file_path}")

    if "Previous_Results" not in data:
        raise KeyError("The JSON file must contain a 'Previous_Results' key.")

    today = datetime.now().strftime("%d-%m-%Y")

    new_entry = {
        "date": today,
        "result": new_result_data.get("result"),
        "review": new_result_data.get("review"),
    }

    data["Previous_Results"].append(new_entry)

    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def load_and_store_pdfs_in_chroma(
    data_path, chroma_path, collection_name="psychologist"
):
    delete_files_and_subfolders(chroma_path)

    if not os.path.exists(chroma_path):
        os.makedirs(chroma_path)

    os.chmod(chroma_path, 0o777)

    chroma_client = chromadb.PersistentClient(path=chroma_path)

    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        print("No existing collection to delete.")
    collection = chroma_client.get_or_create_collection(name=collection_name)

    loader = PyPDFDirectoryLoader(data_path)
    raw_documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(raw_documents)

    documents = [chunk.page_content for chunk in chunks]
    ids = [f"ID{i}" for i, _ in enumerate(chunks)]
    metadata = [chunk.metadata for chunk in chunks]

    collection.upsert(
        documents=documents,
        metadatas=metadata,
        ids=ids,
    )

    print("Data successfully added to ChromaDB.")


def delete_files_and_subfolders(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    try:
        shutil.rmtree(folder_path)
        print(f"Deleted: {folder_path} and all its contents.")
    except Exception as e:
        print(f"Error deleting {folder_path}: {e}")


def get_current_interview_details():
    json_file_path = "Database\\Redirection\\Interview_simulation.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, json_file_path)

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            current_interview = data.get("Current_Interview")
            if current_interview:
                current_interview.pop("resumeFile", None)
                return current_interview
            else:
                return None
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def interview_voice_chat_reply(audioFile, conversationHistory):
    current_details = get_current_interview_details()
    if current_details is None:
        current_details = {
            "InterviewType": "General",
            "Level": "Beginner",
            "Topics": [],
        }

    file_ext = os.path.splitext(audioFile)[1].lower()
    wav_file = audioFile
    if file_ext != ".wav":
        try:
            wav_file = "temp_converted.wav"
            sound = AudioSegment.from_file(audioFile)
            sound.export(wav_file, format="wav")
        except Exception as e:
            print(f"Error converting audio file to WAV: {e}")
            return {"acknowledgement": False, "error": "Audio conversion failed."}

    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
        transcribed_text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        transcribed_text = "Could not understand audio."
    except sr.RequestError as e:
        transcribed_text = f"Error in speech recognition: {e}"
    except Exception as e:
        transcribed_text = f"Unexpected error: {e}"

    if file_ext != ".wav" and os.path.exists(wav_file):
        os.remove(wav_file)

    context = ""
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        chroma_path = os.path.join(base_dir, "Database\\AI_Database\\Vector_Database")
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        collection = chroma_client.get_or_create_collection(name="psychologist")
        query_result = collection.query(query_texts=[transcribed_text], n_results=1)
        if (
            query_result
            and "documents" in query_result
            and len(query_result["documents"]) > 0
            and len(query_result["documents"][0]) > 0
        ):
            context = query_result["documents"][0][0]
    except Exception as e:
        print(f"Error during RAG query: {e}")
        context = ""

    generate_ai_response_input = f"""Your name is Gojo. You are conducting a job interview. Act as a professional and natural interviewer.  Base your responses on the following information:

        * **Current Interview Details:** {current_details}
        * **Candidate Background (retrieved using RAG):** {context}
        * **Previous Conversation History:** {conversationHistory}

    Maintain a consistent interviewer tone throughout the interaction. Focus on asking insightful follow-up questions that probe deeper into the candidate's qualifications and fit for the role. Guide the conversation smoothly and naturally, as you would in a real interview.

    **Important:** Do not leave any information blank or respond with placeholder text. If the provided context or conversation history is insufficient to formulate a relevant and meaningful response.  This response will be sent directly to the user, so avoid unnecessary content."""

    ai_response = generate_ai_response(generate_ai_response_input)

    conversationHistory.append({"speaker": "user", "text": transcribed_text})
    conversationHistory.append({"speaker": "AI", "text": ai_response})

    response_audio_path = os.path.join(
        "API_Endpoint", "Temp_Static_data", "Chat", "Response.mp3"
    )
    try:
        tts = gTTS(text=ai_response, lang="en", slow=False)
        os.makedirs(os.path.dirname(response_audio_path), exist_ok=True)
        tts.save(response_audio_path)
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")
        response_audio_path = ""

    response_speeded_up_output_file = os.path.join(
        "API_Endpoint", "Temp_Static_data", "Chat", "Test_output_speed_up.mp3"
    )

    increase_playback_speed_no_pitch(
        response_audio_path, response_speeded_up_output_file
    )

    return {
        "responseAudio": response_speeded_up_output_file,
        "user": transcribed_text,
        "AI": ai_response,
        "conversationHistory": conversationHistory,
    }


def end_interview_results(conversationHistory):
    """
    This function simulates an AI component that analyzes the conversation history
    from the interview, provides performance feedback, stores the result, and returns
    the feedback data.
    """
    user_texts = [
        entry["text"] for entry in conversationHistory if entry.get("speaker") == "user"
    ]
    if user_texts:
        total_length = sum(len(text) for text in user_texts)
        avg_length = total_length / len(user_texts)
        performance = "good" if avg_length > 30 else "needs improvement"
    else:
        performance = "insufficient data"

    if performance == "good":
        review = "Great job! Your responses were articulate and detailed."
    elif performance == "needs improvement":
        review = (
            "You might consider providing more detailed responses in your interview."
        )
    else:
        review = "Not enough data to evaluate your performance."

    Interview_result_data = {"result": performance, "review": review}
    add_new_result_interview(Interview_result_data)
    return Interview_result_data
