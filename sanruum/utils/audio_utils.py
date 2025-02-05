# sanruum\utils\audio_utils.py
# audio_utils.py

from typing import cast

import pyttsx3
import speech_recognition as sr

from sanruum.utils.logger import logger


def listen() -> str:
    """Capture audio and convert to text using speech recognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text: str = cast(str, recognizer.recognize_google(audio))  # Force str return type
            return text
        except sr.WaitTimeoutError:
            logger.warning("⏳ Listening timed out.")
            return ""
        except sr.UnknownValueError:
            logger.warning("🛑 Could not understand audio.")
            return ""
        except sr.RequestError:
            logger.error("🔗 Speech recognition service unavailable.")
            return ""


def speak(text: str) -> None:
    """Convert text to speech and play it."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")


if __name__ == "__main__":
    print("Testing audio functions...")
    text = listen()
    print(f"You said: {text}")
    speak("This is a test response.")
