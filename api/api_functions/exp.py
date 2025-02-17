import json
from typing import Optional, List
import os


def get_filtered_learn_courses(
    level: Optional[str] = None,
    status: Optional[bool] = None,
    topic: Optional[str] = None,
):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(
        base_dir, "Database\\Redirection\\Redirecting_learn_page_(dynamic_version).json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        courses = json.load(file)

    filtered_courses = []
    for course in courses:
        if level and course.get("level") != level:
            continue
        if status is not None and course.get("Completed") != status:
            continue
        if topic and topic not in course.get("topic", []):
            continue

        filtered_courses.append(
            {
                "id": course["ID"],
                "courseName": course["title"],
                "level": course["level"],
                "topics": course["topic"],
                "completed": course["Completed"],
            }
        )

    return filtered_courses


# Example usage
if __name__ == "__main__":
    print(
        json.dumps(
            get_filtered_learn_courses(level="Easy", status=False, topic="DSA Basics"),
            indent=4,
        )
    )
