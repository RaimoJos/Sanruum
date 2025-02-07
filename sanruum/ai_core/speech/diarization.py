# sanruum\ai_core\speech\diarization.py

from typing import Any

from pyannote.audio import Pipeline

from sanruum.utils.logger import logger


class SpeakerDiarization:
    def __init__(self, model: str = "pyannote/speaker-diarization") -> None:
        try:
            self.pipeline: Any = Pipeline.from_pretrained(model)
            logger.info(
                f"Speaker diarization model '{model}' loaded successfully."
            )
        except Exception as e:
            logger.error(f"Failed to load diarization model: {e}")
            raise

    def diarize(self, audio_path: str) -> Any:
        """Identify speakers in an audio file."""
        try:
            diarization = self.pipeline(audio_path)
            logger.info(f"Diarization successful for: {audio_path}")
            return diarization
        except Exception as e:
            logger.error(f"Diarization failed for {audio_path}: {e}")
            return None
