import json
import os


def get_learn_page_data(input_id):
    try:
        current_dir = os.path.dirname(__file__)
        base_dir = os.path.join(current_dir, "..", "..")
        file_path = os.path.join(
            base_dir,
            "Database\\Redirection\\Redirecting_learn_page_(dynamic_version).json",
        )

        with open(file_path, "r") as f:
            data = json.load(f)

    except FileNotFoundError:
        print("Error: JSON file not found.")
        return {}

    for page_data in data:
        try:
            if page_data["ID"] == input_id:
                return {
                    "course": page_data["Course"],
                    "test": page_data["Test"],
                    "bookmark": page_data["Saved"],
                    "completed": page_data["Completed"],
                }
        except KeyError:
            print(f"Warning: Missing 'ID' key in page data: {page_data}")

    return {"message": f"Learn page with ID '{input_id}' not found."}


input_id = "LEPA_2"
output_data = get_learn_page_data(input_id)
print(json.dumps(output_data, indent=4))
