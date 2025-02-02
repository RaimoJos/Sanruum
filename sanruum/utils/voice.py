import pyttsx3
import speech_recognition as sr

from sanruum.utils.logger import logger

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the speaking rate (lower values slow down the speech)
engine.setProperty('volume', 1.0)  # Set volume level (0.0 to 1.0)
voices = engine.getProperty('voices')

# Ensure voices is a list before indexing
if isinstance(voices, list) and voices:
    preferred_voice = voices[1].id if len(voices) > 1 else voices[0].id
    engine.setProperty('voice', preferred_voice)


def listen() -> str:
    """Capture voice input and return recognized text."""
    recognizer: sr.Recognizer = sr.Recognizer()  # Explicit type hint
    with sr.Microphone() as source:
        logger.debug("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + text)

        return text
    except sr.UnknownValueError:
        logger.error("Could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""


def speak(text: str) -> None:
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()
