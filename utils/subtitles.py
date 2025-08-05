"""Subtitle generation helpers."""
from __future__ import annotations

import os
import re
from typing import List, Tuple

from moviepy import TextClip
from moviepy.video.tools.subtitles import SubtitlesClip


def default_font_path() -> str | None:
    """Return a system font path if one can be located."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
        "/Library/Fonts/Arial.ttf",  # macOS
        "C:/Windows/Fonts/Arial.ttf",  # Windows
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def _split_sentences(text: str) -> List[str]:
    """Split text into sentences using punctuation marks."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def generate_subtitle_entries(story_text: str, audio_duration: float) -> List[Tuple[Tuple[float, float], str]]:
    """Generate evenly spaced subtitles covering the audio duration."""
    sentences = _split_sentences(story_text)
    if not sentences:
        return []
    dur = audio_duration / len(sentences)
    entries: List[Tuple[Tuple[float, float], str]] = []
    start = 0.0
    for sentence in sentences:
        end = start + dur
        entries.append(((start, end), sentence))
        start = end
    return entries


def create_subtitles_clip(
    subtitles: List[Tuple[Tuple[float, float], str]],
    size: Tuple[int, int],
    font: str | None = None,
    fontsize: int = 40,
    color: str = "white",
) -> SubtitlesClip:
    """Create a ``SubtitlesClip`` positioned at the bottom of the frame."""

    def generator(txt: str) -> TextClip:
        params = dict(
            text=txt,
            font_size=fontsize,
            color=color,
            bg_color=(0, 0, 0, 153),
            method="caption",
            size=(int(size[0] * 0.8), None),
            text_align="center",
        )
        if font and os.path.exists(font):
            params["font"] = font
        return TextClip(**params)

    return SubtitlesClip(subtitles, make_textclip=generator).with_position(("center", "bottom"))
