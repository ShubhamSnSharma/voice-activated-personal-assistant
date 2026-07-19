import streamlit as st
import re
import math
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import GEMINI_API_KEY

MODEL_NAME = "gemini-2.5-flash"
_client = None

# Extensible list of keywords related to real-time events
REALTIME_KEYWORDS = [
    "today", "current", "latest", "now", "right now", "weather", "forecast", "rain", 
    "temperature", "news", "breaking", "stock", "share", "share price", "market", 
    "bitcoin", "ethereum", "crypto", "gold", "silver", "exchange rate", "ipl", 
    "cricket", "football", "score", "election", "traffic", "price", "prices"
]


def get_client():
    """
    Get or initialize the Gemini client lazily.
    """
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def get_chat_session():
    """
    Retrieve or create a session-specific chat session using Streamlit session state.
    Google Search grounding is enabled for this session.
    """
    client = get_client()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
    return st.session_state.chat_session


def needs_realtime(prompt):
    """
    Check if the user is asking for information that changes over time by checking keywords with word boundaries.
    """
    prompt_lower = prompt.lower()
    for keyword in REALTIME_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, prompt_lower):
            return True
    return False


def get_chat_session_with_history(history_messages):
    """
    Retrieve or create a session-specific chat session using custom history.
    """
    client = get_client()
    sdk_history = []
    for msg in history_messages:
        role = msg["role"]
        if role not in ["user", "model"]:
            continue
        content = msg["content"]
        # Skip the static welcome message to avoid polluting API history
        if content.startswith("👋 Hi! I'm your Gemini AI Assistant"):
            continue
        sdk_history.append(
            types.Content(
                role=role,
                parts=[types.Part(text=content)]
            )
        )
    
    st.session_state.chat_session = client.chats.create(
        model=MODEL_NAME,
        history=sdk_history,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    return st.session_state.chat_session


def get_response(prompt):
    """
    Send a message to the session-specific chat and return the response text.
    Handles API errors, rate limits, and network errors gracefully.
    Detects if the query needs real-time search, logs the route selected, 
    and prepends the search instruction if necessary.
    Automatically self-heals/retries if the client is closed.
    """
    try:
        chat = get_chat_session()
        
        # Route logic based on real-time intent
        if needs_realtime(prompt):
            # Prepend hidden instruction encouraging Google Search Grounding
            routed_prompt = (
                "You have access to Google Search.\n\n"
                "If this question depends on current or changing information, retrieve the latest available information using Google Search before answering.\n\n"
                "Do not rely only on internal knowledge when current information is required.\n\n"
                f"User question:\n{prompt}"
            )
        else:
            routed_prompt = prompt

        try:
            response = chat.send_message(routed_prompt)
        except Exception as e:
            # Check if the client has been closed
            if "client has been closed" in str(e).lower() or "client is closed" in str(e).lower():
                # Trigger self-healing recovery flow
                global _client
                _client = None  # Reset client cache
                
                # Fetch history excluding the last user prompt (the current query)
                messages = st.session_state.get("messages", [])
                history_messages = messages[:-1] if len(messages) > 0 else []
                
                # Create a new chat session with history
                chat = get_chat_session_with_history(history_messages)
                
                # Retry sending the current prompt once
                response = chat.send_message(routed_prompt)
            else:
                # Raise other errors to be handled by the outer try-except block
                raise e

        if not response.text:
            raise RuntimeError("Gemini returned an empty response. This might be due to safety filters or blocking.")
        return response.text
    except APIError as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "400" in error_msg:
            raise RuntimeError("Invalid API key. Please check your GEMINI_API_KEY in the .env file.") from e
        elif "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            # Attempt to extract the retry duration using regular expressions
            match = re.search(r"retry in (\d+(?:\.\d+)?)s", error_msg, re.IGNORECASE)
            if match:
                seconds = math.ceil(float(match.group(1)))
                raise RuntimeError(
                    "Google Gemini API rate limit reached.\n\n"
                    "You have reached the free-tier request limit for the Gemini API.\n\n"
                    f"Please wait approximately {seconds} seconds before trying again."
                ) from e
            else:
                raise RuntimeError(
                    "Google Gemini API rate limit reached.\n\n"
                    "You have reached the Gemini API free-tier request limit.\n\n"
                    "Please wait about one minute and try again."
                ) from e
        else:
            raise RuntimeError(f"Gemini API Error: {error_msg}") from e
    except ValueError as e:
        # Re-raise value errors (like missing API key) directly
        raise e
    except Exception as e:
        raise RuntimeError(f"Failed to communicate with Gemini: {str(e)}") from e
