import json
import os

def save_bookmark_for_learn_page(id_to_update, new_saved_status):

  try:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, "Database/Redirection/Redirecting_learn_page_(dynamic_version).json")
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

# Example usage:
if save_bookmark_for_learn_page("LEPA_143", True):
  print(f"Saved status for ID 'LEPA_1' updated successfully.")
else:
  print(f"Failed to update saved status for ID 'LEPA_1'.")