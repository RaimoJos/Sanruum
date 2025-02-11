# sanruum\ai_core\speech\text_to_speech.py
from __future__ import annotations

import os
from typing import Any

import pygame
from pydub import AudioSegment
from pydub.playback import play

from sanruum.constants import OUTPUT_MP3_FILE


def play_audio(filename: Any, method: str = 'pygame') -> Any:
    """Plays an audio file using the specified method."""
    if method == 'pygame':
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    elif method == 'pydub':
        sound = AudioSegment.from_file(filename, format='mp3')
        play(sound)
    elif method == 'system':
        os.system(f'ffplay -nodisp -autoexit {filename}')
    else:
        raise ValueError('Unsupported playback method')


# Example usage
if __name__ == '__main__':
    filename = OUTPUT_MP3_FILE
    play_audio(filename, method='pygame')
