import pyttsx3
import speech_recognition as sr
from src.core.logger import Logger


logger = Logger(__name__).get_logger()


class Speech:
    def __init__(self, language: str = "en-US") -> None:
        self.logger = logger
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)
        self.language = language

    def speak(self, text: str) -> None:
        self.logger.debug(f"Speaking text: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def get_audio(self) -> str:
        self.logger.info("Listening for audio input...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.logger.debug("Microphone opened for listening")
            audio = recognizer.listen(source)
        try:
            # Use Google Speech Recognition with Romanian language
            recognized_text = recognizer.recognize_google(audio, language=self.language).lower()  # type: ignore
            self.logger.info(f"Recognized audio: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            self.logger.warning("Speech recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            self.logger.error(f"Error with speech recognition service: {e}")
            return ""