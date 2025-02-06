import streamlit as st
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import os
import tempfile
from gtts import gTTS
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from Interview_Files.Screen import Mock_Interview_screen

load_dotenv()


def capture_audio():
    recognizer = sr.Recognizer()
    audio_bytes = audio_recorder()

    if audio_bytes:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".wav"
        ) as temp_audio_file:
            audio_file_path = temp_audio_file.name
            temp_audio_file.write(audio_bytes)
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            try:
                transcription = recognizer.recognize_google(audio_data)
                return transcription
            except sr.UnknownValueError:
                st.write("Could not understand the audio.")
            except sr.RequestError as e:
                st.write(f"Error with the transcription service: {e}")
        os.remove(audio_file_path)
    return None


def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer


def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def initialize_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)


def build_messages(history, user_input, system_prompt):
    messages = [SystemMessage(content=system_prompt)]
    for chat in history:
        messages.append(HumanMessage(content=chat["user_input"]))
        messages.append(AIMessage(content=chat["response"]))
    messages.append(HumanMessage(content=user_input))
    return messages


def handle_query(query, llm, system_prompt):
    messages = build_messages(st.session_state.chat_history, query, system_prompt)
    response_message = llm(messages)

    if isinstance(response_message, AIMessage):
        response = response_message.content.strip()
    else:
        response = "I'm sorry, I couldn't process your request."

    st.session_state.chat_history.append({"user_input": query, "response": response})
    return response


def hr_Mock_Interview():
    initialize_session_state()

    col1, spacer, col2 = st.columns([1.5, 0.1, 1])
    with col1:
        Mock_Interview_screen()

    with col2:
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        user_input = capture_audio()

        if user_input:
            llm = initialize_llm()

            system_prompt = (
                "You are an AI-powered HR interview assistant. Your role is to conduct a professional and engaging interview with the candidate. "
                "Follow these guidelines:\n"
                "1. **Questioning:** Start with introductory questions to make the candidate comfortable, then progressively ask more in-depth questions related to their experience, skills, and suitability for the role.\n"
                "2. **Adaptability:** Tailor your questions based on the candidate's responses. If a candidate mentions a particular skill or experience, delve deeper into that area.\n"
                "3. **Clarity and Precision:** Ask clear and concise questions. Avoid ambiguity to ensure the candidate understands what is being asked.\n"
                "4. **Feedback:** After each response, provide constructive feedback. Highlight strengths and gently point out areas for improvement.\n"
                "5. **Empathy and Professionalism:** Maintain a friendly yet professional tone. Show understanding and patience, especially if the candidate seems nervous.\n"
                "6. **Closing the Interview:** Summarize the key points discussed, outline the next steps in the hiring process, and thank the candidate for their time.\n"
                "7. **Compliance:** Ensure that all questions comply with employment laws and avoid any discriminatory or inappropriate topics.\n\n"
                "Begin the interview now."
            )

            response = handle_query(user_input, llm, system_prompt)

            audio_response = text_to_speech(response)
            st.audio(audio_response, format="audio/mp3")

        else:
            response = None

        if user_input:
            st.markdown(
                f'<p style="text-align:right; margin-bottom:10px; color:gray;"><strong>You:</strong> {user_input}</p>',
                unsafe_allow_html=True,
            )
        if response:
            st.markdown(
                f'<p style="text-align:left; margin-bottom:5px;"><strong>Interviewer:</strong> {response}</p>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)
