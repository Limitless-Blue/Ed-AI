import json
import os


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


# Example of updating an existing job:
new_data = {
    "id": "job_id_3",
    "title": "Senior Project Manager",
    "status": "In Progress",
}
print(edit_job_event_data(new_data))  # This will add the new job
