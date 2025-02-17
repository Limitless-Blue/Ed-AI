from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json


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
