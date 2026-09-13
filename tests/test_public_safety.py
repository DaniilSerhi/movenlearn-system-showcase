from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.verify_public_repo import audit, scan_blob, scan_text


class PublicationTests(unittest.TestCase):
    def test_sensitive_patterns_are_rejected_without_printing_values(self):
        cases = [
            "/" + "Users/person/private.txt",
            "sk" + "-" + "A" * 32,
            "Bearer " + "B" * 30,
            "person@" + "private-company.invalid",
            "Clients" + "/sample.json",
            "api_key=" + '"abcdef123456"',
            "config " + ".e" + "nv",
        ]
        for text in cases:
            with self.subTest(kind=cases.index(text)):
                self.assertTrue(scan_text(text))
        self.assertFalse(scan_text("fictional@example.invalid"))

    def test_environment_files_and_unapproved_binaries_fail(self):
        self.assertTrue(scan_blob(".e" + "nv", b"nothing", {}))
        self.assertTrue(scan_blob("payload.zip", b"opaque", {}))

    def test_symlink_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "reference.md").write_text("safe")
            (root / "link.md").symlink_to(root / "reference.md")
            self.assertTrue(audit(root, history=False)[0])

    def test_deleted_sensitive_history_is_still_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.run(["git", "-C", str(root), *args], check=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            git("init", "-b", "main")
            git("config", "user.name", "Synthetic Test")
            git("config", "user.email", "test@example.invalid")
            path = root / "accident.md"
            path.write_text("Bearer " + "X" * 30)
            git("add", "accident.md")
            git("commit", "-m", "fixture")
            path.unlink()
            git("add", "-u")
            git("commit", "-m", "remove fixture")
            failures, _, _ = audit(root)
            self.assertTrue(any(name.startswith("history:") for name, _ in failures))

    def test_changed_font_is_rejected(self):
        manifest = {"font.ttf": {"sha256": "0" * 64}}
        self.assertTrue(scan_blob("assets/fonts/font.ttf", b"changed", manifest))


if __name__ == "__main__":
    unittest.main()

