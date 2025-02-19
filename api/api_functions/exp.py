import json
import os
from datetime import datetime


def add_new_result(new_result_data):
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


new_result = {
    "result": "Excellent",
    "review": "Candidate demonstrated strong problem-solving skills.",
}
add_new_result(new_result)
