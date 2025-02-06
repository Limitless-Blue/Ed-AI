import os
import ast
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
Coding_Problems_list_file_path = (
    r"dynamic files\Main_pages\Practice_Coding_Problems.json"
)


def Practice_Coding_Problem_recommendation():
    try:
        with open(Coding_Problems_list_file_path, "r") as f:
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
                        f"""You are provided with a JSON file containing a list of Coding Problems. Each Coding Problem is identified by a unique key (e.g., "prob_arr_00000000001") and includes a "Title" and a "Completed" status. Your task is to generate a list of 5 recommended Coding Problems based on the following criteria:
                        1. **Exclusion of Completed Coding Problems:** Only include Coding Problems where `"Completed": false`.
                        2. **Order of Difficulty:** Arrange the recommended Coding Problems from easiest to hardest based on their Topics.
                        3. **Selection When All Coding Problems Are Completed:** If all Coding Problems are marked as completed, select any 5 Coding Problems that are most suitable.
                        4. **Output Format:** The recommendations should be a list of Coding Problem identifiers, strictly adhering to the format below.

                    **Input JSON:**
                    ```json
                        {data}
                    ```

                    **Expected Output:**
                        ["prob_arr_00000000001", "prob_arr_00000000002", "prob_arr_00000000003", "prob_arr_00000000004", "prob_arr_00000000005"]

                    **Additional Notes:**
                        - Ensure that the list strictly contains only the Coding Problem identifiers (e.g., "prob_arr_00000000001").
                        - Maintain the sequence from the easiest to the most challenging topics.
                        - Do not include any Coding Problems that have `"Completed": true`.
                        - If all Coding Problems are completed, select any 5 Coding Problems that best fit the recommendation criteria.
                        - Adhere strictly to the expected output format without deviations.
                """,
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        '```\n["prob_arr_00000000001", "prob_arr_00000000002", "prob_arr_00000000004", "prob_arr_00000000006", "prob_str_00000000003"]\n``` \n',
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
            "prob_arr_00000000001",
            "prob_arr_00000000002",
            "prob_arr_00000000004",
            "prob_arr_00000000006",
            "prob_str_00000000003",
        ]
        return temp_list


def write_recommendation_data_to_Practice_Coding_Problem():
    result_of_Coding_Problems_recommendation = str(
        Practice_Coding_Problem_recommendation()
    )
    result_of_Coding_Problems_recommendation = (
        result_of_Coding_Problems_recommendation.replace("'", '"')
    )
    Coding_Problems_recommendation_file_path = r"dynamic files\Main_pages\Recommendations\Practice_Coding_Problems_Recommendation.json"

    try:
        with open(Coding_Problems_recommendation_file_path, "w") as file:
            file.write(result_of_Coding_Problems_recommendation)
        print(
            f"Data written to {Coding_Problems_recommendation_file_path} successfully."
        )
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
