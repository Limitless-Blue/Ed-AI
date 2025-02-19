import os
import google.generativeai as genai
import speech_recognition as sr
import subprocess
from pydub import AudioSegment
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from pydub.effects import speedup
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Google_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")


def increase_playback_speed_no_pitch(input_file, output_file, speed_factor=1.3):
    sound = AudioSegment.from_mp3(input_file)
    new_sound = speedup(sound, playback_speed=speed_factor)
    new_sound.export(output_file, format="mp3")


def generate_ai_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


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


def landing_page_mentor_text_chat_response(user_input, conversation_history):
    generate_ai_response_prompt = f"""Answer the user's question.

    User Question: {user_input}
    """

    response = generate_ai_response(generate_ai_response_prompt)
    conversation_history.append({"speaker": "user", "text": user_input})
    conversation_history.append({"speaker": "AI", "text": response})
    return {
        "AI": response,
        "conversationHistory": conversation_history,
    }


def landing_page_mentor_voice_chat_response(audioFile, conversationHistory):
    user_input = transcribe_audio(audioFile)
    response_data = landing_page_mentor_text_chat_response(
        user_input, conversationHistory
    )
    response_audio_path = os.path.join(
        "API_Endpoint", "Temp_Static_data", "Chat", "Response.mp3"
    )
    try:
        tts = gTTS(text=response_data["AI"], lang="en", slow=False)
        os.makedirs(os.path.dirname(response_audio_path), exist_ok=True)
        tts.save(response_audio_path)
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")
        response_audio_path = ""

    response_speeded_up_output_file = os.path.join(
        "API_Endpoint", "Temp_Static_data", "Chat", "Test_output_speed_up.mp3"
    )

    increase_playback_speed_no_pitch(
        response_audio_path, response_speeded_up_output_file
    )

    return {
        "responseAudio": response_speeded_up_output_file,
        "conversationHistory": response_data["conversationHistory"],
    }
