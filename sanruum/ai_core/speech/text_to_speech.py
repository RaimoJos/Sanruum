# sanruum\ai_core\speech\text_to_speech.py
import os
import tempfile
from typing import Optional, Any

import gtts
import pyttsx3

from sanruum.utils.logger import logger


class TextToSpeech:
    def __init__(self, engine: str = "pyttsx3", language: str = "en") -> None:
        self.engine: str = engine
        self.language: str = language
        self.speaker: Optional[Any] = None

        if self.engine == "pyttsx3":
            self.speaker = pyttsx3.init()
            self.speaker.setProperty("rate", 150)
            self.speaker.setProperty("volume", 1.0)

    def speak(self, text: str) -> None:
        """Convert text tp speech."""
        if self.engine == "pyttsx3":
            self._speak_pyttsx3(text)
        elif self.engine == "gtts":
            self._speak_gtts(text)
        else:
            logger.error(f"Unsupported TTS engine: {self.engine}")

    def _speak_pyttsx3(self, text: str) -> None:
        """Offline TTS using pyttsx3."""
        if self.speaker:
            self.speaker.say(text)
            self.speaker.runAndWait()

    def _speak_gtts(self, text: str) -> None:
        """Google TTS (Generates audio file and plays it)."""
        tts = gtts.gTTS(text, lang=self.language)
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            filename = temp_file.name
            tts.save(filename)
            os.system(f"mpg321 {filename}")
            # Cleanup the temporary file after playing it
            os.remove(filename)
