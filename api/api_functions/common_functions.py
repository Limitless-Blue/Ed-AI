import json
import os


def streak_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    filepath = os.path.join(base_dir, "Database/Redirection/Streak_database.json")

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None


def get_user_website_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, "Database/Redirection/User_data.json")
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        for_website_data = data.get("ForWebsite", {})
        return {
            "username": for_website_data.get("username", ""),
            "password": for_website_data.get("password", ""),
            "profilePicture": for_website_data.get("profilePicture", ""),
        }
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None


def save_bookmark_for_learn_page(id_to_update, new_saved_status):

    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        file_path = os.path.join(
            base_dir,
            "Database/Redirection/Redirecting_learn_page_(dynamic_version).json",
        )
        with open(file_path, "r+") as f:
            data = json.load(f)
            for item in data:
                if item["ID"] == id_to_update:
                    item["Saved"] = new_saved_status
                    break
            else:
                return False

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
            return True

    except FileNotFoundError:
        print("Error: JSON file not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def save_bookmark_for_MCQs_page(id_to_update, new_saved_status):
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        file_path = os.path.join(
            base_dir, "Database/Redirection/Redirecting_MCQ_test_(dynamic_version).json"
        )

        with open(file_path, "r") as f:
            data = json.load(f)

        if id_to_update in data:
            data[id_to_update]["Saved"] = new_saved_status
            with open(file_path, "w") as f:
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


def save_bookmark_to_database(id: str):
    if "LEPA" in id:
        return {"acknowledgement": save_bookmark_for_learn_page(id)}
    elif "MCPA" in id:
        return {"acknowledgement": save_bookmark_for_MCQs_page(id)}
    elif "COPA" in id:
        return {"acknowledgement": save_bookmark_for_Coding_problems_page(id)}
    else:
        return {"acknowledgement": False}
