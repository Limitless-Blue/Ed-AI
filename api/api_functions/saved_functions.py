import json
import os


def retrive_Course_ids():
    file_path = "Database\\Redirection\\Redirecting_learn_page_(dynamic_version).json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)

        saved_course_ids = []
        for item in data:
            if item.get("Saved"):
                saved_course_ids.append(item.get("ID"))

        return saved_course_ids

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def retrive_MCQ_ids():
    file_path = "Database\\Redirection\\Redirecting_MCQ_test_(dynamic_version).json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return []

    saved_mcq_ids = []
    for mcq_id, details in data.items():
        if isinstance(details, dict) and details.get("Saved") == True:
            saved_mcq_ids.append(mcq_id)

    return saved_mcq_ids


def retrive_Coding_ids():
    json_file_path = (
        "Database\\Redirection\\Redirecting_Coding_Problem_(dynamic_version).json"
    )
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, json_file_path)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return []

    saved_problems = []
    if "problems" in data:
        for problem_id, problem_data in data["problems"].items():
            if "Saved" in problem_data and problem_data["Saved"]:
                saved_problems.append(problem_id)
    return saved_problems


def retrieve_saved_courses(type):
    if type == "Course":
        return retrive_Course_ids()
    elif type == "MCQ":
        return retrive_MCQ_ids()
    elif type == "Coding":
        return retrive_Coding_ids()
    else:
        return retrive_Course_ids() + retrive_MCQ_ids() + retrive_Coding_ids()
