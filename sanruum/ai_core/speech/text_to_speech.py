from __future__ import annotations

import os
from typing import Any

import pygame
from pydub import AudioSegment
from pydub.playback import play

from sanruum.constants import OUTPUT_MP3_FILE


def play_audio(file_path: Any, method: str = 'pygame') -> None:
    """Plays an audio file using the specified method.

    Supported methods:
      - 'pygame': Uses pygame.mixer for playback.
      - 'pydub': Uses pydub.playback.
      - 'system': Uses ffplay via a system command.
    """
    if method == 'pygame':
        try:
            # Ensure the mixer is initialized only once
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f'Error playing audio with pygame: {e}')
    elif method == 'pydub':
        try:
            sound = AudioSegment.from_file(file_path, format='mp3')
            play(sound)
        except Exception as e:
            print(f'Error playing audio with pydub: {e}')
    elif method == 'system':
        try:
            # Enclose file_path in quotes in case the path contains spaces
            os.system(f'ffplay -nodisp -autoexit "{file_path}"')
        except Exception as e:
            print(f'Error playing audio with system command: {e}')
    else:
        raise ValueError('Unsupported playback method')


# Example usage
if __name__ == '__main__':
    play_audio(OUTPUT_MP3_FILE, method='pygame')
