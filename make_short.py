"""
Starter video builder for AI YouTube Shorts.
Creates a simple 1080x1920 captioned video from a script and optional voiceover.

Install:
  pip install moviepy pillow
  Install FFmpeg separately.

Usage:
  python make_short.py
"""
from pathlib import Path
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, TextClip

OUT = Path("output")
OUT.mkdir(exist_ok=True)

SCRIPT = """The richest man in history was so wealthy, he changed economies.
His name was Mansa Musa, ruler of the Mali Empire in the 1300s.
His kingdom controlled huge amounts of gold and salt.
On his pilgrimage to Mecca, he gave away so much gold that prices were affected for years.
Some historians believe his wealth may have surpassed today's billionaires.
History is full of stories that sound impossible — until you look closer."""

WIDTH, HEIGHT = 1080, 1920
DURATION = 45
BACKGROUND = (20, 20, 20)


def split_captions(text: str, max_words: int = 7):
    words = text.replace("\n", " ").split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))
    return chunks


def main():
    audio_path = Path("voiceover.wav")
    if audio_path.exists():
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
    else:
        audio = None
        duration = DURATION

    bg = ColorClip(size=(WIDTH, HEIGHT), color=BACKGROUND, duration=duration)

    title = TextClip(
        "60 Seconds Smarter",
        fontsize=70,
        color="white",
        method="caption",
        size=(950, None),
        align="center",
    ).set_position((65, 170)).set_duration(duration)

    captions = split_captions(SCRIPT)
    caption_duration = duration / max(len(captions), 1)
    caption_clips = []
    for idx, caption in enumerate(captions):
        clip = TextClip(
            caption,
            fontsize=78,
            color="white",
            method="caption",
            size=(950, None),
            align="center",
        ).set_position((65, 760)).set_start(idx * caption_duration).set_duration(caption_duration)
        caption_clips.append(clip)

    video = CompositeVideoClip([bg, title, *caption_clips])
    if audio:
        video = video.set_audio(audio)

    output_path = OUT / "short.mp4"
    video.write_videofile(str(output_path), fps=30, codec="libx264", audio_codec="aac")
    print(f"Created {output_path}")


if __name__ == "__main__":
    main()
