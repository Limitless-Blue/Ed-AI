import os
import ast
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MCQs_list_file_path = r"dynamic files\Main_pages\Practice_MCQ.json"


def Practice_MCQs_recommendation():
    try:
        with open(MCQs_list_file_path, "r") as f:
            data = json.load(f)

        generation_config = {
            "temperature": 0.05,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        f"""You are provided with a JSON file containing a list of courses. Each course has an "Image Box" identifier, a "Title", and a "Completed" status. Your task is to generate a list of 5 recommended courses based on the following criteria:
                        1. **Exclusion of Completed Courses:** Only include courses where `"Completed": false`.
                        2. **Order of Difficulty:** Arrange the recommended courses from easiest to hardest based on their topics.
                        3. **Selection When All Courses Are Completed:** If all courses are marked as completed, select any 8 courses that are most suitable.
                        4. **Output Format:** The recommendations should be a list of "Image Box" identifiers, strictly adhering to the format below.

                    **Input JSON:**
                    ```json
                        {data}
                    ```

                    **Recommended Courses:**
                        ["Programming_Fundamentals_000001", "Array_000001", "Linked_List_000001", "Stack_000001", "Queue_000001"]

                    **Additional Notes:**
                        - Ensure that the list strictly contains only the "Image Box" identifiers.
                        - Maintain the sequence from the easiest to the most challenging topics.
                        - Do not include any courses that have `"Completed": true`.
                        - If all courses are completed, select any 8 courses that best fit the recommendation criteria.
                        - Adhere strictly to the expected output format without deviations.
                    """,
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        '```\n["Programming_Fundamentals_000001", "Linked_List_000001", "Queue_000001", "Graph_000001", "Hashing_000001"]\n``` \n',
                    ],
                },
            ]
        )

        response = chat_session.send_message("INSERT_INPUT_HERE")

        temp_text = response.text
        string_data = temp_text.replace("```", "")
        list_response = ast.literal_eval(string_data)
        print(list_response)

        return list_response
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        temp_list = [
            "Programming_Fundamentals_000001",
            "Linked_List_000001",
            "Queue_000001",
            "Graph_000001",
            "Hashing_000001",
        ]
        return temp_list


def write_recommendation_data_to_Practice_MCQs():
    result_of_MCQs_recommendation = str(Practice_MCQs_recommendation())
    result_of_MCQs_recommendation = result_of_MCQs_recommendation.replace("'", '"')
    MCQs_recommendation_file_path = (
        r"dynamic files\Main_pages\Recommendations\Practice_MCQ_Recommendation.json"
    )

    try:
        with open(MCQs_recommendation_file_path, "w") as file:
            file.write(result_of_MCQs_recommendation)
        print(f"Data written to {MCQs_recommendation_file_path} successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
