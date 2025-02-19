import json
import os


def change_password_database(old_password, new_password):
    file_path = "Database\\Redirection\\User_data.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)

        if data["ForWebsite"]["password"] == old_password:
            data["ForWebsite"]["password"] = new_password

            with open(json_file_path, "w") as f:
                json.dump(data, f, indent=4)

            return {"acknowledgement": True}
        else:
            return {"acknowledgement": False}

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return {"acknowledgement": False}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return {"acknowledgement": False}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"acknowledgement": False}


def change_username_database(old_username, new_username):
    file_path = "Database\\Redirection\\User_data.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)

        if data["ForWebsite"]["username"] == old_username:
            data["ForWebsite"]["username"] = new_username

            with open(json_file_path, "w") as f:
                json.dump(data, f, indent=4)

            return {"acknowledgement": True}
        else:
            return {"acknowledgement": False}

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return {"acknowledgement": False}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return {"acknowledgement": False}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"acknowledgement": False}


def change_username_database(old_username, new_username):
    file_path = "Database\\Redirection\\User_data.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)

        if data["ForWebsite"]["username"] == old_username:
            data["ForWebsite"]["username"] = new_username

            with open(json_file_path, "w") as f:
                json.dump(data, f, indent=4)

            return {"acknowledgement": True}
        else:
            return {"acknowledgement": False}

    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return {"acknowledgement": False}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return {"acknowledgement": False}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"acknowledgement": False}
