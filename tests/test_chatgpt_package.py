"""Verify public layouts, deterministic builds, dependencies, and privacy offline."""

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


def copy_public_sources(root):
    paths = (*builder.SKILL_FILES, builder.MANIFEST,
             "chatgpt/START-HERE.md", "chatgpt/chat-starter.md")
    for relative in paths:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(builder.ROOT / relative, target)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve() / "source"
        self.root.mkdir()
        copy_public_sources(self.root)

    def test_default_build_offline_deterministic_and_manifest_has_no_local_path(self):
        with patch.object(corpus, "download_reference", side_effect=AssertionError("network")):
            files = builder.build_packages(self.root)
            self.assertEqual(files, builder.build_packages(self.root))
            with patch.object(builder, "ROOT", self.root):
                self.assertEqual(builder.main(["--output", str(self.root / "dist")]), 0)
        report = json.loads(files["package-manifest.json"])
        self.assertEqual(report["name"], "mob-write")
        self.assertEqual(report["version"], "0.4.0-rc.6")
        self.assertEqual(report["source"], builder.SOURCE)
        self.assertEqual(report["external_reference_count"], 0)
        self.assertIsNone(report["reference_sha256"])
        self.assertEqual(report["canonical_content_sha256"],
                         builder.content_sha256(builder.public_skills(self.root)["mob-write"]))
        for path, expected in report["public_source_sha256"].items():
            self.assertEqual(builder.hashlib.sha256((self.root / path).read_bytes()).hexdigest(), expected)
        self.assertNotIn(str(self.root), files["package-manifest.json"].decode())
        for name, expected in report["sha256"].items():
            self.assertEqual(builder.hashlib.sha256(files[name]).hexdigest(), expected)
            self.assertEqual(files[name], (self.root / "dist" / name).read_bytes())

    def test_packages_exclude_private_data_and_unlisted_files(self):
        for relative in (".local/profile.md", "chinese-writing/.local/profile.md",
                         "compat/mob-social-writing/.local/profile.md", ".env",
                         "references/private-notes.md", "agents/private.json",
                         "examples/private-feedback.md", "tests/fixtures/held-out-cases.json",
                         "scripts/private.py", ".git/config"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("PRIVATE_SENTINEL", encoding="utf-8")
        for name, data in builder.build_packages(self.root).items():
            if name.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(data)) as archive:
                    for member in archive.namelist():
                        self.assertNotIn("PRIVATE_SENTINEL", archive.read(member).decode("utf-8"))
                        self.assertFalse(member.startswith("/"))
                        self.assertNotIn("..", Path(member).parts)
                        self.assertNotIn(".local", Path(member).parts)

    def test_single_canonical_plugin_and_standalone_use_identical_public_files(self):
        files = builder.build_packages(self.root)
        self.assertEqual({name for name in files if name.endswith(".zip")},
                         {"mob-write-chatgpt-skill.zip", "mob-write-plugin.zip"})
        with zipfile.ZipFile(io.BytesIO(files["mob-write-chatgpt-skill.zip"])) as canonical:
            canonical_names = set(canonical.namelist())
            self.assertIn("SKILL.md", canonical_names)
            self.assertNotIn("references/external-examples.md", canonical_names)
            with zipfile.ZipFile(io.BytesIO(files["mob-write-plugin.zip"])) as plugin:
                plugin_names = set(plugin.namelist())
                self.assertIn(".codex-plugin/plugin.json", plugin_names)
                self.assertEqual([name for name in plugin_names if name.endswith("/SKILL.md")],
                                 ["skills/mob-write/SKILL.md"])
                primary_manifest = json.loads(plugin.read(".codex-plugin/plugin.json"))
                self.assertEqual(primary_manifest["name"], "mob-write")
                for path in canonical_names:
                    self.assertEqual(canonical.read(path), plugin.read(f"skills/mob-write/{path}"))
    def test_only_one_entry_in_every_distribution_layout(self):
        canonical = (self.root / "SKILL.md").read_bytes()
        self.assertEqual(list(builder.public_skills(self.root)), ["mob-write"])
        for filename, data in builder.build_packages(self.root).items():
            if not filename.endswith(".zip"):
                continue
            destination = self.root.parent / filename.removesuffix(".zip")
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                archive.extractall(destination)
            if filename.endswith("-plugin.zip"):
                directories = [destination / "skills" / builder.NAME]
            else:
                directories = [destination]
            for directory in directories:
                self.assertEqual((directory / "SKILL.md").read_bytes(), canonical)
            self.assertEqual(list(destination.rglob("SKILL.md")), [directories[0] / "SKILL.md"])

    def test_relative_markdown_links_resolve_in_every_archive(self):
        for filename, data in builder.build_packages(self.root).items():
            if not filename.endswith(".zip"):
                continue
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                names = set(archive.namelist())
                for name in names:
                    if not name.endswith(".md") or name in ("README.md", "chat-starter.md"):
                        continue
                    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", archive.read(name).decode()):
                        if "://" in target or target.startswith("#"):
                            continue
                        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target.split("#", 1)[0]))
                        self.assertIn(resolved, names, (filename, name, target))

    def test_optional_reference_layout_keeps_license_and_provenance(self):
        records = [{"id": "synthetic-test-only", "author": "Test Author",
                    "format": "reply", "source_url": "https://example.com/test",
                    "text": "This synthetic fixture is not a writing calibration sample."}]
        with patch.object(corpus, "convert_reference", return_value=records) as convert:
            files = builder.build_packages(self.root, b"synthetic test data")
        convert.assert_called_once_with(b"synthetic test data")
        with zipfile.ZipFile(io.BytesIO(files["mob-write-chatgpt-skill.zip"])) as archive:
            examples = archive.read("references/external-examples.md").decode()
            self.assertIn("Origin: external_reference | Feedback: unreviewed | Parent: missing", examples)
            self.assertIn("third_party/MengTo-LICENSE", archive.namelist())
        report = json.loads(files["package-manifest.json"])
        self.assertEqual(report["external_reference_count"], 1)
        self.assertEqual(report["reference_sha256"], corpus.REFERENCE_SHA256)

    def test_tampered_reference_cannot_be_packaged(self):
        with self.assertRaisesRegex(corpus.CorpusError, "SHA256"):
            builder.build_packages(self.root, b"unverified external or private corpus")

    def test_symlink_sources_and_ancestors_cannot_smuggle_private_data(self):
        private = self.root.parent / "private"
        private.write_text("PRIVATE_SENTINEL", encoding="utf-8")
        source = self.root / "references/reply-moves.md"
        source.unlink()
        source.symlink_to(private)
        with self.assertRaisesRegex(ValueError, "symlink"):
            builder.build_packages(self.root)
        link = self.root.parent / "source-link"
        link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            builder.read_public(link / "references", "sources.md")

    def test_canonical_sources_required(self):
        (self.root / "references/technical-document.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing package source"):
            builder.build_packages(self.root)

    def test_retired_output_artifacts_refused_before_new_files_are_written(self):
        output = self.root.parent / "dist"
        output.mkdir()
        retired = output / "wordaim-plugin.zip"
        retired.write_bytes(b"historical public artifact")
        with patch.object(builder, "ROOT", self.root), self.assertRaisesRegex(ValueError, "Retired artifact"):
            builder.main(["--output", str(output)])
        self.assertEqual(retired.read_bytes(), b"historical public artifact")
        self.assertFalse((output / "mob-write-plugin.zip").exists())

    def test_paths_and_symlink_output_rejected(self):
        for path in ("../private", "/private", "references/../../private", ".local/profile.md", ".env", ".git/config", "x\\private"):
            with self.assertRaisesRegex(ValueError, "Unsafe public path"):
                builder.read_public(self.root, path)
        output = self.root.parent / "out-link"
        output.symlink_to(self.root, target_is_directory=True)
        with patch.object(builder, "ROOT", self.root), self.assertRaisesRegex(ValueError, "symlink"):
            builder.main(["--output", str(output)])

    def test_cli_parent_output_allowed_but_symlink_before_parent_rejected(self):
        output = self.root / "../output"
        with patch.object(builder, "ROOT", self.root):
            self.assertEqual(builder.main(["--output", str(output)]), 0)
        self.assertTrue((output / "mob-write-chatgpt-skill.zip").is_file())
        link = self.root / "redirect"
        link.symlink_to(self.root.parent, target_is_directory=True)
        with patch.object(builder, "ROOT", self.root), self.assertRaisesRegex(ValueError, "symlink"):
            builder.main(["--output", str(link / "../unsafe-output")])
        self.assertFalse((self.root.parent / "unsafe-output").exists())


if __name__ == "__main__":
    unittest.main()
