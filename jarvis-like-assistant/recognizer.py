import random
import time
from calendar_flow import CalendarService

from commands import commands, replies, q_and_a
from speech import get_audio, speak

# Constants
WAKE_WORDS = ["hey assistant", "hello assistant", "assistant"]
CALENDAR = "calendar"
FUNFACT = "fun fact"
QUESTION_KEYWORD = "question"
SCHEDULE = "schedule"
WEATHER = "weather"
TIME = "time"

# Initialize CalendarService
calendar_service = CalendarService()

def process_command(data: str) -> None:
    """
    Process the recognized command and respond accordingly.

    Args:
        data (str): The recognized command text.
    """
    print(f"Recognized command: {data}")
    if not data:
        speak("I didn't hear you, Sir! Please repeat.")
        return
    if CALENDAR in data:
        speak("Opening calendar, Sir!")
        message_to_speak = calendar_service.get_calendar_events(data.split())
        speak(message_to_speak)
    elif SCHEDULE in data:
        speak("Opening schedule, Sir!")
        # Add schedule logic here
    elif WEATHER in data:
        speak("Opening weather, Sir!")
        # Add weather logic here
    elif TIME in data:
        speak("Opening time, Sir!")
        # Add time logic here
    elif FUNFACT in data or QUESTION_KEYWORD in data:
        if QUESTION_KEYWORD in data:
            speak("What is your question, Sir?")
            question = get_audio()
            if question:
                print(f"Recognized question: {question}")
                if question in q_and_a.keys():
                    speak(q_and_a[question])
                else:
                    for key in q_and_a.keys():
                        if question in key:
                            speak(q_and_a[key])
                            return
                    speak("I don't have an answer for that, Sir!")
            else:
                speak("I didn't hear your question, Sir!")
        elif FUNFACT in data:
            speak("Fetching a fun fact for you, Sir!")
            choices = list(q_and_a.values())
            random.shuffle(choices)
            speak(random.choice(choices))

    else:
        for command, reply_list in commands.items():
            if data in reply_list:
                speak(random.choice(replies[command]))
                return
        speak("I'm sorry, Sir! I did not understand your request, Sir!")

def start_recognizer() -> None:
    """
    Start the speech recognizer and process commands.
    """
    print(f"Waiting for wake words: {WAKE_WORDS}")
    while True:
        data = get_audio()
        if any(wake_word in data for wake_word in WAKE_WORDS):
            speak("Yes, Sir?")
            command = get_audio()
            process_command(command)
        time.sleep(1)