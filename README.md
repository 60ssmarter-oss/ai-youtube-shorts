# AI YouTube Shorts Automation Starter Kit

A free, mostly automated pipeline for creating YouTube Shorts.

## What it does
1. Generates a short script from a topic.
2. Creates a voiceover locally.
3. Builds a vertical 1080x1920 video with captions.
4. Exports metadata for YouTube upload.
5. Can be triggered from n8n or run manually.

## Free stack
- n8n Community Edition for scheduling/automation
- Python for video assembly
- Kokoro TTS or Piper TTS for local voiceover
- MoviePy + FFmpeg for editing
- YouTube Studio or YouTube Data API for upload

## Best niche to start
Channel concept: `60 Seconds Smarter`

Theme: fascinating history, science, geography, and money facts explained in under 60 seconds.

## Daily target
Start with 1-3 Shorts per day. Keep videos original, useful, and non-repetitive.

## Folder structure
- `topics.csv` - topic ideas
- `prompts.md` - prompts for scripts and metadata
- `make_short.py` - starter Python video builder
- `n8n_workflow_skeleton.json` - importable workflow outline
- `metadata_template.json` - sample YouTube metadata

## Setup overview
1. Install Python 3.11+
2. Install FFmpeg
3. Run: `pip install moviepy pillow pandas`
4. Add a voiceover file as `voiceover.wav` or connect Kokoro/Piper TTS.
5. Run: `python make_short.py`

## Monetization warning
Do not publish mass-produced repetitive content. Make each Short factual, edited, and meaningfully different.
