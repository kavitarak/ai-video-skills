# AGENTS.md

This repo is a pack of video-editing Agent Skills. Each skill is a folder in `.agents/skills/` with a `SKILL.md`.

- Codex, Gemini CLI and Antigravity read `.agents/skills/` automatically when you open this folder.
- Claude Code reads the synced copy in `.claude/skills/`.
- To use the skills in any folder, run `bash install.sh` (macOS/Linux) or `install.ps1` (Windows).

## Rules for changes
- Edit skills only in `.agents/skills/`, then run `python scripts/build.py` (syncs `.claude/skills/` and rebuilds `dist/*.zip`).
- Run `python -m unittest discover -s tests` before committing.
- Frontmatter `name` must equal the folder name (lowercase, hyphens). `description` says what the skill does and when to use it.
- Keep `.agents/skills/effects/LICENSE` and the credit line in that skill: it is MIT work by Vibha Ramprakash.
- Never hardcode API keys or personal data in a skill.
