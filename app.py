import streamlit as st
from core.memory import (
    initialize_memory,
    clear_memory
)
from core.logger import logger
import core.memory as memory

# Page configuration
st.set_page_config(
    page_title="Voice-Activated Personal Assistant",
    page_icon="🎙️",
    layout="centered"
)

# Custom premium styling via markdown
st.markdown(
    """
    <style>
    /* Gradient App Header */
    .app-header {
        background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }
    
    /* Sleek status indicator pill */
    .status-pill {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 50px;
        background-color: #F1F5F9;
        color: #0F172A;
        font-size: 0.9rem;
        font-weight: 700;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Content containers */
    .container-box {
        padding: 1.2rem;
        border-radius: 12px;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
        color: #334155;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="app-header">🎙️ Voice-Activated Personal Assistant</div>', unsafe_allow_html=True)
st.markdown("##### A modular, voice-capable intelligent assistant powered by Google Gemini.")

# Initialize Session State Variables
if "status" not in st.session_state:
    st.session_state.status = "🟢 Ready"
if "transcript" not in st.session_state:
    st.session_state.transcript = "(No speech received)"
if "response" not in st.session_state:
    st.session_state.response = "(No response yet)"
if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = False

# Status Indicator Display
status_placeholder = st.empty()
status_placeholder.markdown(
    f'<div class="status-pill">Status: {st.session_state.status}</div>',
    unsafe_allow_html=True
)

# Initialize conversation memory in session state
initialize_memory()

# -----------------------------
# Sidebar Setup
# -----------------------------
with st.sidebar:
    st.markdown("## 🎙️ Voice Assistant")
    st.markdown("---")
    
    st.markdown("### Architecture")
    st.markdown("✔ **Gemini 2.5 Flash**")
    st.markdown("✔ **Conversation Memory**")
    st.markdown("✔ **Google Search Grounding**")
    st.markdown("✔ **Modular Design**")
    
    st.markdown("---")
    
    st.markdown("### Features")
    st.markdown("- **🤖 Google Gemini** (Active)")
    st.markdown("- **🧠 Conversation Memory** (Active)")
    st.markdown("- **🔍 Google Search Grounding** (Active)")
    st.markdown("- **🎙️ Speech Recognition** (Active)")
    st.markdown("- **🔊 Text-to-Speech** *(Coming Soon)*")
    st.markdown("- **⚡ Voice Commands** *(Coming Soon)*")
    
    st.markdown("---")
    if st.button("Clear Conversation History", use_container_width=True):
        clear_memory()
        st.session_state.transcript = "(No speech received)"
        st.session_state.response = "(No response yet)"
        st.session_state.conversation_active = False
        if "success_message" in st.session_state:
            del st.session_state.success_message
        if "warning_message" in st.session_state:
            del st.session_state.warning_message
        st.success("Conversation history cleared.")
        st.rerun()

# -----------------------------
# Transcript & Assistant Containers
# -----------------------------
st.subheader("Transcript")
transcript_container = st.empty()
with transcript_container.container():
    st.markdown(
        f'<div class="container-box">{st.session_state.transcript}</div>',
        unsafe_allow_html=True
    )

st.subheader("Assistant")
response_container = st.empty()
with response_container.container():
    st.markdown(
        f'<div class="container-box">{st.session_state.response}</div>',
        unsafe_allow_html=True
    )

# Display feedback messages (warnings/success) if present
if "success_message" in st.session_state:
    st.success(st.session_state.success_message)
if "warning_message" in st.session_state:
    st.warning(st.session_state.warning_message)

# -----------------------------
# Control Button
# -----------------------------
st.markdown("---")
if st.button("🎙️ Start Listening", use_container_width=True, type="primary"):
    # Clear previous feedback states
    if "success_message" in st.session_state:
        del st.session_state.success_message
    if "warning_message" in st.session_state:
        del st.session_state.warning_message

    # Helper function to update status live during the listen process
    def update_status(new_status):
        if new_status == "🤔 Processing...":
            display_status = "🤔 Processing"
        elif new_status == "🎤 Listening...":
            display_status = "🎤 Listening"
        else:
            display_status = new_status
            
        st.session_state.status = display_status
        status_placeholder.markdown(
            f'<div class="status-pill">Status: {st.session_state.status}</div>',
            unsafe_allow_html=True
        )

    # Call the speech recognition module
    import core.speech as speech
    text, error_code = speech.listen(status_callback=update_status)

    # Process final result
    if text is not None and text.strip() != "":
        st.session_state.transcript = text
        st.session_state.success_message = "✅ Speech recognized successfully."
        
        # Transition status to Thinking
        update_status("🧠 Thinking")
        
        # Add message to conversation memory (Design B: UI Layer manages memory)
        memory.add_message("user", text)
        
        try:
            import assistant
            response = assistant.process_input(text)
            st.session_state.response = response
            
            # Add message to conversation memory (Design B)
            memory.add_message("model", response)
        except Exception as e:
            logger.exception("Gemini request failed.")
            error_str = str(e)
            if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                st.session_state.response = (
                    "⚠ Gemini API quota exceeded.\n\n"
                    "Please wait a short time and try again,\n"
                    "or use another API key."
                )
                st.session_state.warning_message = "⚠ Gemini API quota exceeded."
            else:
                st.session_state.response = "Unable to generate a response."
                st.session_state.warning_message = "⚠ Gemini request failed."
    else:
        st.session_state.transcript = "(No speech received)"
        st.session_state.response = "(No response yet)"
        if error_code == speech.ERROR_TIMEOUT:
            st.session_state.warning_message = "⚠ No speech detected."
        elif error_code == speech.ERROR_UNRECOGNIZED:
            st.session_state.warning_message = "⚠ Unable to recognize speech."
        elif error_code == speech.ERROR_MICROPHONE:
            st.session_state.warning_message = "⚠ Microphone unavailable."
        elif error_code == speech.ERROR_REQUEST_FAILED:
            st.session_state.warning_message = "⚠ Recognition service error."

    # Restore ready status
    update_status("🟢 Ready")
    st.rerun()
