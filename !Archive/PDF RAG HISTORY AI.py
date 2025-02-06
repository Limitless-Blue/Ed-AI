import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


def initialize_session_state():
    """Initialize chat history in session state if not already done."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def load_and_split_documents(pdf_path, chunk_size=1000):
    """Load a PDF document and split it into chunks."""
    loader = PyPDFLoader(pdf_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
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


def initialize_llm(model_name, temperature=0.7, max_tokens=None, timeout=None):
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
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", get_prompt_with_history(st.session_state.chat_history, query)),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)


def handle_query(query, retriever, llm, system_prompt):
    """Handle the user query, process it, and update the session state with the response."""
    rag_chain = create_rag_chain(retriever, llm, system_prompt, query)
    response = rag_chain.invoke({"input": query})["answer"]

    st.session_state.chat_history.append({"user_input": query, "response": response})

    return response


def AI_response():
    initialize_session_state()

    docs = load_and_split_documents(r"EXP\mental_health.pdf")
    retriever = setup_vectorstore_and_retriever(
        docs, embedding_model="models/embedding-001"
    )

    llm = initialize_llm(model_name="gemini-1.5-flash")
    system_prompt = (
        "You are an AI assistant providing empathetic mental health and emotional support to students. "
        "Your role is to listen, understand, and offer comforting, positive guidance. Ensure your responses "
        "are gentle and encouraging. If you don’t know something or if the situation seems severe, suggest that "
        "the user speak to a counselor or a trusted person.\n\n"
        "{context}"
    )

    query = st.chat_input("How are you feeling today?")

    if query:
        response = handle_query(query, retriever, llm, system_prompt)
        st.write(response)


AI_response()
