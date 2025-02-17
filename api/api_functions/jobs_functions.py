import json
import os


def read_and_print_json_data():
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


def edit_job_event_data(
    id: str, title: str, status: str, deadlineDate: str, description: str
):
    pass


def delete_job_event_data(id: str):
    pass
