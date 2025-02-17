import json
import os


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


# Example usage
level = "Easy"  # Example level filter
status = False  # Example status filter (True or False)
topic = ["Iterables"]  # Example topic filter (can be a list of topics)

# Get filtered practices
filtered_practices = get_filtered_mcqs_courses(level=level, status=status, topic=topic)

# Output the result
print(json.dumps(filtered_practices, indent=4))
