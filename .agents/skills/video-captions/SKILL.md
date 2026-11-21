---
name: video-captions
description: Add burned-in Hindi/Hinglish + English captions and a credit line to any video, and write Hinglish hooks, titles and hashtags for it, using Video Caption Generator by Tarak Industries (offline Whisper, no API key). Use when the user asks for captions, subtitles, an .srt file, an English translation of a Hindi video, or hooks/titles for a video.
---

# Video captions (Hindi + English) and Hinglish hooks

Video Caption Generator by Tarak Industries (MIT) listens to a video with Whisper on the user's
own computer, then makes:
- `<name>.mp4`: the video with spoken-language captions at the bottom, English captions (yellow)
  just above, and a credit line in the top-right corner
- `<name>.srt` and `<name> (English).srt`
- Hinglish hooks, titles and hashtags, plus the strongest lines from the video

Repo: https://github.com/kavitarak/video-caption-generator-by-tarak-industries

The user is usually not technical. Do the work for them; don't ask them to run commands.

## 1. Set up (once)
1. Check `python --version` (3.10+) and `ffmpeg -version`. Install ffmpeg if missing:
   Windows `winget install ffmpeg` (then reopen the terminal), macOS `brew install ffmpeg`,
   Linux `sudo apt install ffmpeg`.
2. `git clone --depth 1 https://github.com/kavitarak/video-caption-generator-by-tarak-industries ~/tarak-captions`
3. `cd ~/tarak-captions && pip install -e ".[video]"` (installs faster-whisper). Use
   `python -m tarak_captions` if the `tarak-captions` command isn't on PATH.

## 2. Captions
Ask once for the credit text if the user hasn't given one (default "Video by Tarak Industries").

```bash
tarak-captions --video "<file>" --captions --credit "<credit>" --name "<file name>" --out output
```
- Hindi video: add `--lang hi`. Better Hindi accuracy: `--whisper-model medium` (slower).
- Fast test on a slow PC: `--whisper-model tiny`.
- Only one caption line: `--no-english`.
- Hindi letters show as boxes: pass a Hindi font, `--font "Nirmala UI"` (Windows).

The first run downloads the Whisper model (about 75 MB for tiny, 460 MB for small).

## 3. Hooks and titles only
- From the video: `tarak-captions --video "<file>" -n 10`
- From a topic: `tarak-captions "AI tools for students" -n 10`
- From subtitles: `tarak-captions --transcript subs.srt`
If the detected topic looks wrong, pass the topic yourself as the first argument.

## 4. Finish
Tell the user the file paths, show 3 to 5 of the best hooks, and remind them in one line to
watch the video before posting (Whisper can mishear names).
