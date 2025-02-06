import os
import ast
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
Learn_list_file_path = r"dynamic files\Main_pages\Learn.json"


def learn_recommendation():
    try:
        with open(Learn_list_file_path, "r") as f:
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
                        f"""You are provided with a JSON file containing a list of courses. Each course has an \"Image Box\" identifier, a \"Title\", and a \"Completed\" status. Your task is to generate a list of 5 recommended courses based on the following criteria:\n\n1. **Exclusion of Completed Courses:** Only include courses where `\"Completed\": false`.\n2. **Order of Difficulty:** Arrange the recommended courses from easiest to hardest based on their topics.\n3. **Selection When All Courses Are Completed:** If all courses are marked as completed, select any 5 courses that are most suitable.\n4. **Output Format:** The recommendations should be a list of \"Image Box\" identifiers, strictly adhering to the format below.\n\n**Input JSON:**\n```{data}```\n[\"Image Box X\", \"Image Box Y\", \"Image Box Z\", \"Image Box A\", \"Image Box B\"]\n```\n\n**Additional Notes:**\n- Ensure that the list strictly contains only the \"Image Box\" identifiers.\n- Maintain the sequence from the easiest to the most challenging topics.\n- Do not include any courses that have `\"Completed\": true`.\n- If all courses are completed, select any 8 courses that best fit the recommendation criteria.\n- Adhere strictly to the expected output format without deviations.\n""",
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        '```\n["Image Box 2", "Image Box 3", "Image Box 7", "Image Box 9", "Image Box 11"]\n``` \n',
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
            "Image Box 2",
            "Image Box 4",
            "Image Box 5",
            "Image Box 6",
            "Image Box 7",
        ]
        return temp_list


def write_recommendation_data_to_Learn_file():
    result_of_learn_recommendation = str(learn_recommendation())
    result_of_learn_recommendation = result_of_learn_recommendation.replace("'", '"')
    learn_recommendation_file_path = (
        r"dynamic files\Main_pages\Recommendations\Learn_Recommendation.json"
    )

    try:
        with open(learn_recommendation_file_path, "w") as file:
            file.write(result_of_learn_recommendation)
        print(f"Data written to {learn_recommendation_file_path} successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
