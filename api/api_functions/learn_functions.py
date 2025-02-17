import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from api.api_functions.common_functions import extract_recommendation_list


def learn_page_recommendations():
    input_ids = extract_recommendation_list("Learn_Page")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(
        base_dir, "Database/Redirection/Redirecting_learn_page_(dynamic_version).json"
    )

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    id_to_course_name = {entry["ID"]: entry["title"] for entry in data}

    recommendations = [
        {
            "id": course_id,
            "courseName": id_to_course_name.get(course_id, "Unknown Course"),
        }
        for course_id in input_ids
    ]

    filters = {
        "level": ["Easy", "Medium", "Hard"],
        "topic": [
            "Advanced Problem Solving",
            "Algorithm Analysis",
            "Array",
            "Control Structures",
            "DSA Basics",
            "Data Structures",
            "Functions",
            "Graph",
            "Hashing",
            "Heap",
            "Linked List",
            "Programming Basics",
            "Problem Solving",
            "Queue",
            "Sorting Algorithms",
            "Stack",
            "Tree",
        ],
        "status": [True, False],
    }

    output = {"recommendations": recommendations, "filters": filters}

    return output


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


def get_filtered_learn_courses():
    pass
