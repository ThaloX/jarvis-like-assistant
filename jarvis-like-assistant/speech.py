import pyttsx3
import speech_recognition as sr


def speak(text: str) -> None:
    """
    Speak the given text using the pyttsx3 text-to-speech engine.

    Args:
        text (str): The text to be spoken.
    """
    rate = 150
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

def get_audio() -> str:
    """
    Capture audio from the microphone and return the recognized text.

    Returns:
        str: The recognized text from the audio.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower() # type: ignore
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Error with speech recognition service: {e}")
        return ""