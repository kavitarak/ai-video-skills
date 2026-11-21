import importlib.util
import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("setup_effects", ROOT / ".agents/skills/effects/setup_effects.py")
se = importlib.util.module_from_spec(spec)
spec.loader.exec_module(se)


def fake_kit(d: Path) -> Path:
    kit = d / "effects-kit"
    (kit / "scripts").mkdir(parents=True)
    (kit / "scripts" / "fx.py").write_text("# fake engine\n")
    (kit / "requirements.txt").write_text("")
    return kit


class SetupTests(unittest.TestCase):
    def run_main(self, argv):
        buf = io.StringIO()
        with mock.patch("sys.argv", ["setup_effects.py", *argv]), redirect_stdout(buf):
            code = se.main()
        return code, buf.getvalue().strip().splitlines()[-1]

    def test_missing_ffmpeg(self):
        with mock.patch.object(se.shutil, "which", return_value=None):
            code, last = self.run_main(["--dir", "x"])
        self.assertEqual(code, 1)
        self.assertTrue(last.startswith("NEED_FFMPEG"))

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
    def test_ready_with_existing_engine(self):
        with tempfile.TemporaryDirectory() as d:
            kit = fake_kit(Path(d))
            with mock.patch.object(se, "REQUIRED", "import json"), \
                    mock.patch.object(se, "run", return_value=True):
                code, last = self.run_main(["--dir", str(kit)])
            self.assertEqual(code, 0)
            self.assertTrue(last.startswith("READY"))
            self.assertIn(str(se.venv_python(kit.resolve())), last)

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
    def test_non_empty_folder_without_engine_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "junk.txt").write_text("x")
            with mock.patch.object(se.shutil, "which", side_effect=lambda n: "/usr/bin/" + n):
                code, last = self.run_main(["--dir", d])
            self.assertEqual(code, 1)
            self.assertTrue(last.startswith("FAILED"))

    def test_windows_python_path(self):
        self.assertEqual(se.venv_python(Path("k"), windows=True), Path("k") / ".venv" / "Scripts" / "python.exe")
        self.assertEqual(se.venv_python(Path("k"), windows=False), Path("k") / ".venv" / "bin" / "python")


if __name__ == "__main__":
    unittest.main()
