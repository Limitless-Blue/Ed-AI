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

# Load environment variables
load_dotenv()


# Function for capturing and transcribing audio
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


# Function for text-to-speech conversion
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer


# Initialize session state for chat history
def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


# Initialize the language model
def initialize_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)


# Build chat messages for the LLM
def build_messages(history, user_input, system_prompt):
    messages = [SystemMessage(content=system_prompt)]
    for chat in history:
        messages.append(HumanMessage(content=chat["user_input"]))
        messages.append(AIMessage(content=chat["response"]))
    messages.append(HumanMessage(content=user_input))
    return messages


# Handle user input and generate AI response
def handle_query(query, llm, system_prompt):
    messages = build_messages(st.session_state.chat_history, query, system_prompt)
    response_message = llm(messages)

    if isinstance(response_message, AIMessage):
        response = response_message.content.strip()
    else:
        response = "I'm sorry, I couldn't process your request."

    st.session_state.chat_history.append({"user_input": query, "response": response})
    return response


# Display the mock interview page
def Mock_Interview():
    # Initialize session state
    initialize_session_state()

    # Custom CSS for centering all content
    st.markdown(
        """
    <style>
    .centered-content {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
    }
    .mentor-title {
        font-size: 28px;
        font-weight: bold;
        background: linear-gradient(90deg, #FFF5EE, #F3CFC6, #f9bec7, #ffafcc, #f72585, #b5179e, #7209b7, #560bad, #480ca8, #3a0ca3, #3f37c9, #4361ee, #4895ef, #4cc9f0, #caf0f8, #FFF5EE, #FFF5EE);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        background-size: 200% 200%;
        animation: gradientFlow 5s ease infinite;
        margin-top: 0;
        margin-bottom: 15px;
    }
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    <div class="centered-content">
        <h1 class="mentor-title">✨ Mock Interview</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )
    col1, spacer, col2 = st.columns(
        [1.5, 0.1, 1]
    )  # Adjust the middle column width (spacer) as needed
    with col1:
        Mock_Interview_screen()

    with col2:
        # Center the audio recording and response content
        st.markdown('<div class="centered-content">', unsafe_allow_html=True)
        user_input = capture_audio()

        if user_input:
            llm = initialize_llm()

            system_prompt = (
                "You are an AI conducting a professional interview. Ask questions based on the user's responses, "
                "follow up with clarifications, and provide feedback on their answers."
            )
            response = handle_query(user_input, llm, system_prompt)

            # Display AI's audio response and text
            audio_response = text_to_speech(response)
            st.audio(audio_response, format="audio/mp3")

        else:
            response = None

        # Ensure response and user_input are not None before rendering
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


if __name__ == "__main__":
    Mock_Interview()
