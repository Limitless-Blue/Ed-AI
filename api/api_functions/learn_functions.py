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
        "topic": ["Linked_List", "Trees", "Stacks", "Queues", "Arrays", "Strings"],
        "status": [True, False],
    }

    output = {"recommendations": recommendations, "filters": filters}

    return output
