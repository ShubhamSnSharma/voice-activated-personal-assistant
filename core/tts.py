"""
Text-to-Speech (TTS) module.
"""

import pyttsx3
from config import TTS_RATE, TTS_VOLUME, TTS_VOICE
from core.logger import logger

# Initialize the pyttsx3 engine once during module load
_engine = None
try:
    _engine = pyttsx3.init()
    _engine.setProperty("rate", TTS_RATE)
    _engine.setProperty("volume", TTS_VOLUME)
    if TTS_VOICE is not None:
        _engine.setProperty("voice", TTS_VOICE)
except Exception as e:
    logger.exception("Failed to initialize pyttsx3 TTS engine globally.")

def speak(text: str) -> None:
    """
    Convert text to speech and play it synchronously.
    Handles exceptions internally to prevent application crashes.
    """
    if not text or text.strip() == "":
        return
        
    if _engine is None:
        logger.error("TTS engine is not available.")
        return
        
    try:
        logger.info("Speaking response")
        _engine.say(text)
        _engine.runAndWait()
        logger.info("Speech finished")
    except Exception as e:
        logger.exception("Text-to-Speech execution failed.")
