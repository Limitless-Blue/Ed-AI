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


def get_resume_details():
    file_path = "Database\\Redirection\\User_data.json"
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    json_file_path = os.path.join(base_dir, file_path)

    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            if "ResumeDetails" in data:
                return data["ResumeDetails"]
            else:
                print(f"Error: 'ResumeDetails' key not found in {json_file_path}")
                return None
    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def generate_ai_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


def get_coverLetter(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


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
    user_career_info = get_resume_details()
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
    user_career_info = get_resume_details()
    prompt = f"""Write a compelling and personalized cover letter for the following job description, using the provided career information.  The cover letter should be professional, enthusiastic, and tailored to highlight the skills and experience that best align with the job requirements.  Focus on quantifiable achievements whenever possible.  Keep the tone confident but not arrogant. Aim for a concise and impactful letter, ideally no more than one page.

    **Job Description:**
    ```
        {jobDescription}
    ```

    **Career Information:**
    ```
        {user_career_info}
    ```

    **Instructions for the Cover Letter:**

    *   **Opening:**  Start with a strong opening paragraph that immediately grabs the reader's attention and clearly states the position you're applying for.  Mention how you learned about the opportunity.
    *   **Body Paragraphs:**  Develop 2-3 body paragraphs that highlight your most relevant skills and experiences.  Specifically address the key requirements and responsibilities outlined in the job description.  Provide concrete examples and quantifiable results to demonstrate your capabilities.  Connect your experience to the company's mission or values, if possible.
    *   **Closing:**  Conclude with a strong closing paragraph that reiterates your interest in the position and expresses your eagerness to learn more.  Mention your availability for an interview and thank the reader for their time and consideration.
    *   **Format:**  The cover letter should be formatted professionally, as if it were being sent to a real company.  Include a proper salutation (e.g., "Dear [Hiring Manager Name],") and closing (e.g., "Sincerely,").  Use clear and concise language, avoiding jargon or overly technical terms unless specifically relevant to the job.
    *   **Tailoring:**  The cover letter *must* be tailored specifically to this job description.  Do not generate a generic cover letter.  Reference specific requirements and demonstrate how your skills and experience directly address them.
    *   **Tone:**  Maintain a professional and enthusiastic tone throughout the letter.  Express your genuine interest in the company and the position.
    *   **Length:** Aim for a concise and impactful letter, ideally no more than one page.

    **Output the cover letter in plain text format.**
    """
    try:
        prompt_response = generate_ai_response(prompt)

        cover_letter_output_file = os.path.join(
            "API_Endpoint", "Temp_Static_data", "Chat", "cover_letter.txt"
        )
        os.makedirs(os.path.dirname(cover_letter_output_file), exist_ok=True)

        try:
            with open(cover_letter_output_file, "w") as f:
                f.write(prompt_response)
        except Exception as e:
            print(f"Error writing cover letter to file: {e}")
            return {"error": "Error writing cover letter to file."}

        return {"coverLetter": cover_letter_output_file}

    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return {"error": "Error generating cover letter."}


def cover_letter_chat_response(jobDescription, coverLetter, userMessage):
    user_career_info = get_resume_details()
    coverLetter_info = get_coverLetter(coverLetter)

    prompt = f"""
    You are a career consultant helping a job seeker tailor their cover letter.  Given the following information, revise the provided cover letter to be more effective.

    **User Message/Request:**
    {userMessage}

    **Existing Cover Letter:**
    {coverLetter_info}

    **User Career Information (from resume):**
    {user_career_info}
    
    **Job Description:**
    {jobDescription}

    **Instructions:**

    1. Carefully analyze the job description, user career information, existing cover letter, and the user's message/request.
    2. Revise the existing cover letter to:
        * Highlight the skills and experiences from the user's career information that are most relevant to the job description.
        * Address any specific requirements or qualifications mentioned in the job description.
        * Incorporate the user's message/request, which may include specific instructions or areas of focus.
        * Maintain a professional and concise tone.
        * Ensure the revised cover letter is well-structured and easy to read.
    3. Output ONLY the revised cover letter. Do not include any explanations or commentary.  Just the text of the updated cover letter.

    """
    prompt_response = generate_ai_response(prompt)
    print(f"Prompt response: {prompt_response}")
    try:
        prompt_response = generate_ai_response(prompt)

        cover_letter_output_file = os.path.join(
            "API_Endpoint", "Temp_Static_data", "Chat", "cover_letter.txt"
        )
        os.makedirs(os.path.dirname(cover_letter_output_file), exist_ok=True)

        try:
            with open(cover_letter_output_file, "w") as f:
                f.write(prompt_response)
        except Exception as e:
            print(f"Error writing cover letter to file: {e}")
            return {"error": "Error writing cover letter to file."}

        return {"coverLetter": cover_letter_output_file}

    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return {"error": "Error generating cover letter."}
