import streamlit as st


WELCOME_MESSAGE = {
    "role": "model",
    "content": "👋 Hi! I'm your Gemini AI Assistant. I can answer general questions, remember our conversation, and retrieve real-time information using Google Search."
}


def initialize_memory():
    """
    Initialize chat history if it doesn't exist.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [WELCOME_MESSAGE]


def add_message(role, content):
    """
    Add a message to chat history.
    """
    st.session_state.messages.append(
        {
            "role": role,
            "content": content
        }
    )


def get_messages():
    """
    Return all messages.
    """
    return st.session_state.messages


def clear_memory():
    """
    Clear conversation history and reset the Gemini chat session.
    """
    st.session_state.messages = [WELCOME_MESSAGE]
    if "chat_session" in st.session_state:
        del st.session_state.chat_session
