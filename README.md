# Jarvis-Like Assistant

A voice-activated assistant that integrates with Google Calendar, provides answers to predefined questions, and performs various tasks such as fetching fun facts, responding to greetings, and more.

---

## Features

### Core Functionalities

- **Speech Recognition**: Uses `speech_recognition` to capture and process voice commands.
- **Text-to-Speech**: Uses `pyttsx3` to provide voice responses.
- **Google Calendar Integration**:
  - Fetches events for specific dates (e.g., "today," "tomorrow," or specific dates like "20 May").
  - Retrieves upcoming events.
- **Predefined Commands**:
  - Responds to greetings, farewells, and small talk.
  - Provides fun facts and answers to predefined questions.
- **Dynamic Command Handling**:
  - Commands and replies are loaded dynamically from CSV files (`input.csv` and `q_and_a.csv`).
- **Wake Words**:
  - Activates on hearing "hey assistant," "hello assistant," or "assistant."

### Utilities

- **CSV Management**:
  - Sorts and organizes commands in `input.csv` by category.
  - Removes duplicate lines from CSV files.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry for dependency management
- A Google Cloud project with the Google Calendar API enabled
- `credentials.json` file for Google Calendar API authentication

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/jarvis-like-assistant.git
   cd jarvis-like-assistant
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Place the `credentials.json` file in the `user_data` folder:

   ```text
   user_data/credentials.json
   ```

4. Run the application:

   ```bash
   poetry run python main.py
   ```

---

## Requirements

### Python Libraries (Managed by Poetry)

- `pyttsx3`: For text-to-speech functionality.
- `speechrecognition`: For speech recognition.
- `pyaudio`: For capturing audio input.
- `pocketsphinx`: For offline speech recognition.
- `google-api-python-client`: For Google Calendar API integration.
- `google-auth-oauthlib`: For Google OAuth2 authentication.
- `google-auth-httplib2`: For HTTP transport with Google APIs.
- `colorlog`, `pytz`, `tzlocal`: For logging and timezone support.

### System Requirements

- A working microphone for voice input.
- Internet connection for Google Calendar API and online speech recognition.

---

## File Structure

```text
jarvis-like-assistant/
├── main.py                        # Entry point of the application
├── pyproject.toml                 # Poetry dependencies and metadata
├── LICENSE                        # License file
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore file
├── .python-version                # Python version file
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── constants.py           # Application constants (wake words, etc.)
│   │   ├── logger.py              # Logger configuration
│   │   ├── recognizer.py          # Processes voice commands and routes to services
│   │   ├── speech.py              # Handles speech recognition and text-to-speech
│   ├── data/
│   │   ├── __init__.py
│   │   ├── commands.py            # Handles commands, replies, and Q&A loading
│   │   ├── utils.py               # Utility functions for CSV management
│   ├── flows/
│   │   ├── __init__.py
│   │   ├── calendar_flow.py       # Google Calendar integration and logic
│   │   ├── time_flow.py           # Time/date/week info logic
├── user_data/
│   ├── credentials.json           # Google Calendar API credentials (not tracked)
│   ├── token.json                 # OAuth2 token for Google Calendar API (not tracked)
│   ├── input.csv                  # Commands and replies (not tracked)
│   ├── q_and_a.csv                # Predefined questions and answers (not tracked)
├── tests/
│   ├── test_data.py               # Tests for data/commands
│   ├── test_logger.py             # Tests for logger
│   ├── test_speech.py             # Tests for speech
│   ├── test_time_flow.py          # Tests for time flow
│   ├── test_utils.py              # Tests for utils
```

- All core logic is under `src/`.
- User data and credentials are stored in `user_data/` (excluded by `.gitignore`).
- All tests are in the `tests/` directory.

---

## Usage

### Wake Words

The assistant activates when it hears any of the following:

- "hey assistant"
- "hello assistant"
- "assistant"

### Commands

- **Google Calendar**:
  - "What are my events for today?"
  - "What are my upcoming events?"
- **Fun Facts**:
  - "Tell me a fun fact."
  - "Do you know any fun facts?"
- **Predefined Questions**:
  - "Who invented the telephone?"
  - "What is the capital of France?"

### CSV Management

- To sort and organize commands in `input.csv`, use the `sort_by_categories` function in `utils.py`.
- To remove duplicate lines from a file, use the `remove_duplicate_lines` function in `utils.py`.

---

## Testing

To run all tests using pytest:

```bash
# Make sure you are in the project root
poetry run pytest
```

If you encounter import errors, set the `PYTHONPATH` to the project root:

```bash
set PYTHONPATH=%CD%
poetry run pytest
```
Or in PowerShell:
```powershell
$env:PYTHONPATH = $PWD
poetry run pytest
```

---

## Notes

- Ensure the `credentials.json` file is correctly configured and placed in the `user_data` folder.
- The assistant requires an active internet connection for Google Calendar API and online speech recognition.
- You can add or modify commands and replies by editing the `input.csv` and `q_and_a.csv` files.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Author

Developed by Vlad Bugnariu.