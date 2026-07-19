# Voice-Activated Personal Assistant

A modular, voice-activated personal assistant built with Python, Streamlit, and Google Gemini AI. The application combines speech recognition, intelligent command routing, generative AI, text-to-speech, weather updates, news retrieval, and voice reminders into an interactive assistant with a clean, modular architecture.

---

## Features

- 🎤 **Speech Recognition** using SpeechRecognition and PyAudio
- 🧠 **Google Gemini AI** integration with Google Search Grounding
- 💬 **Conversation Memory** for contextual interactions
- 🔊 **Text-to-Speech (TTS)** using pyttsx3
- 🌤️ **Real-Time Weather** information
- 📰 **Latest News** by category
- 🕒 **Time & Date** commands
- ⏰ **Voice Reminders** with background scheduling
- 🧩 **Modular Architecture** with separated components
- 📝 **Centralized Logging & Error Handling**

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Programming Language | Python 3 |
| AI Model | Google Gemini 2.5 Flash |
| Speech Recognition | SpeechRecognition, PyAudio |
| Text-to-Speech | pyttsx3 |
| APIs | Google Gemini API, OpenWeather API, NewsAPI |
| Configuration | python-dotenv |

---

## Project Architecture

The application follows a modular architecture where each component has a single responsibility.

```text
Voice-Activated-Personal-Assistant/
│
├── app.py                  # Streamlit user interface
├── assistant.py            # Main assistant orchestrator
├── config.py               # Configuration loader
├── requirements.txt
├── README.md
├── LICENSE
├── .env.example
│
├── core/
│   ├── __init__.py
│   ├── speech.py           # Speech recognition engine
│   ├── gemini_client.py    # Gemini API client
│   ├── memory.py           # Conversation history
│   ├── tts.py              # Text-to-Speech engine
│   ├── commands.py         # Command routing
│   ├── reminder.py         # Voice reminder scheduler
│   ├── logger.py           # Centralized logging
│   └── utils.py            # Utility functions
│
├── assets/
└── recordings/
```

---

## Supported Voice Commands

### AI Assistant

- Explain quantum computing.
- Tell me a joke.
- Who invented Python?
- Summarize artificial intelligence.

### Time & Date

- What time is it?
- What's today's date?

### Weather

- What's the weather?
- What's the weather in Mumbai?
- Weather in Delhi.

### News

- Technology news.
- Sports news.
- Business news.

### Voice Reminders

- Remind me to drink water in 30 seconds.
- Remind me to stand up in 2 minutes.
- Remind me to call Mom in 5 minutes.

---

## Project Progress

- ✅ Project Architecture
- ✅ Speech Recognition
- ✅ Google Gemini Integration
- ✅ Conversation Memory
- ✅ Text-to-Speech
- ✅ Weather Commands
- ✅ News Commands
- ✅ Time & Date Commands
- ✅ Voice Reminder Scheduling
- ✅ Modular Command Routing
- ✅ Logging & Error Handling

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Voice-Activated-Personal-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file:

```bash
cp .env.example .env
```

Add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key

OPENWEATHER_API_KEY=your_openweather_api_key

NEWS_API_KEY=your_newsapi_key
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

---

## PyAudio Troubleshooting (macOS)

If PyAudio fails to build because PortAudio is missing:

```bash
conda install -c conda-forge portaudio
```

Then reinstall the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Future Improvements

Potential enhancements include:

- Calendar integration
- Email support
- Desktop notifications
- Persistent reminder storage
- Natural language date/time reminders
- Smart home integration
- Multi-language speech recognition

---

## License

This project is licensed under the MIT License.

---

## Author

Developed as part of a **Voice-Activated Personal Assistant** internship project using Python, Streamlit, and Google Gemini AI.
