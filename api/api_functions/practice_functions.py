import json
import os
import sys
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from api.api_functions.common_functions import extract_recommendation_list


def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def practice_page_recommendations():
    MCQs_input_ids = extract_recommendation_list("MCQs_page")
    coding_problems_input_ids = extract_recommendation_list("coding_problems_page")

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    MCQs_json_file_path = os.path.join(
        base_dir, "Database\\Redirection\\Redirecting_MCQ_test_(dynamic_version).json"
    )
    coding_problems_json_file_path = os.path.join(
        base_dir,
        "Database\\Redirection\\Redirecting_Coding_Problem_(dynamic_version).json",
    )

    MCQs_data = load_json(MCQs_json_file_path)
    coding_problems_data = load_json(coding_problems_json_file_path)

    mcq_recommendations = [
        {"id": mcq_id, "practiceName": MCQs_data[mcq_id]["Title"]}
        for mcq_id in MCQs_input_ids
        if mcq_id in MCQs_data
    ]

    coding_recommendations = [
        {
            "id": problem_id,
            "practiceName": coding_problems_data["problems"][problem_id]["title"],
        }
        for problem_id in coding_problems_input_ids
        if problem_id in coding_problems_data["problems"]
    ]

    mcq_levels = sorted({MCQs_data[key]["level"] for key in MCQs_data})
    mcq_topics = sorted(
        {topic for key in MCQs_data for topic in MCQs_data[key]["topic"]}
    )
    coding_levels = sorted(
        {
            coding_problems_data["problems"][key]["Difficulty"]
            for key in coding_problems_data["problems"]
        }
    )
    coding_topics = sorted(
        {
            topic
            for key in coding_problems_data["problems"]
            for topic in coding_problems_data["problems"][key]["topic"]
        }
    )

    return {
        "mcqRecommendations": mcq_recommendations,
        "codingRecommendations": coding_recommendations,
        "filters": {
            "mcqs": {
                "level": mcq_levels,
                "topic": mcq_topics,
                "status": [True, False],
            },
            "codingQuestions": {
                "level": coding_levels,
                "topic": coding_topics,
                "status": [True, False],
            },
        },
    }


def get_filtered_mcqs_courses(level=None, status=None, topic=None):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(
        base_dir, "Database\\Redirection\\Redirecting_MCQ_test_(dynamic_version).json"
    )

    with open(json_file_path, "r") as file:
        data = json.load(file)

    output = []

    for key, practice in data.items():
        practice_name = practice["Title"]
        practice_status = practice["Saved"]
        practice_level = practice["level"]
        practice_topic = practice["topic"]

        if level and practice_level != level:
            continue
        if status is not None and practice_status != status:
            continue
        if topic and not any(t in practice_topic for t in topic):
            continue

        output.append(
            {
                "id": key,
                "practiceName": practice_name,
                "status": practice_status,
                "difficulty": practice_level.lower(),
            }
        )

    return output


def get_filtered_codingQuestions_courses(
    level: Optional[str] = None,
    status: Optional[bool] = None,
    topic: Optional[str] = None,
):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(
        base_dir,
        "Database\\Redirection\\Redirecting_Coding_Problem_(dynamic_version).json",
    )
    with open(json_file_path, "r") as file:
        data = json.load(file)
    filtered_problems = []

    for problem_id, problem_data in data["problems"].items():
        if level and level.lower() != problem_data["Difficulty"].lower():
            continue
        if status is not None and status != problem_data["Completed"]:
            continue
        if topic and topic not in problem_data["topic"]:
            continue

        filtered_problems.append(
            {
                "id": problem_id,
                "practiceName": problem_data["title"],
                "status": problem_data["Completed"],
                "difficulty": problem_data["Difficulty"].lower(),
            }
        )

    return filtered_problems


def get_filtered_practice_courses(type, level, status, topic):
    if type == "mcqs":
        return get_filtered_mcqs_courses(level, status, topic)
    elif type == "codingQuestions":
        return get_filtered_codingQuestions_courses(level, status, topic)
