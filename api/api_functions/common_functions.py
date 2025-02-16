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
