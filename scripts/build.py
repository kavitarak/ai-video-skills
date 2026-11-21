"""Sync .agents/skills -> .claude/skills and build one upload zip per skill in dist/.

Run after editing any skill:  python scripts/build.py
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".agents" / "skills"
CLAUDE = ROOT / ".claude" / "skills"
DIST = ROOT / "dist"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError(f"{skill_md}: missing YAML frontmatter")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta


def skills() -> list[Path]:
    return sorted(p for p in SRC.iterdir() if (p / "SKILL.md").is_file())


def check() -> list[str]:
    errors = []
    for d in skills():
        meta = frontmatter(d / "SKILL.md")
        if meta.get("name") != d.name:
            errors.append(f"{d.name}: frontmatter name '{meta.get('name')}' must match the folder name")
        if not NAME_RE.match(d.name) or len(d.name) > 64:
            errors.append(f"{d.name}: name must be lowercase letters, digits and hyphens (max 64)")
        if not meta.get("description") or len(meta["description"]) > 1024:
            errors.append(f"{d.name}: description is required and must be at most 1024 characters")
    return errors


def build() -> None:
    errors = check()
    if errors:
        sys.exit("\n".join(errors))
    if CLAUDE.exists():
        shutil.rmtree(CLAUDE)
    shutil.copytree(SRC, CLAUDE, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob("*.zip"):
        old.unlink()
    for d in skills():
        with zipfile.ZipFile(DIST / f"{d.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts and f.suffix != ".pyc":
                    z.write(f, f"{d.name}/{f.relative_to(d).as_posix()}")
    print(f"Built {len(skills())} skills: " + ", ".join(d.name for d in skills()))


if __name__ == "__main__":
    build()
