"""
Reminder scheduling and handling module.
"""

import re
import threading
from core import tts
from core.logger import logger

# Global registry of active background timers
_active_reminders: list[threading.Timer] = []

def _trigger(task: str) -> None:
    """Trigger voice and logging output when a reminder expires."""
    logger.info(f"Reminder triggered: '{task}'")
    tts.speak(f"Reminder: {task}")

def handle(text: str) -> tuple[bool, str | None]:
    """
    Check if the query matches a reminder command.
    If matched, parse and schedule the background reminder.
    """
    if not text:
        return False, None
        
    text_lower = text.lower().strip()
    if "remind" not in text_lower:
        return False, None
        
    # Match pattern: case-insensitive but extracting original task casing
    match = re.search(r"remind me to (.+?) in (\d+)\s+(second|minute)s?", text, re.IGNORECASE)
    if not match:
        # Check for unsupported temporal terms specifically
        unsupported_terms = ["tomorrow", "next week", "next month", "every day", "daily", "hourly", "every"]
        if any(term in text_lower for term in unsupported_terms):
            return True, "I currently support reminders using seconds or minutes."
        return True, "Sorry.\n\nPlease say something like\n\"Remind me to drink water in 10 minutes.\""
        
    task = match.group(1).strip()
    duration_val = int(match.group(2))
    unit = match.group(3).lower().strip()
    
    if duration_val <= 0:
        return True, "Reminder duration must be greater than zero."
        
    # Calculate delay in seconds
    delay_seconds = duration_val
    if "minute" in unit:
        delay_seconds = duration_val * 60
        
    try:
        logger.info("Reminder created")
        
        def timer_callback(timer_ref):
            _trigger(task)
            try:
                _active_reminders.remove(timer_ref)
            except ValueError:
                pass
                
        timer = threading.Timer(
            delay_seconds,
            lambda: timer_callback(timer)
        )
        timer.daemon = True
        _active_reminders.append(timer)
        timer.start()
        
        logger.info(f"Reminder scheduled: '{task}' in {delay_seconds} seconds.")
        
        # Format display string
        unit_str = f"{duration_val} {unit}"
        if duration_val > 1:
            unit_str += "s"
            
        response = f"Okay.\n\nI'll remind you to {task} in {unit_str}."
        return True, response
    except Exception as e:
        logger.exception("Error scheduling background reminder.")
        return True, "Sorry, I had trouble scheduling the reminder."
