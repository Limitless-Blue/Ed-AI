import json
import os


def get_for_website_data():

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
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return {}


# Example usage:
website_data = get_for_website_data()
print(json.dumps(website_data, indent=4))
