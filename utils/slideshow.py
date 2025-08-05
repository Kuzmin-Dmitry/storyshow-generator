"""Create slideshow clips with transitions and effects."""
from __future__ import annotations

import random
from typing import Iterable, Tuple

from moviepy import (
    CompositeVideoClip,
    ImageClip,
    VideoClip,
    vfx,
)

from .effects import apply_random_effect


TRANSITIONS = ("crossfade", "fade", "slide")


def _concat_with_transition(
    base: VideoClip, new: VideoClip, transition: str, duration: float
) -> VideoClip:
    """Concatenate ``new`` to ``base`` applying ``transition``."""
    start = max(base.duration - duration, 0)
    if transition == "crossfade":
        new = new.with_start(start).with_effects([vfx.CrossFadeIn(duration)])
    elif transition == "slide":
        new = new.with_start(start).with_effects([vfx.SlideIn(duration, "left")])
    elif transition == "fade":
        new = new.with_start(start).with_effects([vfx.FadeIn(duration)])
    else:
        new = new.with_start(start)
    return CompositeVideoClip([base, new]).with_duration(start + new.duration)


def create_slideshow(
    image_paths: Iterable[str],
    audio_duration: float,
    size: Tuple[int, int] = (1920, 1080),
    transition_duration: float = 1.0,
) -> VideoClip:
    """Return a video clip built from ``image_paths`` covering ``audio_duration``.

    Effects and transitions are applied randomly to keep slides trendy.
    """
    paths = list(image_paths)
    n = len(paths)
    if n == 0:
        raise ValueError("No images provided")

    # Duration of each clip adjusted for overlapping transitions
    clip_duration = (audio_duration + transition_duration * (n - 1)) / n

    clips = []
    for path in paths:
        clip = ImageClip(path).resized(size).with_duration(clip_duration)
        clip = apply_random_effect(clip)
        clips.append(clip)

    final = clips[0]
    for clip in clips[1:]:
        trans = random.choice(TRANSITIONS)
        final = _concat_with_transition(final, clip, trans, transition_duration)

    return final.with_duration(audio_duration)
