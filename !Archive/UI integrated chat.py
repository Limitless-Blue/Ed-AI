import time
import streamlit as st
import re
import textwrap
import streamlit as st
from langchain.document_loaders import TextLoader  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate  # Corrected import path
from dotenv import load_dotenv

load_dotenv()


def initialize_session_state():
    """Initialize chat history in session state if not already done."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def load_and_split_documents(txt_path, chunk_size=1000):
    """Load a TXT document and split it into chunks."""
    loader = TextLoader(
        txt_path, encoding="utf-8"
    )  # Use TextLoader with appropriate encoding
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=100
    )  # Optional: adjust overlap
    docs = text_splitter.split_documents(data)
    return docs


def setup_vectorstore_and_retriever(docs, embedding_model, k=10):
    """Setup the vectorstore and retriever for document similarity search."""
    vectorstore = Chroma.from_documents(
        documents=docs, embedding=GoogleGenerativeAIEmbeddings(model=embedding_model)
    )
    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": k}
    )
    return retriever


def initialize_llm(model_name, temperature=0.8, max_tokens=None, timeout=None):
    """Initialize the language model for answering queries."""
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
    )


def get_prompt_with_history(history, user_input):
    """Generate the conversation history and combine it with the new user input."""
    history_text = ""
    for item in history:
        history_text += f"Human: {item['user_input']}\n{item['response']}\n"
    history_text += f"Human: {user_input}\n"
    return history_text


def create_rag_chain(retriever, llm, system_prompt, query):
    """Create a Retrieval-Augmented Generation (RAG) chain using the retriever and LLM."""
    query = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", get_prompt_with_history(st.session_state.chat_history, query)),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, query)
    return create_retrieval_chain(retriever, question_answer_chain)


def handle_query(query, retriever, llm, system_prompt):
    """Handle the user query, process it, and update the session state with the response."""
    rag_chain = create_rag_chain(retriever, llm, system_prompt, query)
    response = rag_chain.invoke({"input": query})["answer"]

    st.session_state.chat_history.append({"user_input": query, "response": response})

    return response


def chat():
    initialize_session_state()
    docs = load_and_split_documents(r"EXP\Learn.txt")  # Changed from .pdf to .txt
    retriever = setup_vectorstore_and_retriever(
        docs, embedding_model="models/embedding-001"
    )

    llm = initialize_llm(model_name="gemini-1.5-flash")

    toggle_socratic = st.toggle(
        "Socratic Mode", value=True, key="socratic_mode_toggle_5"
    )
    # Custom CSS for chat UI
    st.markdown(
        """
        <style>
        .assistant-message {
            text-align: left !important;
            background: linear-gradient(135deg, #3d0e61, #613dc1); /* Gradient from dark blue to a lighter blue */
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

    # Initialize the session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Function to separate text and code in the assistant's message
    def render_message(content):
        # Patterns to detect both Python and JSON code blocks
        code_block_pattern = r"```(python|json)(.*?)```"

        # Split the content by code blocks
        parts = re.split(code_block_pattern, content, flags=re.DOTALL)

        for i in range(0, len(parts), 3):
            text_part = parts[i].strip()  # Regular text
            if text_part:
                st.markdown(
                    f'<div class="assistant-message">{text_part}</div>',
                    unsafe_allow_html=True,
                )

            if i + 1 < len(parts):
                language = parts[i + 1]  # Either 'python' or 'json'
                code_part = parts[i + 2].strip()  # Code block content
                if code_part:
                    st.code(code_part, language=language)

    # Display previous chat messages
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            render_message(message["content"])
        else:
            st.markdown(
                f'<div class="user-message">{message["content"]}</div>',
                unsafe_allow_html=True,
            )

    # User input section
    query = st.chat_input("What’s on your mind?")
    if query:
        # Store the user message in session state and render it
        st.session_state.messages.append({"role": "user", "content": query})
        st.markdown(f'<div class="user-message">{query}</div>', unsafe_allow_html=True)

        # Generate a response based on the toggle
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

        response_text = handle_query(query, retriever, llm, system_prompt)
        # Simulate assistant's typing effect with delay
        response_container = st.empty()
        partial_response = ""
        for word in response_text.split():
            partial_response += word + " "
            if "```python" in partial_response:
                # Display code block if detected in the message
                code_content = partial_response.split("```python")[1].split("```")[0]
                response_container.code(code_content, language="python")
            else:
                response_container.markdown(
                    f'<div class="assistant-message">{partial_response}</div>',
                    unsafe_allow_html=True,
                )
            time.sleep(0.1)

        # Store the assistant's full response and render it completely
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )
        render_message(response_text)

        # Rerun to update the chat UI
        st.rerun()


chat()
