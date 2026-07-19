from __future__ import annotations
import speech_recognition as sr
from config import (
    SPEECH_LANGUAGE,
    SPEECH_TIMEOUT,
    PHRASE_TIME_LIMIT,
    AMBIENT_NOISE_DURATION,
    PAUSE_THRESHOLD,
    NON_SPEAKING_DURATION,
    ENERGY_THRESHOLD
)
from core.logger import logger

# Speech error constants
ERROR_MICROPHONE = "microphone_unavailable"
ERROR_TIMEOUT = "timeout"
ERROR_UNRECOGNIZED = "unrecognized"
ERROR_REQUEST_FAILED = "request_failed"

def _recognize(recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
    """Helper wrapper for the speech-to-text service call."""
    return recognizer.recognize_google(audio, language=SPEECH_LANGUAGE)  # type: ignore

def listen(*, status_callback=None) -> tuple[str | None, str | None]:
    """
    Listen to user audio input and return (text, error_code).
    Handles ambient noise calibration, timeouts, and recognition errors.
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = PAUSE_THRESHOLD
    recognizer.non_speaking_duration = NON_SPEAKING_DURATION
    recognizer.energy_threshold = ENERGY_THRESHOLD
    recognizer.dynamic_energy_threshold = True
    
    try:
        logger.info("Initializing microphone")
        mic = sr.Microphone()
    except Exception as e:
        logger.error(f"Microphone unavailable. Error: {str(e)}")
        return None, ERROR_MICROPHONE
        
    try:
        with mic as source:
            if status_callback:
                status_callback("🎤 Listening...")
            logger.info("Calibrating ambient noise")
            recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_NOISE_DURATION)
            logger.info(f"Energy threshold: {recognizer.energy_threshold}")
            
            logger.info("Listening")
            audio = recognizer.listen(
                source,
                timeout=SPEECH_TIMEOUT,
                phrase_time_limit=PHRASE_TIME_LIMIT
            )
            logger.info("Speech capture complete")
            if status_callback:
                status_callback("🤔 Processing...")
            logger.info("Processing speech")
    except sr.WaitTimeoutError:
        logger.error("Listening timed out.")
        return None, ERROR_TIMEOUT
    except Exception as e:
        logger.error(f"Microphone unavailable. Error: {str(e)}")
        return None, ERROR_MICROPHONE

    try:
        text = _recognize(recognizer, audio)
        logger.info("Speech recognized.")
        return text, None
    except sr.UnknownValueError:
        logger.error("Speech could not be understood.")
        return None, ERROR_UNRECOGNIZED
    except sr.RequestError as e:
        logger.error(f"Recognition request failure. Error: {str(e)}")
        return None, ERROR_REQUEST_FAILED
