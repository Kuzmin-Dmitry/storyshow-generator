"""Command line interface for StoryShow video generation."""
from __future__ import annotations

import argparse
import glob
import os

from moviepy import CompositeVideoClip

from utils.audio import load_audio
from utils.slideshow import create_slideshow
from utils.subtitles import create_subtitles_clip, generate_subtitle_entries


def parse_resolution(value: str) -> tuple[int, int]:
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except Exception as exc:  # pragma: no cover - simple validation
        raise argparse.ArgumentTypeError("Resolution must be WxH") from exc


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a story slideshow video.")
    parser.add_argument("--images_dir", default="assets/images", help="Folder with images")
    parser.add_argument("--audio_path", default="assets/audio/audio.mp3", help="Path to narration audio")
    parser.add_argument("--text_path", default="assets/text/text.txt", help="Path to story text")
    parser.add_argument("--output", default="output/video_final.mp4", help="Output video path")
    parser.add_argument("--resolution", default="1920x1080", help="Video resolution WxH")
    parser.add_argument(
        "--transition", type=float, default=1.0, help="Transition duration in seconds"
    )
    parser.add_argument(
        "--font",
        default="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        help="Font path used for subtitle rendering",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    width, height = parse_resolution(args.resolution)

    try:
        image_paths = sorted(glob.glob(os.path.join(args.images_dir, "*")))
        if not image_paths:
            raise FileNotFoundError("No images found in images_dir")

        audio_clip = load_audio(args.audio_path)

        slideshow = create_slideshow(
            image_paths,
            audio_clip.duration,
            size=(width, height),
            transition_duration=args.transition,
        )

        with open(args.text_path, "r", encoding="utf-8") as f:
            story_text = f.read()

        subtitle_entries = generate_subtitle_entries(story_text, audio_clip.duration)
        subtitles_clip = create_subtitles_clip(
            subtitle_entries, (width, height), font=args.font
        )

        video = CompositeVideoClip([slideshow, subtitles_clip])
        video = video.with_audio(audio_clip)

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        video.write_videofile(args.output, fps=25, codec="libx264")
    except Exception as exc:  # pragma: no cover - runtime safety
        print(f"Error: {exc}")
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
