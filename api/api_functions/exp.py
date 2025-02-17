import json
import os


def get_coding_problem(problemId: str):
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


# Example usage
problemId = "COPA_3"
result = get_coding_problem(problemId)
print(json.dumps(result, indent=4))
