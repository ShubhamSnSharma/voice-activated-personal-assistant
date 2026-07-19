import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Speech recognition configuration
SPEECH_LANGUAGE = "en-US"
SPEECH_TIMEOUT = 5
PHRASE_TIME_LIMIT = 10
AMBIENT_NOISE_DURATION = 1.0

# Speech recognition stability settings
PAUSE_THRESHOLD = 1.2
NON_SPEAKING_DURATION = 0.6
ENERGY_THRESHOLD = 300

# Text-to-Speech configuration
TTS_RATE = 180
TTS_VOLUME = 1.0
TTS_VOICE = None

# External APIs
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

DEFAULT_CITY = "Delhi"
DEFAULT_NEWS_COUNTRY = "in"





