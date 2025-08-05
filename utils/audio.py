"""Audio utilities."""
from __future__ import annotations

from moviepy import AudioFileClip


def load_audio(audio_path: str) -> AudioFileClip:
    """Load audio file and return ``AudioFileClip``."""
    return AudioFileClip(audio_path)
