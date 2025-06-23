from importlib import import_module
import random
import time
from src.core.constants import WAKE_WORDS, CALENDAR, FUNFACT, QUESTION_KEYWORD, TIME, WEATHER, TIME
from src.core.logger import Logger
from src.core.speech import Speech
from src.data.commands import commands, replies, q_and_a

class Recognizer:
    def __init__(self):
        self.logger = Logger(__name__).get_logger()
        self.speech = Speech()
        self.calendar_service = None
        self.time_service = None
        # self.weather_service = None

    def lazy_load_calendar_service(self):
        if not self.calendar_service:
            self.logger.debug("Lazy loading CalendarService")
            calendar_module = import_module("src.flows.calendar_flow")
            self.calendar_service = calendar_module.CalendarService()
    
    def lazy_load_time_service(self):
        if not self.time_service:
            self.logger.debug("Lazy loading TimeService")
            time_module = import_module("src.flows.time_flow")
            self.time_service = time_module.TimeService()

    def process_command(self, data: str) -> None:
        """
        Process the recognized command and respond accordingly.

        Args:
            data (str): The recognized command text.
        """
        self.logger.debug(f"Processing command: {data}")
        if not data:
            self.logger.warning("No command detected")
            self.speech.speak("I didn't hear you, Sir! Please repeat.")
            return

        def handle_calendar():
            self.lazy_load_calendar_service()
            self.logger.info("Calendar command detected")
            self.speech.speak("Opening calendar, Sir!")
            message_to_speak = self.calendar_service.get_calendar_events(data.split()) # type: ignore
            self.speech.speak(message_to_speak)

        def handle_time():
            self.lazy_load_time_service()
            self.logger.info("Time command detected")
            self.speech.speak("Opening time, Sir!")
            message_to_speak = self.time_service.get_time_info(data.split()) # type: ignore
            self.speech.speak(message_to_speak)

        def handle_weather():
            self.logger.info("Weather command detected")
            self.speech.speak("Opening weather, Sir!")
            # Add weather logic here

        def handle_question():
            self.logger.info("Question command detected")
            self.speech.speak("What is your question, Sir?")
            question = self.speech.get_audio()
            if question:
                self.logger.debug(f"Recognized question: {question}")
                if question in q_and_a.keys():
                    self.speech.speak(q_and_a[question])
                else:
                    for key in q_and_a.keys():
                        if question in key:
                            self.speech.speak(q_and_a[key])
                            return
                    self.speech.speak("I don't have an answer for that, Sir!")
            else:
                self.logger.warning("No question detected")
                self.speech.speak("I didn't hear your question, Sir!")

        def handle_funfact():
            self.logger.info("Fun fact command detected")
            self.speech.speak("Fetching a fun fact for you, Sir!")
            choices = list(q_and_a.values())
            random.shuffle(choices)
            self.speech.speak(random.choice(choices))

        def handle_predefined():
            self.logger.info("Searching for matching command in predefined replies")
            for command, reply_list in commands.items():
                if data in reply_list:
                    self.speech.speak(random.choice(replies[command]))
                    return True
            return False

        # Command handler mapping
        command_handlers = [
            (lambda d: CALENDAR in d, handle_calendar),
            (lambda d: TIME in d, handle_time),
            (lambda d: WEATHER in d, handle_weather),
            (lambda d: QUESTION_KEYWORD in d, handle_question),
            (lambda d: FUNFACT in d, handle_funfact),
        ]

        for condition, handler in command_handlers:
            if condition(data):
                handler()
                self.logger.info("Command processed successfully")
                return

        if handle_predefined():
            self.logger.info("Command processed successfully")
            return

        self.logger.warning("Unrecognized command")
        self.speech.speak("I'm sorry, Sir! I did not understand your request, Sir!")
        self.logger.info("Command processed successfully")

    def start(self) -> None:
        """
        Start the speech recognizer and process commands.
        """
        self.logger.info(f"Waiting for wake words: {WAKE_WORDS}")
        while True:
            try:
                data = self.speech.get_audio()
                if any(wake_word in data for wake_word in WAKE_WORDS):
                    self.logger.info("Wake word detected")
                    self.speech.speak("Yes, Sir?")
                    command = self.speech.get_audio()
                    self.process_command(command)
            except Exception as e:
                self.logger.error("Error in recognizer loop: %s", e)
            time.sleep(1)