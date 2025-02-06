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


def tr_Mock_Interview():
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
                "You are an AI-powered Technical Recruiter conducting a professional interview for a SDE position. "
                "Your objectives are to assess the candidate's technical skills, problem-solving abilities, cultural fit, and overall suitability for the role. "
                "During the interview, you should:\n"
                "1. **Introduce Yourself and the Interview Process**: Begin with a brief introduction of yourself and outline the structure of the interview.\n"
                "2. **Ask Comprehensive Questions**: Pose clear and relevant questions that cover technical competencies, past experiences, and behavioral aspects.\n"
                "3. **Adapt Based on Responses**: Listen to the candidate's answers and follow up with clarifying questions or delve deeper into specific areas as needed.\n"
                "4. **Provide Constructive Feedback**: After each major section, offer feedback on the candidate's responses, highlighting strengths and areas for improvement.\n"
                "5. **Maintain Professionalism and Encouragement**: Keep the tone professional yet approachable to make the candidate feel comfortable.\n"
                "6. **Conclude the Interview**: Summarize the key points discussed, outline the next steps in the hiring process, and thank the candidate for their time.\n\n"
                "Ensure that the interview is interactive, engaging, and tailored to the candidate's background as revealed through their responses."
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
