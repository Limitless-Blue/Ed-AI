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


def get_all_mcq_test(testId: str):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(
        base_dir, "Database\\Redirection\\Redirecting_MCQ_test_(dynamic_version).json"
    )

    with open(json_file_path, "r") as file:
        data = json.load(file)

    if testId in data:
        test_file = data[testId].get("Test_file")
        return {"testFile": test_file}
    else:
        return {"error": "Test ID not found"}


def get_all_coding_problem(problemId: str):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(
        base_dir,
        "Database\\Redirection\\Redirecting_Coding_Problem_(dynamic_version).json",
    )

    with open(json_file_path, "r") as file:
        data = json.load(file)

    problem_data = data["problems"].get(problemId)

    if problem_data:
        problem_description = problem_data["Problem_Description"]
        problem_solution = problem_data["Problem_Solution"]
        test_cases = []

        for test_case in problem_data["Test_Cases"]:
            input_case = test_case[0]
            output_case = eval(test_case[1])
            test_cases.append([input_case, output_case])

        return {
            "problemDescription": problem_description,
            "problemSolution": problem_solution,
            "testCases": test_cases,
        }
    else:
        return {"error": f"Problem with ID {problemId} not found."}


def update_coding_problem_page_database(courseId):
    json_file_path = (
        "Database\\Redirection\\Redirecting_Coding_Problem_(dynamic_version).json"
    )
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(base_dir, json_file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "problems" not in data:
            data["problems"] = {}

        if courseId in data["problems"]:
            data["problems"][courseId]["Completed"] = True

        else:
            print(f"Course ID '{courseId}' not found in the database.")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Database updated for Course ID: {courseId} (Completed set to True)")

    except FileNotFoundError:
        print(f"Error: JSON file not found at {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# TODO: Add AI Part
def update_recommendation_coding_problem_page_database():
    pass


def submit_practice_function(courseId, score):
    update_coding_problem_page_database(courseId)
    update_recommendation_coding_problem_page_database()

    return {"acknowledgement": True}


def update_MCQs_page_database(courseId, score):
    file_path = "Database\\Redirection\\Redirecting_MCQ_test_(dynamic_version).json"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        if courseId in data:
            data[courseId]["Score"] = score
            data[courseId]["Completed"] = True

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            print(f"Successfully updated data for {courseId}.")
        else:
            print(f"Course ID '{courseId}' not found in the database.")

    except FileNotFoundError:
        print(f"Error: JSON file not found at {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# TODO: Add AI Part
def update_recommendation_MCQs_page_database():
    pass


def end_practice_function(courseId, score):
    update_MCQs_page_database(courseId, score)
    update_recommendation_MCQs_page_database()

    return {"acknowledgement": True}
