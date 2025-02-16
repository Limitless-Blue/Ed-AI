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


streak_data = streak_data()

if streak_data:
    print(json.dumps(streak_data, indent=4))
