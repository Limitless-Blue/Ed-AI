import json
import os
import sys
from typing import List, Optional, Dict, Any
import google.generativeai as genai
import speech_recognition as sr
import subprocess
from pydub import AudioSegment
from dotenv import load_dotenv
import chromadb
import re

load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")

CHROMA_PATH = "Database\\AI_Database\\Vector_Database"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="psychologist")


def clean_json_string(text):
    text = re.sub(
        r"(^\s*```\s*json?\s*$|\n\s*```\s*$)",
        "",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    ).strip()
    text = text.strip("`")
    return text


def generate_ai_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


def get_user_career_info(job_description):
    prompt = f"""
    Given the following job description:
    ```
    {job_description}
    ```

    Summarize the user's relevant job experience, projects, and achievements that demonstrate their fit for this role. Focus on quantifiable achievements and skills that align with the job requirements. If the user profile is not provided, please provide general advice on what kind of experience would be beneficial for the role.

    If no relevant information is found, state "No relevant career information found."
    """

    results = collection.query(
        query_texts=[prompt],
        n_results=2,
    )
    print(f"Results: {results}")
    if results["documents"]:
        return results["documents"][0]
    else:
        return "No relevant career information found."


def analyze_job_match_response(jobDescription):
    user_career_info = get_user_career_info(jobDescription)
    print(f"User career info: {user_career_info}")

    prompt = f"""
    Analyze the following job description and provide a structured response in JSON format. The response should contain the following keys:

    *   `match`: A string indicating the overall match quality. Possible values are "Good", "Fair", or "Poor". Base this on the alignment of the job description's requirements with common candidate profiles for such roles.
    *   `skillGapAnalysis`: A detailed analysis of potential skill gaps. Identify specific skills mentioned in the job description that might be challenging to find in typical candidates, or where the job description requires a very specialized skill set. Explain *why* these are potential gaps. If there are no apparent gaps, state "No significant skill gaps identified."
    *   `salaryInsights`: Provide insights into the expected salary range for this role. if specified in the job description or if you can infer it. If not specified, state "Salary range not provided."

    **NOTE:** Ensure the response is valid JSON and can be parsed directly by a program. Do not include any explanatory text outside the JSON structure.

    **Job Description:**
    ```
    {jobDescription}
    ```

    **About User Career:**
    ```
    {user_career_info}
    ```
    """

    prompt_response = generate_ai_response(prompt)
    prompt_response_cleaned = clean_json_string(prompt_response)
    try:
        return json.loads(prompt_response_cleaned)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw response:\n {prompt_response_cleaned}")
        return {
            "error": "Invalid JSON response from AI model",
            "raw_response": prompt_response_cleaned,
        }


def generate_cover_letter_response(jobDescription):
    prompt = f""" """
    prompt_response = generate_ai_response(prompt)
    return

    # return {
    #     "coverLetter": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt"
    # }


def cover_letter_chat_response(jobDescription, coverLetter, userMessage):
    prompt = f""" """
    prompt_response = generate_ai_response(prompt)
    return

    # return {
    #     "coverLetter": r"API_Endpoint\Temp_Static_data\JobSearchOptimization\CoverLetter.txt"
    # }
