"""Cross-platform setup for the effects skill (Windows, macOS, Linux).

Works in Claude Code, Codex, Gemini CLI and Antigravity, including sandboxed agents:
the engine is placed in the CURRENT project folder (./effects-kit) by default, so it
never needs write access outside the workspace.

    python setup_effects.py            # set up in ./effects-kit
    python setup_effects.py --dir PATH # set up somewhere else

Last line printed:
    READY <python-path> <kit-folder>      everything is installed
    NEED_FFMPEG / NEED_GIT / NEED_NETWORK / FAILED <reason>
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ENGINE_URL = "https://github.com/Vibha-Ramprakash/claude-video-effects"
REQUIRED = "import mediapipe, cv2, PIL, numpy"


def say(status: str, detail: str = "") -> None:
    print(f"{status} {detail}".strip(), flush=True)


def venv_python(kit: Path, windows: bool | None = None) -> Path:
    if (os.name == "nt") if windows is None else windows:
        return kit / ".venv" / "Scripts" / "python.exe"
    return kit / ".venv" / "bin" / "python"


def ok(py: Path) -> bool:
    if not py.exists():
        return False
    return subprocess.run([str(py), "-c", REQUIRED], capture_output=True).returncode == 0


def run(cmd: list[str]) -> bool:
    return subprocess.run(cmd).returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dir", default="effects-kit", help="where to put the engine (default ./effects-kit)")
    args = parser.parse_args()
    kit = Path(args.dir).expanduser().resolve()

    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        say("NEED_FFMPEG", "Windows: winget install ffmpeg | macOS: brew install ffmpeg | Linux: sudo apt install ffmpeg")
        return 1
    if sys.version_info < (3, 10):
        say("FAILED", f"Python 3.10+ needed, this is {sys.version.split()[0]}")
        return 1

    if not (kit / "scripts" / "fx.py").is_file():
        if not shutil.which("git"):
            say("NEED_GIT", "Windows: winget install Git.Git | macOS: xcode-select --install | Linux: sudo apt install git")
            return 1
        if kit.exists() and any(kit.iterdir()):
            say("FAILED", f"{kit} exists but has no scripts/fx.py; pick another --dir")
            return 1
        print(f"Downloading the effects engine into {kit} ...", flush=True)
        if not run(["git", "clone", "--depth", "1", ENGINE_URL, str(kit)]):
            say("NEED_NETWORK", "git clone failed; allow network access for this step and run again")
            return 1

    py = venv_python(kit)
    if ok(py):
        say("READY", f"{py} {kit}")
        return 0

    print("Creating a Python environment (first time takes 1 to 3 minutes) ...", flush=True)
    if not py.exists():
        venv.EnvBuilder(with_pip=True).create(kit / ".venv")
    req = kit / "requirements.txt"
    if not (run([str(py), "-m", "pip", "install", "-q", "--upgrade", "pip"])
            and run([str(py), "-m", "pip", "install", "-q", "-r", str(req)])):
        say("NEED_NETWORK", "pip install failed; allow network access for this step and run again")
        return 1
    if not ok(py):
        say("FAILED", "packages installed but mediapipe/opencv did not import; try Python 3.12")
        return 1
    say("READY", f"{py} {kit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
