import json
import os


def get_previous_results():
    file_path = "Database\\Redirection\\Interview_simulation.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data.get("Previous_Results")
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage:
previous_results = get_previous_results()
print(json.dumps(previous_results, indent=4))
