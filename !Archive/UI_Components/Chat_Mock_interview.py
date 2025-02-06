import time
import re
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()


def initialize_session_state():
    """Initialize chat history in session state if not already done."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def initialize_llm(model_name, temperature=0.7, max_tokens=None, timeout=None):
    """Initialize the language model for chatting."""
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
    )


def build_messages(history, user_input, system_prompt):
    """
    Construct the list of messages for the chat model.

    Args:
        history (list): List of previous chat messages.
        user_input (str): The latest user input.
        system_prompt (str): The system prompt defining AI behavior.

    Returns:
        list: A list of message instances.
    """
    messages = [SystemMessage(content=system_prompt)]

    for chat in history:
        messages.append(HumanMessage(content=chat["user_input"]))
        messages.append(AIMessage(content=chat["response"]))

    messages.append(HumanMessage(content=user_input))

    return messages


def handle_query(query, llm, system_prompt):
    """
    Handle the user query, generate a response, and update the session state with the response.

    Args:
        query (str): The user's input.
        llm: The language model instance.
        system_prompt (str): The system prompt defining AI behavior.

    Returns:
        str: The AI's response.
    """
    messages = build_messages(st.session_state.chat_history, query, system_prompt)

    response_message = llm(messages)

    if isinstance(response_message, AIMessage):
        response = response_message.content.strip()
    else:
        response = "I'm sorry, I couldn't process your request."

    st.session_state.chat_history.append({"user_input": query, "response": response})

    return response


def Help_Chat():
    initialize_session_state()

    llm = initialize_llm(model_name="gemini-1.5-flash")

    toggle_socratic = st.toggle(
        "Socratic Mode", value=True, key="socratic_mode_toggle_4"
    )
    st.markdown(
        """
        <style>
        .assistant-message {
            text-align: left !important;
            background: linear-gradient(90deg, #33006e, #41008b, #5202db);
            color: white;
            padding: 12px;
            border-radius: 20px;
            margin: 5px 0;
            width: fit-content;
            max-width: 80%;
        }
        .user-message {
            text-align: right !important;
            background-color: #333333;
            color: white;
            padding: 12px;
            border-radius: 20px;
            margin: 5px 0;
            width: fit-content;
            max-width: 80%;
            margin-left: auto !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def render_message(content):
        code_block_pattern = r"```(python|json)(.*?)```"

        parts = re.split(code_block_pattern, content, flags=re.DOTALL)

        for i in range(0, len(parts), 3):
            text_part = parts[i].strip()
            if text_part:
                st.markdown(
                    f'<div class="assistant-message">{text_part}</div>',
                    unsafe_allow_html=True,
                )

            if i + 1 < len(parts):
                language = parts[i + 1]
                code_part = parts[i + 2].strip()
                if code_part:
                    st.code(code_part, language=language)

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            render_message(message["content"])
        else:
            st.markdown(
                f'<div class="user-message">{message["content"]}</div>',
                unsafe_allow_html=True,
            )

    query = st.chat_input("What’s on your mind?")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.markdown(f'<div class="user-message">{query}</div>', unsafe_allow_html=True)

        if toggle_socratic:
            system_prompt = (
                "You are an AI teaching assistant specializing in Data Structures and Algorithms."
                "Your primary teaching method is the Socratic method, where you guide students by asking probing and thought-provoking questions instead of providing direct answers. "
                "Your goal is to help students understand concepts deeply by encouraging them to think critically and arrive at solutions independently. "
                "Ensure your interactions are patient, encouraging, and supportive, adapting your questions based on the student's responses to lead them toward the correct understanding. "
                "If a student remains stuck or frustrated after an extended conversation, provide a direct answer with a clear explanation to help them overcome the obstacle.\n\n"
                "{context}"
            )
        else:
            system_prompt = (
                "You are a Friendly Teacher specializing in Data Structures and Algorithms. "
                "Your primary teaching method is direct instruction, where you provide clear explanations and engaging examples to help students grasp concepts effectively. "
                "Your goal is to support students in their learning journey by offering detailed insights, step-by-step guidance, and practical applications in a welcoming manner. "
                "Ensure your interactions are warm, encouraging, and supportive, providing clear explanations that anticipate student questions and challenges. "
                "If a student expresses confusion or difficulty, address their concerns directly with comprehensive explanations and relatable examples, fostering a positive learning environment.\n\n"
                "{context}"
            )

        response_text = handle_query(query, llm, system_prompt)
        response_container = st.empty()
        partial_response = ""
        for word in response_text.split():
            partial_response += word + " "
            if "```python" in partial_response:
                code_content = partial_response.split("```python")[1].split("```")[0]
                response_container.code(code_content, language="python")
            else:
                response_container.markdown(
                    f'<div class="assistant-message">{partial_response}</div>',
                    unsafe_allow_html=True,
                )
            time.sleep(0.1)

        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )
        render_message(response_text)

        st.rerun()
