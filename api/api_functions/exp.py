import os
import json


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


# Example usage:
saved_ids = retrive_Coding_ids()
print(saved_ids)
