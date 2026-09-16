"""Check upload layout, privacy boundaries, and source integrity (no network)."""

import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_chatgpt as builder
import corpus


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for relative in (*builder.SKILL_FILES, builder.MANIFEST,
                         "chatgpt/START-HERE.md", "chatgpt/chat-starter.md"):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(builder.ROOT / relative, target)
        self.records = [{"id": "synthetic-test-only", "author": "Test Author",
                         "format": "reply", "source_url": "https://example.com/test",
                         "text": "This synthetic test fixture is not calibration data."}]

    def build_fixture(self):
        with patch.object(corpus, "convert_reference", return_value=self.records):
            return builder.build_packages(self.root, b"synthetic test data")

    def test_packages_exclude_private_data_and_unlisted_files(self):
        for relative in (".local/profile.md", ".env", "references/private-notes.md",
                         "agents/private.json", "scripts/private.py", ".git/config"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("PRIVATE_SENTINEL", encoding="utf-8")
        files = self.build_fixture()
        for name, data in files.items():
            if name.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    for member in archive.namelist():
                        self.assertNotIn("PRIVATE_SENTINEL", archive.read(member).decode("utf-8"))
                        self.assertFalse(member.startswith("/"))
                        self.assertNotIn("..", Path(member).parts)

    def test_expected_upload_layout_and_same_skill_content(self):
        files = self.build_fixture()
        with zipfile.ZipFile(io.BytesIO(files["mob-social-writing-chatgpt-skill.zip"])) as skill:
            with zipfile.ZipFile(io.BytesIO(files["mob-social-writing-plugin.zip"])) as plugin:
                self.assertIn("SKILL.md", skill.namelist())
                self.assertIn(".codex-plugin/plugin.json", plugin.namelist())
                for name in skill.namelist():
                    self.assertEqual(skill.read(name), plugin.read(f"skills/mob-social-writing/{name}"))
                examples = skill.read("references/external-examples.md").decode("utf-8")
                self.assertIn("Origin: external_reference | Feedback: unreviewed | Parent: missing", examples)
                self.assertIn("third_party/MengTo-LICENSE", skill.namelist())
        self.assertEqual(files, self.build_fixture())
        report = json.loads(files["package-manifest.json"])
        self.assertFalse(report["private_data_included"])

    def test_symlink_cannot_smuggle_private_data(self):
        private = self.root / "secret"
        private.write_text("PRIVATE_SENTINEL", encoding="utf-8")
        source = self.root / "references/reply-moves.md"
        source.unlink()
        source.symlink_to(private)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.build_fixture()

    def test_tampered_reference_cannot_be_packaged(self):
        with self.assertRaisesRegex(corpus.CorpusError, "SHA256"):
            builder.build_packages(self.root, b"unverified external or private corpus")


if __name__ == "__main__":
    unittest.main()
