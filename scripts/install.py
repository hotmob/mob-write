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
LEGACY_SKILLS = {"wordaim", "chinese-writing", "mob-social-writing"}
SCHEMA = 1
VERSION_PATTERN = r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][a-zA-Z0-9.-]+)?"


class InstallError(ValueError):
    """An install was refused before changing public files."""


@dataclass(frozen=True)
class InstallState:
    files: dict[str, str]
    receipt: str | None = None
    migrated_from: dict | None = None


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
        manifest = json.loads(manifest_path.read_bytes())
    except (ValueError, OSError) as exc:
        raise InstallError(f"Unreadable install manifest: {manifest_path}") from exc
    if (not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA
            or manifest.get("skill") != skill or not isinstance(manifest.get("version"), str)
            or not re.fullmatch(VERSION_PATTERN, manifest["version"])
            or not isinstance(manifest.get("files"), dict)):
        raise InstallError(f"Install source or manifest does not match Mob Write: {directory}")
    legacy = receipt == LEGACY_INSTALL_MANIFEST
    recognized = ((legacy and skill in LEGACY_SKILLS
                   and manifest.get("source") == builder.LEGACY_SOURCE
                   and manifest.get("canonical") == builder.LEGACY_NAME)
                  or (not legacy and skill in {builder.NAME, *builder.ALIAS_SOURCES}
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
                or history.get("source") != builder.LEGACY_SOURCE
                or history.get("canonical") != builder.LEGACY_NAME
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
    return InstallState(previous, receipt, migrated_from)


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


def install(root: Path, skills_dir: Path) -> dict:
    """Preflight all four public installs, then replace only managed files."""
    skills_dir = skills_dir.expanduser().absolute()
    builder.reject_symlinks(skills_dir)
    if skills_dir.exists() and not skills_dir.is_dir():
        raise InstallError(f"Skills directory is not a directory: {skills_dir}")
    skills = builder.public_skills(root)
    version = builder.plugin_manifest(root)[0]["version"]
    previous = {name: inspect_install(skills_dir / name, name, files)
                for name, files in skills.items()}
    # Do not create any target until all source and destination checks succeed.
    for name, files in skills.items():
        directory = skills_dir / name
        for relative, data in files.items():
            atomic_write(installed_path(directory, relative), data)
        for relative in previous[name].files.keys() - files.keys():
            installed_path(directory, relative).unlink()
        manifest = {
            "schema": SCHEMA, "source": builder.SOURCE, "skill": name,
            "version": version, "canonical": builder.NAME,
            "canonical_content_sha256": builder.content_sha256(skills[builder.NAME]),
            "skill_content_sha256": builder.content_sha256(files),
            "files": {relative: digest(data) for relative, data in sorted(files.items())},
        }
        if previous[name].migrated_from is not None:
            manifest["migrated_from"] = previous[name].migrated_from
        atomic_write(directory / INSTALL_MANIFEST,
                     (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        if previous[name].receipt == LEGACY_INSTALL_MANIFEST:
            retired_receipt = directory / LEGACY_INSTALL_MANIFEST
            builder.reject_symlinks(retired_receipt)
            retired_receipt.unlink()
    return {"source": builder.SOURCE, "version": version,
            "skills_dir": str(skills_dir), "skills": list(skills),
            "private_data_migrated": False,
            "migrated_skills": [name for name, state in previous.items()
                                if state.receipt == LEGACY_INSTALL_MANIFEST]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True,
                        help="Explicit destination; no global directory is selected automatically")
    args = parser.parse_args(argv)
    try:
        report = install(ROOT, args.skills_dir)
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
