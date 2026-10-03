"""Check upload layout, privacy boundaries, and source integrity (no network)."""

import io
import json
import posixpath
import re
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
                         *(f"chinese-writing/{name}" for name in builder.COMMON_FILES),
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
        for relative in (".local/profile.md", "chinese-writing/.local/profile.md", ".env", "references/private-notes.md",
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
                    target = (f"skills/{name}" if name.startswith("chinese-writing/")
                              else f"skills/mob-social-writing/{name}")
                    self.assertEqual(skill.read(name), plugin.read(target))
                self.assertNotIn("skills/mob-social-writing/chinese-writing/SKILL.md", plugin.namelist())
                with zipfile.ZipFile(io.BytesIO(files["chinese-writing-chatgpt-skill.zip"])) as common:
                    for name in common.namelist():
                        self.assertEqual(common.read(name), skill.read(f"chinese-writing/{name}"))
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

    def test_common_dependency_required_for_packaging(self):
        (self.root / "chinese-writing/SKILL.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing package source"):
            self.build_fixture()

    def test_actual_dependency_routes_and_relative_links_in_all_archives(self):
        files = self.build_fixture()
        for filename, data in files.items():
            if not filename.endswith(".zip"):
                continue
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = set(archive.namelist())
                common_entries = [name for name in names
                                  if name.endswith("chinese-writing/SKILL.md")]
                if filename == "chinese-writing-chatgpt-skill.zip":
                    self.assertIn("SKILL.md", names)
                else:
                    self.assertEqual(len(common_entries), 1)
                    social = ("skills/mob-social-writing/SKILL.md"
                              if filename.endswith("-plugin.zip") else "SKILL.md")
                    base = posixpath.dirname(social)
                    candidates = [posixpath.normpath(posixpath.join(base, path))
                                  for path in ("chinese-writing/SKILL.md", "../chinese-writing/SKILL.md")]
                    resolved = [name for name in candidates if name in names]
                    self.assertEqual(resolved, common_entries)
                for name in names:
                    if not name.endswith(".md") or name in ("README.md", "START-HERE.md", "chat-starter.md"):
                        continue
                    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", archive.read(name).decode("utf-8")):
                        if "://" in target or target.startswith("#"):
                            continue
                        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                        self.assertIn(resolved, names, (filename, name, target))

    def test_tampered_reference_cannot_be_packaged(self):
        with self.assertRaisesRegex(corpus.CorpusError, "SHA256"):
            builder.build_packages(self.root, b"unverified external or private corpus")


if __name__ == "__main__":
    unittest.main()
