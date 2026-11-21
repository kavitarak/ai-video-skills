import filecmp
import sys
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402


class SkillTests(unittest.TestCase):
    def test_every_skill_is_valid(self):
        self.assertEqual(build.check(), [])

    def test_expected_skills_present(self):
        names = {d.name for d in build.skills()}
        self.assertEqual(names, {"effects", "rank-reel", "casefile-documentary-reel", "gtaclip", "video-captions"})

    def test_claude_copy_is_in_sync(self):
        cmp = filecmp.dircmp(build.SRC, build.CLAUDE)
        def diffs(c):
            out = c.left_only + c.right_only + c.diff_files
            for sub in c.subdirs.values():
                out += diffs(sub)
            return out
        self.assertEqual(diffs(cmp), [], "run: python scripts/build.py")

    def test_dist_zips_have_skill_md_in_folder(self):
        for d in build.skills():
            with zipfile.ZipFile(build.DIST / f"{d.name}.zip") as z:
                self.assertIn(f"{d.name}/SKILL.md", z.namelist())

    def test_effects_keeps_original_mit_license(self):
        text = (build.SRC / "effects" / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Vibha Ramprakash", text)


if __name__ == "__main__":
    unittest.main()
