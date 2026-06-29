import os
import random
import wave
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip


WIDTH = 1080
HEIGHT = 1920
FPS = 30
OUTPUT_DIR = "output"


TOPICS = [
    {
        "title": "The Richest Man in History",
        "script": "The richest man in history may have been Mansa Musa, the ruler of Mali. When he travelled to Egypt, he gave away so much gold that he reportedly affected the local economy. His empire controlled major gold and salt trade routes, making him almost unimaginably wealthy."
    },
    {
        "title": "The Shortest War Ever",
        "script": "The shortest war in history lasted less than an hour. In 1896, Britain and Zanzibar fought a war that ended after around 38 minutes. Zanzibar’s palace was heavily damaged, and the conflict was over almost as soon as it began."
    },
    {
        "title": "The Animal That Can Survive Space",
        "script": "Tardigrades are tiny creatures sometimes called water bears. They can survive extreme heat, freezing cold, radiation, and even the vacuum of space for a limited time. They do this by entering a dried-out survival state."
    },
]


def make_beep_audio(path: str, duration: float = 12.0, freq: int = 220):
    sample_rate = 44100
    amplitude = 12000
    total_samples = int(sample_rate * duration)

    with wave.open(path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        for i in range(total_samples):
            value = int(amplitude * math.sin(2 * math.pi * freq * i / sample_rate))
            wav.writeframesraw(value.to_bytes(2, byteorder="little", signed=True))


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""

    dummy = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy)

    for word in words:
        test = current + " " + word if current else word
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def get_font(size):
    possible_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for font_path in possible_fonts:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)

    return ImageFont.load_default()


def make_text_image(title, script):
    img = Image.new("RGB", (WIDTH, HEIGHT), (18, 18, 18))
    draw = ImageDraw.Draw(img)

    title_font = get_font(82)
    body_font = get_font(48)
    small_font = get_font(38)

    draw.text((70, 140), "60 Seconds Smarter", font=small_font, fill=(220, 220, 220))

    title_lines = wrap_text(title, title_font, WIDTH - 140)
    y = 330
    for line in title_lines:
        draw.text((70, y), line, font=title_font, fill=(255, 255, 255))
        y += 100

    script_lines = wrap_text(script, body_font, WIDTH - 140)
    y += 90
    for line in script_lines[:12]:
        draw.text((70, y), line, font=body_font, fill=(235, 235, 235))
        y += 68

    draw.text((70, HEIGHT - 180), "#shorts #facts #weirdfacts", font=small_font, fill=(200, 200, 200))

    return np.array(img)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    topic = random.choice(TOPICS)
    title = topic["title"]
    script = topic["script"]

    audio_path = os.path.join(OUTPUT_DIR, "voice.wav")
    video_path = os.path.join(OUTPUT_DIR, "short.mp4")

    make_beep_audio(audio_path, duration=12)

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    background = ColorClip(size=(WIDTH, HEIGHT), color=(18, 18, 18), duration=duration)

    text_img = make_text_image(title, script)
    text_clip = ImageClip(text_img).set_duration(duration)

    video = CompositeVideoClip([background, text_clip])
    video = video.set_audio(audio)

    video.write_videofile(
        video_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=2,
    )

    print(f"Created video: {video_path}")


if __name__ == "__main__":
    main()
