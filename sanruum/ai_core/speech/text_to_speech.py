from __future__ import annotations

import os
from typing import Any

import pygame
from pydub import AudioSegment
from pydub.playback import play

from sanruum.constants import OUTPUT_MP3_FILE


def play_audio(filename: Any, method: str = 'pygame') -> None:
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
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f'Error playing audio with pygame: {e}')
    elif method == 'pydub':
        try:
            sound = AudioSegment.from_file(filename, format='mp3')
            play(sound)
        except Exception as e:
            print(f'Error playing audio with pydub: {e}')
    elif method == 'system':
        try:
            # Enclose filename in quotes in case the path contains spaces
            os.system(f'ffplay -nodisp -autoexit "{filename}"')
        except Exception as e:
            print(f'Error playing audio with system command: {e}')
    else:
        raise ValueError('Unsupported playback method')


# Example usage
if __name__ == '__main__':
    filename = OUTPUT_MP3_FILE
    play_audio(filename, method='pygame')
