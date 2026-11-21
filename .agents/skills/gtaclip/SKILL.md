---
name: gtaclip
description: Turn a long YouTube video (or a local video with subtitles) into viral vertical 9:16 clips with a hook title and burned-in captions, using GTAClip. Use when the user asks to clip, cut, or make Shorts, Reels or TikToks from a long video or podcast, or says /gtaclip.
---

# GTAClip: long video → viral vertical clips

GTAClip (by kavi.onlines, MIT) downloads a video and its subtitles, lets YOU pick the best
moments from the transcript (no API key needed), then cuts each moment, crops it to 9:16 and
burns in a hook title and captions. Repo: https://github.com/kavitarak/GTA-clip.kavi

The user is usually not technical. Do the work for them; don't ask them to run commands.

## 1. Set up (once)
1. Check `python --version` (3.10+), `ffmpeg -version` and `yt-dlp --version`. Install what's missing:
   - ffmpeg: Windows `winget install ffmpeg`, macOS `brew install ffmpeg`, Linux `sudo apt install ffmpeg`.
   - yt-dlp: `pip install yt-dlp`.
2. Get GTAClip: `git clone --depth 1 https://github.com/kavitarak/GTA-clip.kavi ~/gtaclip`, then
   `pip install -e ~/gtaclip`. Use `python -m clipper` if the `gtaclip` command isn't on PATH.

## 2. Make the clips (agent mode, no API key)
1. Ask only what you can't decide: how many clips (default 5) and length (default 20 to 60 s).
2. Save the transcript and instructions:
   `gtaclip "<URL or file>" --clips 5 --dump-transcript transcript.txt`
   For a local file add `--transcript <file.srt|.vtt>`.
3. Read `transcript.txt`. Pick self-contained moments with a strong first line and a complete
   ending. Write `picks.json`:
   `{"clips": [{"start": 12.5, "end": 48.0, "title": "...", "hook": "...", "score": 85, "reason": "..."}]}`
   Title and hook in the speaker's language (Hindi, Hinglish or English). Hook: at most 8 words.
   No overlaps.
4. Render: `gtaclip "<same URL or file>" --clips 5 --picks picks.json` (same `--transcript` if used).
   For Hindi (Devanagari) captions add `--font "Nirmala UI"` on Windows or `--font "Noto Sans Devanagari"`.
5. Tell the user where the clips are (`output/clip_01.mp4` …) and summarise `output/manifest.json`.
   Remind them in one line to watch each clip before posting.

## Rules
- Only clip videos the user owns or has permission to use.
- Cropping is centred; there is no face tracking yet. Say so if the speaker is off-centre.
- If the video has no subtitles, say so: GTAClip needs a transcript (`--transcript FILE`).
