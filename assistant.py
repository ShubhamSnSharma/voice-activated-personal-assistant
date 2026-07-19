"""
Assistant Orchestrator Module.
Coordinates speech recognition, command parsing, Gemini model querying, and Text-to-Speech output.
"""

from core import gemini_client, commands, tts
from core.logger import logger

def process_input(text: str) -> str:
    """
    Main processing pipeline.

    Flow:
        User Text
            ↓
        Local Commands
            ↓
    handled?
       │
       ├── Yes → return command response
       │
       └── No
             ↓
          Gemini
             ↓
       return AI response
    """
    # 1. Check local voice commands (placeholder/structural routing)
    handled, command_response = commands.execute(text)
    if handled and command_response is not None:
        logger.info("Command handled locally.")
        tts.speak(command_response)
        return command_response

    # 2. Retrieve response from Gemini client
    logger.info("Sending request to Gemini")
    ai_response = gemini_client.get_response(text)
    logger.info("Response received")
    
    # 3. Speak response
    tts.speak(ai_response)
    
    return ai_response
