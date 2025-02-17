import json
from typing import Optional
import os


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


# Define file path
level = "Easy"
status = False
topic = None

filtered_results = get_filtered_codingQuestions_courses(
    level=level, status=status, topic=topic
)

print(json.dumps(filtered_results, indent=4))
