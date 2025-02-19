import os
import google.generativeai as genai
import speech_recognition as sr
import subprocess
from pydub import AudioSegment
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")


def check_ffmpeg():
    try:
        subprocess.check_output(["ffmpeg", "-version"])
    except FileNotFoundError:
        print("ffmpeg is not installed or not in your system's PATH.")
        return False
    return True


def convert_mp3_to_wav(mp3_file: str) -> str:
    if check_ffmpeg():
        wav_file = mp3_file.replace(".mp3", ".wav")
        sound = AudioSegment.from_mp3(mp3_file)
        sound.export(wav_file, format="wav")
        return wav_file
    else:
        raise RuntimeError("Cannot convert MP3 to WAV. ffmpeg is required.")


def generate_non_socratic_ai_response(
    prompt: str, conversation_history: List[Dict[str, str]]
) -> str:
    conversation_text = "".join(
        [f"{entry['speaker']}: {entry['text']}\n" for entry in conversation_history]
    )
    full_prompt = conversation_text + f"User: {prompt}\nAI: "
    response = model.generate_content(full_prompt)
    return response.text.strip()


def generate_socratic_ai_response(
    prompt: str, conversation_history: List[Dict[str, str]]
) -> str:
    conversation_text = "".join(
        [f"{entry['speaker']}: {entry['text']}\n" for entry in conversation_history]
    )

    full_prompt = f"""
    You are a Socratic tutoring assistant specializing in Sorting Algorithms.  Your goal is to guide the student to the correct solution through questioning, not by giving direct answers. Focus on understanding the student's reasoning and identifying their misconceptions.  Be patient and encouraging.  If the student's code has issues (like timeouts or incorrect output), use the Socratic method to lead them to discover the problem and its solution.  Avoid simply stating the error.

    Here are some examples of Socratic questions you can ask:

    *   "Can you walk me through your code step by step, explaining what each part does?"
    *   "What are the different types of sorting algorithms you know, and what are their time and space complexities?"
    *   "What are the key differences between this test case and the ones that passed?"
    *   "Can you analyze the time complexity of the section of your code that handles this specific type of input?"
    *   "What are some ways to optimize that section of code?"
    *   "What are the potential edge cases for this algorithm?"
    *   "Is there another approach you could try?"
    *   "How does your algorithm compare to other sorting algorithms in terms of efficiency?"
    *   "Let's consider a slightly different input. How would your algorithm handle it?"

    Remember to tailor your questions to the student's responses and the specific problem they are facing.  Be concise and avoid jargon unless the student has demonstrated understanding of it.  Prioritize understanding the student's thought process.

    Conversation History:
    {conversation_text}
    User: {prompt}
    AI: 
    """

    response = model.generate_content(full_prompt)
    return response.text.strip()


def chat_text_text_socraticAI(
    user_input: str, conversation_history: List[Dict[str, str]]
):
    ai_response = generate_socratic_ai_response(user_input, conversation_history)
    conversation_history.append({"speaker": "user", "text": user_input})
    conversation_history.append({"speaker": "AI", "text": ai_response})
    return {
        "user": user_input,
        "AI": ai_response,
        "conversationHistory": conversation_history,
    }


def chat_text_text_Non_socraticAI(
    user_input: str, conversation_history: List[Dict[str, str]]
):
    ai_response = generate_non_socratic_ai_response(user_input, conversation_history)
    conversation_history.append({"speaker": "user", "text": user_input})
    conversation_history.append({"speaker": "AI", "text": ai_response})
    return {
        "user": user_input,
        "AI": ai_response,
        "conversationHistory": conversation_history,
    }


def transcribe_audio(audio_file: str) -> str:
    recognizer = sr.Recognizer()
    if audio_file.endswith(".mp3"):
        audio_file = convert_mp3_to_wav(audio_file)
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"


def chat_text_voice_socraticAI(
    user_audio_file: str, conversation_history: List[Dict[str, str]]
):
    user_input = transcribe_audio(user_audio_file)
    return chat_text_text_socraticAI(user_input, conversation_history)


def chat_text_voice_Non_socraticAI(
    user_audio_file: str, conversation_history: List[Dict[str, str]]
):
    user_input = transcribe_audio(user_audio_file)
    return chat_text_text_Non_socraticAI(user_input, conversation_history)
