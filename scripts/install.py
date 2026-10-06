#!/usr/bin/env python3
"""Install public Mob Write skills into an explicitly chosen skills directory.

Only same-source, hash-verified managed installs may be upgraded. Private .local
directories are never read, copied, removed, or migrated by this installer.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

import build_chatgpt as builder


ROOT = builder.ROOT
INSTALL_MANIFEST = ".mob-write-install.json"
LEGACY_INSTALL_MANIFEST = ".wordaim-install.json"
LEGACY_SKILLS = ("wordaim", "chinese-writing", "mob-social-writing")
LEGACY_SOURCE = "https://github.com/hotmob/mob-social-writing"
LEGACY_NAME = "wordaim"
SCHEMA = 1
VERSION_PATTERN = r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][a-zA-Z0-9.-]+)?"


class InstallError(ValueError):
    """An install was refused before changing public files."""


@dataclass(frozen=True)
class InstallState:
    files: dict[str, str]
    receipt: str | None = None
    migrated_from: dict | None = None
    public_data: dict[str, bytes] | None = None
    receipt_data: bytes | None = None


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def installed_path(directory: Path, relative: str) -> Path:
    builder.safe_relative(relative)
    path = directory / relative
    builder.reject_symlinks(path)
    return path


def inspect_install(directory: Path, skill: str, incoming: dict[str, bytes]) -> InstallState:
    """Preflight managed public paths only; never enumerate private contents."""
    builder.reject_symlinks(directory)
    if not directory.exists():
        return InstallState({})
    if not directory.is_dir():
        raise InstallError(f"Installation target is not a directory: {directory}")
    receipts = []
    for name in (INSTALL_MANIFEST, LEGACY_INSTALL_MANIFEST):
        path = directory / name
        builder.reject_symlinks(path)
        if path.exists():
            if not path.is_file():
                raise InstallError(f"Install receipt is not a file: {path}")
            receipts.append(name)
    if len(receipts) > 1:
        raise InstallError(f"Conflicting install receipts at {directory}; review them before retrying")
    if not receipts:
        raise InstallError(
            f"Unmanaged installation at {directory}. Review its source and public changes, "
            "then move it aside yourself before retrying. Private data has not been "
            "read or migrated; keep its original path until you choose a migration."
        )
    receipt = receipts[0]
    manifest_path = directory / receipt
    try:
        receipt_data = manifest_path.read_bytes()
        manifest = json.loads(receipt_data)
    except (ValueError, OSError) as exc:
        raise InstallError(f"Unreadable install manifest: {manifest_path}") from exc
    if (not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA
            or manifest.get("skill") != skill or not isinstance(manifest.get("version"), str)
            or not re.fullmatch(VERSION_PATTERN, manifest["version"])
            or not isinstance(manifest.get("files"), dict)):
        raise InstallError(f"Install source or manifest does not match Mob Write: {directory}")
    legacy = receipt == LEGACY_INSTALL_MANIFEST
    recognized = ((legacy and skill in LEGACY_SKILLS
                   and manifest.get("source") == LEGACY_SOURCE
                   and manifest.get("canonical") == LEGACY_NAME)
                  or (not legacy and skill in {builder.NAME, *LEGACY_SKILLS}
                      and manifest.get("source") == builder.SOURCE
                      and manifest.get("canonical") == builder.NAME))
    if not recognized:
        raise InstallError(f"Install source or manifest does not match Mob Write: {directory}")
    migrated_from = None
    if legacy:
        migrated_from = {key: manifest[key] for key in ("source", "version", "canonical")}
    elif manifest.get("migrated_from") is not None:
        history = manifest["migrated_from"]
        if (not isinstance(history, dict) or set(history) != {"source", "version", "canonical"}
                or history.get("source") != LEGACY_SOURCE
                or history.get("canonical") != LEGACY_NAME
                or not isinstance(history.get("version"), str)
                or not re.fullmatch(VERSION_PATTERN, history["version"])):
            raise InstallError(f"Invalid migration provenance: {manifest_path}")
        migrated_from = dict(history)
    previous = manifest["files"]
    if "SKILL.md" not in previous:
        raise InstallError(f"Incomplete install manifest: {manifest_path}")
    actual = {}
    for relative, expected in previous.items():
        if not isinstance(relative, str) or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise InstallError(f"Invalid public file record: {manifest_path}")
        if relative in (INSTALL_MANIFEST, LEGACY_INSTALL_MANIFEST):
            raise InstallError(f"Install manifest cannot manage itself: {manifest_path}")
        path = installed_path(directory, relative)
        data = path.read_bytes() if path.is_file() else None
        if data is None or digest(data) != expected:
            raise InstallError(
                f"Public file changed or missing: {path}. Preserve your edits and review "
                "them before reinstalling; no installation files were changed."
            )
        actual[relative] = data
    if manifest.get("skill_content_sha256") != builder.content_sha256(actual):
        raise InstallError(f"Public content hash does not match install receipt: {manifest_path}")
    for relative in incoming.keys() - previous.keys():
        path = installed_path(directory, relative)
        if path.exists():
            raise InstallError(f"New public file would overwrite an unmanaged path: {path}")
    return InstallState(previous, receipt, migrated_from, actual, receipt_data)


def inspect_legacy(directory: Path, skill: str) -> InstallState:
    """An inert old directory can retain private/unknown data after retirement."""
    builder.reject_symlinks(directory)
    if not directory.exists():
        return InstallState({})
    if not directory.is_dir():
        raise InstallError(f"Installation target is not a directory: {directory}")
    for name in ("SKILL.md", INSTALL_MANIFEST, LEGACY_INSTALL_MANIFEST):
        path = directory / name
        builder.reject_symlinks(path)
        if path.exists():
            return inspect_install(directory, skill, {})
    # Do not enumerate the directory or inspect private/unmanaged contents.
    return InstallState({})


def atomic_write(path: Path, data: bytes) -> None:
    builder.reject_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".mob-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def require_unchanged(path: Path, expected: bytes | None) -> None:
    """Recheck public state immediately before replacing or retiring a path."""
    builder.reject_symlinks(path)
    actual = path.read_bytes() if path.is_file() else None
    if (expected is None and path.exists()) or actual != expected:
        raise InstallError(f"Public path changed during installation: {path}")


def require_receipt_unchanged(directory: Path, state: InstallState) -> None:
    for name in (INSTALL_MANIFEST, LEGACY_INSTALL_MANIFEST):
        require_unchanged(directory / name, state.receipt_data if name == state.receipt else None)


def receipt_bytes(name: str, files: dict, skills: dict,
                  state: InstallState, version: str) -> bytes:
    manifest = {
        "schema": SCHEMA, "source": builder.SOURCE, "skill": name,
        "version": version, "canonical": builder.NAME,
        "canonical_content_sha256": builder.content_sha256(skills[builder.NAME]),
        "skill_content_sha256": builder.content_sha256(files),
        "files": {relative: digest(data) for relative, data in sorted(files.items())},
    }
    if state.migrated_from is not None:
        manifest["migrated_from"] = state.migrated_from
    return (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def rollback_fresh(skills_dir: Path, owned: dict[str, dict[str, bytes]]) -> None:
    """Remove only this fresh attempt's unchanged public bytes, never unknown data."""
    for name, files in owned.items():
        # Disable our entry first, then clean up other public files we wrote.
        for relative in sorted(files, key=lambda value: value != "SKILL.md"):
            expected = files[relative]
            path = skills_dir / name / relative
            try:
                builder.reject_symlinks(path)
                if path.is_file() and path.read_bytes() == expected:
                    path.unlink()
            except (ValueError, OSError):
                # A new link, edit, or inaccessible file belongs to recovery, not deletion.
                continue


def write_install(skills_dir: Path, skills: dict, previous: dict,
                  retired: dict, version: str, fresh_owned: dict) -> None:
    # Recheck all targets after backup I/O, before the first discovery change.
    for name, files in skills.items():
        state = previous[name]
        directory = skills_dir / name
        require_receipt_unchanged(directory, state)
        for relative in state.files.keys() | files.keys():
            require_unchanged(installed_path(directory, relative),
                              (state.public_data or {}).get(relative))
    for name in LEGACY_SKILLS:
        current = inspect_legacy(skills_dir / name, name)
        if current != retired.get(name, InstallState({})):
            raise InstallError(f"Public legacy entry changed during installation: {skills_dir / name}")
    for name, files in skills.items():
        directory = skills_dir / name
        state = previous[name]
        ordered = sorted(files, key=lambda relative: relative == "SKILL.md")
        for relative in ordered:
            data = files[relative]
            path = installed_path(directory, relative)
            require_unchanged(path, (state.public_data or {}).get(relative))
            atomic_write(path, data)
            if state.receipt is None:
                fresh_owned.setdefault(name, {})[relative] = data
        for relative in state.files.keys() - files.keys():
            path = installed_path(directory, relative)
            require_unchanged(path, state.public_data[relative])
            path.unlink()
        require_receipt_unchanged(directory, state)
        data = receipt_bytes(name, files, skills, state, version)
        atomic_write(directory / INSTALL_MANIFEST, data)
        if state.receipt is None:
            fresh_owned.setdefault(name, {})[INSTALL_MANIFEST] = data
        if state.receipt == LEGACY_INSTALL_MANIFEST:
            retired_receipt = directory / LEGACY_INSTALL_MANIFEST
            require_unchanged(retired_receipt, state.receipt_data)
            retired_receipt.unlink()
    for name, state in retired.items():
        directory = skills_dir / name
        require_receipt_unchanged(directory, state)
        # Keep the ignore file to protect private data that stays at its old path.
        for relative in state.files:
            if relative != ".gitignore":
                path = installed_path(directory, relative)
                require_unchanged(path, state.public_data[relative])
                path.unlink()
        require_unchanged(directory / state.receipt, state.receipt_data)
        (directory / state.receipt).unlink()


def install(root: Path, skills_dir: Path, backup_dir: Path | None = None) -> dict:
    """Install one entry and retire verified legacy public entries with a backup."""
    skills_dir = skills_dir.expanduser().absolute()
    builder.reject_symlinks(skills_dir)
    if skills_dir.exists() and not skills_dir.is_dir():
        raise InstallError(f"Skills directory is not a directory: {skills_dir}")
    skills = builder.public_skills(root)
    version = builder.plugin_manifest(root)[0]["version"]
    previous = {name: inspect_install(skills_dir / name, name, files)
                for name, files in skills.items()}
    retired = {name: inspect_legacy(skills_dir / name, name) for name in LEGACY_SKILLS}
    retired = {name: state for name, state in retired.items() if state.receipt}
    backup = None
    if retired:
        if backup_dir is None:
            raise InstallError("Managed legacy entries need --backup-dir outside the skills directory before retirement")
        backup_dir = backup_dir.expanduser().absolute()
        builder.reject_symlinks(backup_dir)
        if backup_dir.exists() and not backup_dir.is_dir():
            raise InstallError(f"Backup target is not a directory: {backup_dir}")
        if backup_dir.resolve() == skills_dir.resolve() or skills_dir.resolve() in backup_dir.resolve().parents:
            raise InstallError("Backup directory must be outside the skills discovery directory")
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup = Path(tempfile.mkdtemp(prefix="mob-write-retired-", dir=backup_dir))
        # Complete all recoverable public backups before changing discovery paths.
        for name, state in retired.items():
            for relative, data in state.public_data.items():
                atomic_write(backup / name / relative, data)
            atomic_write(backup / name / state.receipt, state.receipt_data)
    fresh_owned = {}
    try:
        write_install(skills_dir, skills, previous, retired, version, fresh_owned)
    except (ValueError, OSError) as exc:
        rollback_fresh(skills_dir, fresh_owned)
        if backup:
            raise InstallError(f"{exc}. Verified legacy public backup: {backup}. Installation may be partially updated; preserve it before recovery.") from exc
        raise
    return {"source": builder.SOURCE, "version": version,
            "skills_dir": str(skills_dir), "skills": list(skills),
            "private_data_migrated": False,
            "retired_skills": list(retired), "backup_dir": str(backup) if backup else None,
            "migrated_skills": [name for name, state in retired.items()
                                if state.receipt == LEGACY_INSTALL_MANIFEST]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True,
                        help="Explicit destination; no global directory is selected automatically")
    parser.add_argument("--backup-dir", type=Path,
                        help="Outside skills discovery; required to retire verified legacy public entries")
    args = parser.parse_args(argv)
    try:
        report = install(ROOT, args.skills_dir, args.backup_dir)
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
