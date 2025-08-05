"""Visual effects helpers for StoryShow Generator."""
from __future__ import annotations

import random
from typing import Callable, List

from moviepy import VideoClip, vfx


def apply_ken_burns(clip: VideoClip, zoom: float = 1.1) -> VideoClip:
    """Apply a simple Ken Burns (slow zoom-in) effect to ``clip``."""
    effect = vfx.Resize(lambda t: 1 + (zoom - 1) * (t / clip.duration))
    return clip.with_effects([effect])


def apply_grayscale(clip: VideoClip) -> VideoClip:
    """Convert clip to grayscale."""
    return clip.with_effects([vfx.BlackAndWhite()])


_EFFECTS = {
    "kenburns": apply_ken_burns,
    "grayscale": apply_grayscale,
}


def apply_random_effect(clip: VideoClip, effect_names: List[str] | None = None) -> VideoClip:
    """Apply a random visual effect from ``effect_names`` to ``clip``.

    Parameters
    ----------
    clip:
        Source video clip.
    effect_names:
        List of effect identifiers. If ``None`` all known effects are used.
    """
    names = effect_names or list(_EFFECTS.keys())
    effect: Callable[[VideoClip], VideoClip] = _EFFECTS[random.choice(names)]
    return effect(clip)
