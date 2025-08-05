# storyshow-generator

Utility for generating a short video story using images, narration audio and text.

## Usage

```bash
python main.py --images_dir assets/images --audio_path assets/audio/audio.mp3 \
  --text_path assets/text/text.txt --output output/video_final.mp4
```

Arguments:
- `--images_dir` – folder containing images (all files are used).
- `--audio_path` – path to narration audio (`mp3`/`wav`).
- `--text_path` – path to plain text story.
- `--output` – resulting mp4 file.
- `--resolution` – video resolution, e.g. `1920x1080`.
- `--transition` – duration of transitions between slides in seconds.
  - `--font` – path to a `.ttf` font used for subtitle text. If omitted, the script
    attempts to locate a common system font and otherwise falls back to MoviePy's
    default.

The script prefers a bundled virtual environment at `.venv` for importing
MoviePy so a newer release can be used without affecting the system Python.
Install requirements with `pip install -r requirements.txt` inside `.venv`
or globally.

Subtitles are generated automatically by splitting the text into sentences
and distributing them across the audio duration.
