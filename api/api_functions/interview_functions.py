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
    file_path = "Database\\Redirection\\Interview_simulation.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

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


# TODO: Add AI Part so that it can reply to the user's voice chat and update the conversation history and also the conversation should be based on the interview type, level, and topics...etc.
def interview_voice_chat_reply(audioFile, conversationHistory):
    current_interview_details = get_current_interview_details()
    return {
        "responseAudio": r"API_Endpoint\Temp_Static_data\Chat\Response.mp3",
        "user": "Transcribed user speech",
        "AI": "AI's text response",
        "conversationHistory": [
            {"speaker": "user", "text": "Transcribed user speech"},
            {"speaker": "AI", "text": "AI's text response"},
        ],
    }


# TODO: Add an AI component that provides feedback based on the interview's conversation history, as specified in the output requirements.
def end_interview_results(conversationHistory):
    Interivew_result_data = {"result": "good", "review": "Detailed feedback"}
    add_new_result_interview(Interivew_result_data)
    return Interivew_result_data
