"""Exercise real isolated installs and upgrades without touching global skills."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_chatgpt as builder
import install as installer
from test_chatgpt_package import copy_public_sources, resolve_canonical_directory, resolve_technical_pointer


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.root = self.base / "source"
        self.root.mkdir()
        copy_public_sources(self.root)
        self.target = self.base / "isolated-skills"

    def legacy_install_fixture(self):
        """Model the published rc.1 protocol with public synthetic content only.

        Real historical-source installation and upgrade are separately exercised
        outside this suite; CI does not need an old commit or an authored copy.
        """
        canonical = {path: f"Synthetic legacy public file: {path}\n".encode()
                     for path in builder.SKILL_FILES}
        canonical["SKILL.md"] = b"---\nname: wordaim\ndescription: Synthetic legacy fixture.\n---\n"
        canonical[".gitignore"] = (self.root / ".gitignore").read_bytes()
        legacy = {builder.LEGACY_NAME: canonical}
        for name in ("chinese-writing", "mob-social-writing"):
            files = {path: f"Synthetic legacy alias file: {path}\n".encode()
                     for path in builder.alias_files(name)}
            files["SKILL.md"] = f"---\nname: {name}\ndescription: Synthetic legacy alias.\n---\nRead ../wordaim/SKILL.md.\n".encode()
            files[".gitignore"] = canonical[".gitignore"]
            files["LICENSE"] = canonical["LICENSE"]
            legacy[name] = files
        for name, files in legacy.items():
            directory = self.target / name
            for relative, data in files.items():
                path = directory / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            receipt = {"schema": 1, "source": builder.LEGACY_SOURCE,
                       "skill": name, "canonical": "wordaim", "version": "0.4.0-rc.1",
                       "files": builder.file_sha256(files),
                       "canonical_content_sha256": builder.content_sha256(canonical),
                       "skill_content_sha256": builder.content_sha256(files)}
            (directory / installer.LEGACY_INSTALL_MANIFEST).write_text(json.dumps(receipt))
        return legacy

    def test_actual_install_upgrade_hashes_aliases_and_private_preservation(self):
        report = installer.install(self.root, self.target)
        self.assertEqual(report["skills"], ["mob-write", "chinese-writing", "mob-social-writing", "wordaim"])
        self.assertEqual(resolve_technical_pointer(self.target / "chinese-writing"),
                         (self.root / "references/technical-document.md").read_bytes())
        for name, files in builder.public_skills(self.root).items():
            directory = self.target / name
            manifest = json.loads((directory / installer.INSTALL_MANIFEST).read_bytes())
            self.assertEqual(manifest["source"], builder.SOURCE)
            self.assertEqual(manifest["canonical_content_sha256"],
                             builder.content_sha256(builder.public_skills(self.root)["mob-write"]))
            self.assertNotIn(str(self.base), json.dumps(manifest))
            for relative, data in files.items():
                self.assertEqual((directory / relative).read_bytes(), data)
                self.assertEqual(manifest["files"][relative], installer.digest(data))
            private = directory / ".local/profile.md"
            private.parent.mkdir()
            private.write_text("PRIVATE_SENTINEL", encoding="utf-8")
        unknown = self.target / "mob-write/notes.txt"
        unknown.write_text("user-owned notes", encoding="utf-8")
        original_read = Path.read_bytes
        def public_reads_only(path):
            self.assertNotIn(".local", path.parts, "installer tried reading private data")
            return original_read(path)
        (self.root / "references/work.md").write_text("new public version\n", encoding="utf-8")
        manifest_path = self.root / builder.MANIFEST
        manifest = json.loads(manifest_path.read_bytes())
        manifest["version"] = "0.4.0-rc.3"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with patch.object(Path, "read_bytes", public_reads_only):
            report = installer.install(self.root, self.target)
        self.assertEqual(report["version"], "0.4.0-rc.3")
        self.assertEqual((self.target / "mob-write/references/work.md").read_text(), "new public version\n")
        for name in report["skills"]:
            self.assertEqual((resolve_canonical_directory(self.target / name) / "SKILL.md").read_bytes(),
                             (self.root / "SKILL.md").read_bytes())
            self.assertEqual((self.target / name / ".local/profile.md").read_text(), "PRIVATE_SENTINEL")
            alias = self.target / name / "SKILL.md"
            if name != "mob-write":
                self.assertIn("../mob-write/SKILL.md", alias.read_text())
                self.assertTrue((alias.parent / "../mob-write/SKILL.md").is_file())
        self.assertEqual(unknown.read_text(), "user-owned notes")

    def test_cli_requires_explicit_target_and_actual_repository_install(self):
        command = [sys.executable, str(builder.ROOT / "scripts/install.py")]
        missing = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)
        self.assertIn("--skills-dir", missing.stderr)
        completed = subprocess.run(command + ["--skills-dir", str(self.target)], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["version"], "0.4.0-rc.2")
        second = subprocess.run(command + ["--skills-dir", str(self.target)], capture_output=True, text=True)
        self.assertEqual(second.returncode, 0, second.stderr)
        for name in (builder.NAME, *builder.ALIAS_SOURCES):
            self.assertTrue((self.target / name / "SKILL.md").is_file())

    def test_unknown_legacy_directory_refused_before_any_install(self):
        legacy = self.target / "mob-social-writing"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md").write_text("legacy user content", encoding="utf-8")
        (legacy / ".local").mkdir()
        (legacy / ".local/profile.md").write_text("PRIVATE_SENTINEL", encoding="utf-8")
        with self.assertRaisesRegex(installer.InstallError, "Unmanaged installation"):
            installer.install(self.root, self.target)
        self.assertFalse((self.target / "mob-write").exists())
        self.assertEqual((legacy / "SKILL.md").read_text(), "legacy user content")
        self.assertEqual((legacy / ".local/profile.md").read_text(), "PRIVATE_SENTINEL")

    def test_user_public_changes_block_all_upgrades(self):
        installer.install(self.root, self.target)
        changed = self.target / "mob-social-writing/SKILL.md"
        changed.write_text("user public edits", encoding="utf-8")
        original = (self.target / "mob-write/SKILL.md").read_bytes()
        (self.root / "SKILL.md").write_text("new upstream content", encoding="utf-8")
        with self.assertRaisesRegex(installer.InstallError, "Public file changed"):
            installer.install(self.root, self.target)
        self.assertEqual((self.target / "mob-write/SKILL.md").read_bytes(), original)
        self.assertEqual(changed.read_text(), "user public edits")

    def test_other_source_and_malformed_manifest_refused(self):
        installer.install(self.root, self.target)
        path = self.target / "mob-write" / installer.INSTALL_MANIFEST
        manifest = json.loads(path.read_bytes())
        manifest["source"] = "https://example.com/unrelated-project"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(installer.InstallError, "source or manifest"):
            installer.install(self.root, self.target)
        path.write_text("broken json", encoding="utf-8")
        with self.assertRaisesRegex(installer.InstallError, "Unreadable install manifest"):
            installer.install(self.root, self.target)

    def test_managed_private_and_parent_traversal_paths_rejected_before_read(self):
        installer.install(self.root, self.target)
        path = self.target / "mob-write" / installer.INSTALL_MANIFEST
        manifest = json.loads(path.read_bytes())
        for relative in ("../outside", ".local/profile.md", ".env", ".git/config", "/outside", "x\\outside"):
            modified = dict(manifest, files={**manifest["files"], relative: "0" * 64})
            path.write_text(json.dumps(modified), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unsafe public path"):
                installer.install(self.root, self.target)

    def test_target_parent_managed_file_and_directory_symlinks_rejected(self):
        private = self.base / "private"
        private.mkdir()
        link = self.base / "link"
        link.symlink_to(private, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            installer.install(self.root, link / "nested")
        self.assertFalse((private / "nested").exists())
        installer.install(self.root, self.target)
        public = self.target / "mob-write/references/work.md"
        public.unlink()
        public.symlink_to(private / "sensitive")
        with self.assertRaisesRegex(ValueError, "symlink"):
            installer.install(self.root, self.target)
        public.unlink()
        public.write_bytes((self.root / "references/work.md").read_bytes())
        directory = self.target / "mob-write/references"
        shutil.rmtree(directory)
        directory.symlink_to(private, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            installer.install(self.root, self.target)

    def test_private_symlink_not_followed_or_moved_on_upgrade(self):
        installer.install(self.root, self.target)
        private = self.base / "private"
        private.mkdir()
        (private / "profile.md").write_text("PRIVATE_SENTINEL", encoding="utf-8")
        link = self.target / "mob-write/.local"
        link.symlink_to(private, target_is_directory=True)
        installer.install(self.root, self.target)
        self.assertTrue(link.is_symlink())
        self.assertEqual((private / "profile.md").read_text(), "PRIVATE_SENTINEL")

    def test_new_public_file_cannot_overwrite_user_owned_path(self):
        installer.install(self.root, self.target)
        directory = self.target / "mob-write"
        path = directory / installer.INSTALL_MANIFEST
        manifest = json.loads(path.read_bytes())
        # Simulate a prior managed version which did not include this file.
        manifest["files"].pop("assets/voice-profile.example.md")
        previous_content = {path: (directory / path).read_bytes() for path in manifest["files"]}
        manifest["skill_content_sha256"] = builder.content_sha256(previous_content)
        path.write_text(json.dumps(manifest), encoding="utf-8")
        owned = directory / "assets/voice-profile.example.md"
        owned.write_text("user-owned template", encoding="utf-8")
        with self.assertRaisesRegex(installer.InstallError, "unmanaged path"):
            installer.install(self.root, self.target)
        self.assertEqual(owned.read_text(), "user-owned template")

    def test_cli_parent_target_allowed_but_symlink_before_parent_rejected(self):
        command = [sys.executable, str(builder.ROOT / "scripts/install.py")]
        relative_target = self.root / "../relative-skills"
        result = subprocess.run(command + ["--skills-dir", str(relative_target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((relative_target / "mob-write/SKILL.md").is_file())
        link = self.root / "redirect"
        link.symlink_to(self.base, target_is_directory=True)
        result = subprocess.run(command + ["--skills-dir", str(link / "../unsafe-skills")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("symlink", result.stderr)
        self.assertFalse((self.base / "unsafe-skills").exists())

    def test_project_local_private_data_is_git_ignored_but_public_skills_can_be_added(self):
        project = self.base / "git-project"
        project.mkdir()
        initialized = subprocess.run(["git", "init", "-q", str(project)], capture_output=True, text=True)
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        target = project / ".agents/skills"
        installer.install(self.root, target)
        private_paths = []
        for name in (builder.NAME, *builder.ALIAS_SOURCES):
            directory = target / name
            self.assertEqual((directory / ".gitignore").read_bytes(), (self.root / ".gitignore").read_bytes())
            for relative in (".local/profile.md", ".env"):
                private = directory / relative
                private.parent.mkdir(parents=True, exist_ok=True)
                private.write_text("SYNTHETIC_PRIVATE_SENTINEL", encoding="utf-8")
                private_paths.append(str(private.relative_to(project)))
        ignored = subprocess.run(["git", "-C", str(project), "check-ignore", "--", *private_paths], capture_output=True, text=True)
        self.assertEqual(ignored.returncode, 0, ignored.stderr)
        self.assertEqual(set(ignored.stdout.splitlines()), set(private_paths))
        status = subprocess.run(["git", "-C", str(project), "status", "--porcelain", "--untracked-files=all"], capture_output=True, text=True)
        self.assertEqual(status.returncode, 0, status.stderr)
        for private in private_paths:
            self.assertNotIn(private, status.stdout)
        added = subprocess.run(["git", "-C", str(project), "add", "-A"], capture_output=True, text=True)
        self.assertEqual(added.returncode, 0, added.stderr)
        staged = subprocess.run(["git", "-C", str(project), "diff", "--cached", "--name-only"], capture_output=True, text=True)
        self.assertEqual(staged.returncode, 0, staged.stderr)
        self.assertIn(".agents/skills/mob-write/SKILL.md", staged.stdout.splitlines())
        for private in private_paths:
            self.assertNotIn(private, staged.stdout)

    def test_recognized_rc1_upgrade_preserves_private_paths_and_replaces_only_managed_public_files(self):
        old = self.legacy_install_fixture()
        self.assertEqual({name: len(files) for name, files in old.items()},
                         {"wordaim": 19, "chinese-writing": 5, "mob-social-writing": 4})
        for name in old:
            private = self.target / name / ".local/profile.md"
            private.parent.mkdir()
            private.write_text("SYNTHETIC_PRIVATE_SENTINEL")
        env = self.target / "wordaim/.env"
        env.write_text("SYNTHETIC_ENV_SENTINEL")
        notes = self.target / "wordaim/user-notes.txt"
        notes.write_text("user-owned notes")
        original_read = Path.read_bytes
        original_iterdir = Path.iterdir
        def read_public(path):
            self.assertNotIn(".local", path.parts)
            self.assertNotEqual(path.name, ".env")
            return original_read(path)
        def enumerate_public(path):
            self.assertNotIn(".local", path.parts)
            return original_iterdir(path)
        with patch.object(Path, "read_bytes", read_public), patch.object(Path, "iterdir", enumerate_public):
            report = installer.install(self.root, self.target)
        self.assertEqual(set(report["migrated_skills"]), set(old))
        self.assertFalse(report["private_data_migrated"])
        new = builder.public_skills(self.root)
        for name, files in new.items():
            directory = self.target / name
            self.assertEqual((resolve_canonical_directory(directory) / "SKILL.md").read_bytes(), new[builder.NAME]["SKILL.md"])
            receipt = json.loads((directory / installer.INSTALL_MANIFEST).read_bytes())
            self.assertEqual(receipt["source"], builder.SOURCE)
            self.assertEqual(receipt["canonical"], "mob-write")
            for relative, data in files.items():
                self.assertEqual((directory / relative).read_bytes(), data)
            if name in old:
                self.assertEqual((directory / ".local/profile.md").read_text(), "SYNTHETIC_PRIVATE_SENTINEL")
                self.assertEqual(receipt["migrated_from"], {"source": builder.LEGACY_SOURCE,
                                 "canonical": "wordaim", "version": "0.4.0-rc.1"})
                self.assertFalse((directory / installer.LEGACY_INSTALL_MANIFEST).exists())
                for relative in old[name].keys() - files.keys():
                    self.assertFalse((directory / relative).exists())
        self.assertEqual(notes.read_text(), "user-owned notes")
        self.assertEqual(env.read_text(), "SYNTHETIC_ENV_SENTINEL")
        receipts = {(self.target / name / installer.INSTALL_MANIFEST).read_bytes() for name in old}
        self.assertEqual(installer.install(self.root, self.target)["migrated_skills"], [])
        self.assertEqual(receipts, {(self.target / name / installer.INSTALL_MANIFEST).read_bytes() for name in old})

    def test_changed_rc1_public_file_blocks_the_whole_migration(self):
        old = self.legacy_install_fixture()
        changed = self.target / "wordaim/references/work.md"
        changed.write_text("user edits")
        with self.assertRaisesRegex(installer.InstallError, "Public file changed"):
            installer.install(self.root, self.target)
        self.assertFalse((self.target / "mob-write").exists())
        self.assertEqual((self.target / "mob-social-writing/SKILL.md").read_bytes(), old["mob-social-writing"]["SKILL.md"])
        self.assertEqual(changed.read_text(), "user edits")

    def test_legacy_receipt_identity_is_an_exact_allowlist(self):
        self.legacy_install_fixture()
        directory = self.target / "wordaim"
        path = directory / installer.LEGACY_INSTALL_MANIFEST
        original = json.loads(path.read_bytes())
        for patch_values in ({"source": "https://example.com/wordaim"},
                             {"canonical": "mob-social-writing"}, {"skill": "mob-write"}, {"schema": 2}):
            path.write_text(json.dumps({**original, **patch_values}))
            with self.assertRaisesRegex(installer.InstallError, "source or manifest"):
                installer.install(self.root, self.target)
            self.assertFalse((self.target / "mob-write").exists())
        path.unlink()
        (directory / installer.INSTALL_MANIFEST).write_text(json.dumps(original))
        with self.assertRaisesRegex(installer.InstallError, "source or manifest"):
            installer.install(self.root, self.target)

    def test_two_receipts_are_refused_before_any_public_change(self):
        old = self.legacy_install_fixture()
        directory = self.target / "wordaim"
        old_receipt = json.loads((directory / installer.LEGACY_INSTALL_MANIFEST).read_bytes())
        new_receipt = dict(old_receipt, source=builder.SOURCE, canonical=builder.NAME)
        (directory / installer.INSTALL_MANIFEST).write_text(json.dumps(new_receipt))
        with self.assertRaisesRegex(installer.InstallError, "Conflicting install receipts"):
            installer.install(self.root, self.target)
        self.assertFalse((self.target / "mob-write").exists())
        self.assertEqual((directory / "SKILL.md").read_bytes(), old["wordaim"]["SKILL.md"])

    def test_legacy_receipt_symlink_and_corrupt_content_hash_rejected(self):
        self.legacy_install_fixture()
        path = self.target / "wordaim" / installer.LEGACY_INSTALL_MANIFEST
        original = path.read_bytes()
        secret = self.base / "synthetic-secret"
        secret.write_text("SYNTHETIC_PRIVATE_SENTINEL")
        path.unlink()
        path.symlink_to(secret)
        with self.assertRaisesRegex(ValueError, "symlink"):
            installer.install(self.root, self.target)
        self.assertFalse((self.target / "mob-write").exists())
        path.unlink()
        corrupt = dict(json.loads(original), skill_content_sha256="0" * 64)
        path.write_text(json.dumps(corrupt))
        with self.assertRaisesRegex(installer.InstallError, "Public content hash"):
            installer.install(self.root, self.target)


if __name__ == "__main__":
    unittest.main()
