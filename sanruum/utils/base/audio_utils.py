from __future__ import annotations

from typing import cast

import pyttsx3
import speech_recognition as sr

from sanruum.utils.base.logger import logger


def listen(timeout: float = 5, microphone: sr.Microphone | None = None) -> str:
    """
    Listen to audio input and return recognized text using Google Speech Recognition.

    Accepts an optional `microphone` parameter to allow injection of a dummy microphone
    (useful for testing environments without an audio device).
    """
    r = sr.Recognizer()
    if microphone is None:
        try:
            microphone = sr.Microphone()
        except OSError as e:
            logger.error('No default input device available: %s', e)
            return ''
    with microphone as source:
        print('Listening...')
        try:
            audio = r.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            logger.error('Listening timed out. No speech detected.')
            return ''
        except Exception as e:
            logger.error(f'Error during listening: {e}')
            return ''
    try:
        result = r.recognize_google(audio)
        return cast(str, result)
    except sr.UnknownValueError:
        logger.error('Google Speech Recognition could not understand the audio')
        return ''
    except sr.RequestError as e:
        logger.error(f'Google Speech Recognition service error: {e}')
        return ''


def speak(text: str) -> None:
    """Convert text to speech and play it."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logger.error(f'Error in text-to-speech: {e}')
