from typing import Any

from pyannote.audio import Pipeline


class SpeakerDiarization:
    def __init__(self, model: str = "pyannote/speaker-diarization") -> None:
        self.pipeline: Any = Pipeline.from_pretrained(model)

    def diarize(self, audio_path: str) -> Any:
        """Identify speakers in an audio file."""
        diarization = self.pipeline(audio_path)
        return diarization
