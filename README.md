# Voice-Activated Personal Assistant

A modular, voice-capable intelligent assistant built in Python and powered by Google Gemini. The project provides a modular architecture separating audio capture, speech recognition, command parsing, AI generation, and Text-to-Speech (TTS) response.

## Technology Stack

- **Frontend**: Streamlit
- **AI Engine**: Google Gemini API (gemini-2.5-flash)
- **Speech Capabilities**: Custom pipelines (Coming soon in subsequent milestones)
- **Core Library**: python-dotenv, google-genai

## Project Structure

```text
Voice-Activated-Personal-Assistant/
│
├── app.py                  # Main Streamlit web application
├── assistant.py            # Orchestrator coordinating core pipelines
├── config.py               # Environment configuration loader
├── requirements.txt        # Verified project dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License
├── .env.example            # Template for environment settings
│
├── core/
│   ├── __init__.py         # Core package initialization
│   ├── gemini_client.py    # Self-healing Gemini API client
│   ├── memory.py           # Chat history management
│   ├── speech.py           # Speech recognition placeholder
│   ├── tts.py              # Text-to-Speech placeholder
│   ├── commands.py         # Voice command execution placeholder
│   ├── utils.py            # Utility helpers placeholder
│   └── logger.py           # Centralized Streamlit-safe logging utility
│
├── assets/                 # UI assets, diagrams, and static media
└── recordings/             # Saved speech recordings
```

## Planned Features

- **Google Gemini & Google Search Grounding**: Leverages LLMs with real-time web retrieval.
- **Conversation Memory**: Remembers context across conversation turns.
- **Speech Recognition**: Capture and transcribe microphone input locally or via cloud APIs. The module automatically adapts to background/ambient noise dynamically and supports custom silence thresholds to allow natural speaking pacing.
- **Voice Commands**: Route specific keyword actions locally (e.g. system commands).
- **Text-to-Speech (TTS)**: Verbal response feedback from the assistant.

## Progress Checklist

- [x] Project Architecture
- [x] Speech Recognition
- [x] Gemini Integration
- [x] Text-to-Speech
- [x] Weather Commands
- [x] News Commands
- [x] Reminder Commands

## Roadmap

- **Milestone 1**
  - ✓ Architecture & Modular Scaffolding
- **Milestone 2**
  - ✓ Speech Recognition Integration
- **Milestone 3**
  - ✓ Gemini Integration & Context Handling
- **Milestone 4**
  - ✓ Text-to-Speech Voice Output
- **Milestone 5**
  - ✓ Custom Voice Commands & Routing (Weather, News, Time, Date)
- **Milestone 6**
  - ✓ Voice Reminders (Background Scheduling)

## Example Voice Commands

- "What time is it?"
- "What's today's date?"
- "What's the weather in Mumbai?"
- "Give me technology news."
- "Remind me to drink water in 30 seconds."
- "Explain quantum computing."

## Screenshots

![Assistant Conversation Placeholder](assets/assistant_conversation_placeholder.png)


## PyAudio Troubleshooting (macOS)

If `pyaudio` fails to compile because of system-level issues:
1. Ensure the system `portaudio` package is installed. If using Anaconda:
   ```bash
   conda install -y -c conda-forge portaudio
   ```
2. Re-run `pip install -r requirements.txt`.


## Installation Instructions

1. **Clone or set up the repository**:
   ```bash
   git clone <repository-url>
   cd Voice-Activated-Personal-Assistant
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Copy `.env.example` to `.env` and fill in your Google Gemini API key:
   ```bash
   cp .env.example .env
   ```
   Add your API key:
   ```text
   GEMINI_API_KEY=AIzaSy...
   ```

5. **Run the Application**:
   Launch the Streamlit web interface:
   ```bash
   streamlit run app.py
   ```
