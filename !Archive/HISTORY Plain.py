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

    # Append the current user input
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

    # Generate response using the LLM
    response_message = llm(messages)

    # Extract the content from the AIMessage object
    if isinstance(response_message, AIMessage):
        response = response_message.content.strip()
    else:
        # Handle unexpected response types
        response = "I'm sorry, I couldn't process your request."

    # Update chat history
    st.session_state.chat_history.append({"user_input": query, "response": response})

    return response


def AI_response():
    initialize_session_state()

    llm = initialize_llm(model_name="gemini-1.5-flash")
    system_prompt = (
        "You are an AI assistant providing empathetic mental health and emotional support to students. "
        "Your role is to listen, understand, and offer comforting, positive guidance. Ensure your responses "
        "are gentle and encouraging. If you don’t know something or if the situation seems severe, suggest that "
        "the user speak to a counselor or a trusted person."
    )

    query = st.chat_input("How are you feeling today?")

    if query:
        response = handle_query(query, llm, system_prompt)
        st.write(response)

    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### Chat History")
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['user_input']}")
            st.markdown(f"**AI:** {chat['response']}")


if __name__ == "__main__":
    AI_response()
