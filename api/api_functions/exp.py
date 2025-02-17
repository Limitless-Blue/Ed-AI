import json
import os


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


json_file_path = "Database\\Redirection\\job_tracker_board_database.json"

result = delete_job_event_data("job_id_3")  # Delete job_id_3
print(result)

result = delete_job_event_data("job_id_6")  # Delete job_id_6 (not found)
print(result)
