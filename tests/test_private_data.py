"""Exercise connection selection, private upgrade isolation and empty templates."""
import contextlib
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_chatgpt as builder
import corpus
import install
import private_data


class PrivateDataTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.skill = self.base / "skills/mob-write"
        install.install(builder.ROOT, self.skill.parent)

    def bundle(self, name):
        directory = self.base / name
        private_data.initialize(directory, name, "Personal English replies only")
        return directory

    def test_initialization_is_private_empty_and_refuses_overwrite(self):
        directory = self.bundle("Avery")
        self.assertEqual((directory / "corpus.jsonl").read_bytes(), b"")
        self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)
        for path in directory.iterdir():
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        before = {p.name: p.read_bytes() for p in directory.iterdir()}
        with self.assertRaisesRegex(ValueError, "overwrite"):
            private_data.initialize(directory, "Other", "Other scope")
        self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})

    def test_connection_switches_corpus_without_merging_authors(self):
        first, second = self.bundle("Avery"), self.bundle("Blair")
        for directory in (first, second):
            row = {"id": directory.name, "platform": "x", "format": "reply", "intent": "gratitude",
                   "author": directory.name, "origin": "human_authored", "feedback": "unreviewed",
                   "feedback_note": "", "text": f"PRIVATE_SENTINEL_{directory.name}",
                   "parent_text": None, "source_url": None}
            (directory / "corpus.jsonl").write_text(json.dumps(row) + "\n")
        first_before = (first / "corpus.jsonl").read_bytes()
        with patch.object(corpus, "SKILL_ROOT", self.skill):
            for directory in (first, second):
                private_data.connect(self.skill, directory)
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(corpus.main(["stats"]), 0)
                self.assertEqual(json.loads(output.getvalue())["data_dir"], str(directory))
                self.assertEqual(corpus.load_all(private_data.data_directory(self.skill))[0]["author"], directory.name)
        self.assertEqual((first / "corpus.jsonl").read_bytes(), first_before)

    def test_no_connection_uses_local_and_explicit_directory_overrides(self):
        self.assertEqual(private_data.data_directory(self.skill), self.skill / ".local")
        first, second = self.bundle("Avery"), self.bundle("Blair")
        private_data.connect(self.skill, first)
        self.assertEqual(private_data.data_directory(self.skill, second), second)

    def test_bad_connection_fails_instead_of_silently_selecting_other_data(self):
        directory = self.bundle("Avery")
        private_data.connect(self.skill, directory)
        (directory / "bundle.json").write_text('{"schema":1,"owner":"Avery"}')
        with self.assertRaisesRegex(ValueError, "owner/scope"):
            private_data.data_directory(self.skill)
        with patch.object(corpus, "SKILL_ROOT", self.skill), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(corpus.main(["stats"]), 1)

    def test_connection_does_not_read_private_prose(self):
        directory = self.bundle("Avery")
        original = Path.open
        def metadata_only(path, *args, **kwargs):
            self.assertNotIn(path.name, ("profile.md", "voice-notes.md", "corpus.jsonl"))
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", metadata_only):
            private_data.connect(self.skill, directory)

    def test_public_upgrade_and_package_never_read_or_include_connected_data(self):
        directory = self.bundle("Avery")
        (directory / "profile.md").write_text("PRIVATE_SENTINEL_REPLACEMENT")
        private_data.connect(self.skill, directory)
        before = {p.name: p.read_bytes() for p in directory.iterdir()}
        connection = (self.skill / private_data.CONFIG).read_bytes()
        original = Path.open
        def public_only(path, *args, **kwargs):
            self.assertNotIn(directory, path.parents)
            self.assertNotIn(".local", path.parts)
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", public_only):
            install.install(builder.ROOT, self.skill.parent)
            # Even an installed source with an active local connection is public-safe.
            for relative in (builder.MANIFEST, "chatgpt/START-HERE.md", "chatgpt/chat-starter.md"):
                target = self.skill / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((builder.ROOT / relative).read_bytes())
            packages = builder.build_packages(self.skill)
        self.assertEqual((self.skill / private_data.CONFIG).read_bytes(), connection)
        self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})
        self.assertNotIn(str(directory), packages["package-manifest.json"].decode())

    def test_symlink_binding_and_bundle_are_refused(self):
        directory = self.bundle("Avery")
        alias = self.base / "alias"
        alias.symlink_to(directory, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            private_data.connect(self.skill, alias)
        (directory / "profile.md").unlink()
        (directory / "profile.md").symlink_to(builder.ROOT / "SKILL.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            private_data.connect(self.skill, directory)


if __name__ == "__main__":
    unittest.main()
