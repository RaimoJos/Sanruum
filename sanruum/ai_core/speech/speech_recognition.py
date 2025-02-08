# sanruum\ai_core\speech\speech_recognition.py
from __future__ import annotations

import speech_recognition as sr
import whisper

from sanruum.utils.logger import logger

# Workaround for recognize_google issue
try:
    from speech_recognition.recognizers import google
except (ModuleNotFoundError, ImportError):
    pass
else:
    sr.Recognizer.recognize_google = google.recognize_legacy


class SpeechRecognition:
    def __init__(self, engine: str = 'whisper', timeout: int = 5) -> None:
        self.engine: str = engine
        self.recognizer: sr.Recognizer = sr.Recognizer()
        self.microphone: sr.Microphone = sr.Microphone()
        self.timeout = timeout  # Timeout after X seconds

        if self.engine == 'whisper':
            self.model = whisper.load_model('base')

    def recognize_speech(self) -> str:
        """
        Capture voice input and convert to text using the selected engine.
        """
        with self.microphone as source:
            print('Listening...')
            try:
                audio: sr.AudioData = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                )
            except sr.WaitTimeoutError:
                logger.error('Listening timed out. No speech detected.')
                return ''
            except Exception as e:
                logger.error(f'Error during listening: {e}')
                return ''

        if self.engine == 'google':
            return self._recognize_google(audio)
        elif self.engine == 'whisper':
            return self._recognize_whisper(audio)
        else:
            logger.error(f'Unsupported STT engine: {self.engine}')
            return ''

    def _recognize_google(self, audio: sr.AudioData) -> str:
        """Recognize speech using Google Speech Recognition."""
        try:
            text: str = self.recognizer.recognize_google(audio)
            logger.info(f'Google Speech Recognition thinks you said: {text}')
            return text
        except sr.UnknownValueError:
            logger.error(
                'Google Speech Recognition could not understand the audio',
            )
            return ''
        except sr.RequestError as e:
            logger.error(f'Google Speech Recognition service error: {e}')
            return ''

    def _recognize_whisper(self, audio: sr.AudioData) -> str:
        """Recognize speech using OpenAI's Whisper model."""
        try:
            audio_data = audio.get_wav_data()
            result = self.model.transcribe(audio_data)
            text: str = result['text']
            logger.info(f'Whisper thinks you said: {text}')
            return text
        except Exception as e:
            logger.error(f'Whisper recognition error: {e}')
            return ''
