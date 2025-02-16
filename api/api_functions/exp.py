import json
import os


def save_bookmark_for_Coding_problems_page(id_to_update, new_saved_status):
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        file_path = os.path.join(
            base_dir,
            "Database/Redirection/Redirecting_Coding_Problem_(dynamic_version).json",
        )

        with open(file_path, "r+") as f:
            data = json.load(f)

            item = data["problems"].get(id_to_update)

            if item:
                item["Saved"] = new_saved_status

                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
                return True
            else:
                return False

    except FileNotFoundError:
        print("Error: JSON file not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


if save_bookmark_for_Coding_problems_page("COPA_1", True):
    print(f"Saved status for ID 'COPA_1' updated successfully.")
else:
    print(f"Failed to update saved status for ID 'COPA_1'.")
