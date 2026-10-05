#!/usr/bin/env python3
"""Install public WordAim skills into an explicitly chosen skills directory.

Only same-source, hash-verified managed installs may be upgraded. Private .local
directories are never read, copied, removed, or migrated by this installer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

import build_chatgpt as builder


ROOT = builder.ROOT
INSTALL_MANIFEST = ".wordaim-install.json"
SCHEMA = 1


class InstallError(ValueError):
    """An install was refused before changing public files."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def installed_path(directory: Path, relative: str) -> Path:
    builder.safe_relative(relative)
    path = directory / relative
    builder.reject_symlinks(path)
    return path


def inspect_install(directory: Path, skill: str, incoming: dict[str, bytes]) -> dict[str, str]:
    """Preflight managed public paths only; never enumerate private contents."""
    builder.reject_symlinks(directory)
    if not directory.exists():
        return {}
    if not directory.is_dir():
        raise InstallError(f"Installation target is not a directory: {directory}")
    manifest_path = directory / INSTALL_MANIFEST
    builder.reject_symlinks(manifest_path)
    if not manifest_path.is_file():
        raise InstallError(
            f"Unmanaged installation at {directory}. Review its source and public changes, "
            "then move it aside yourself before retrying. Private data has not been "
            "read or migrated; keep its original path until you choose a migration."
        )
    try:
        manifest = json.loads(manifest_path.read_bytes())
    except (ValueError, OSError) as exc:
        raise InstallError(f"Unreadable install manifest: {manifest_path}") from exc
    if (not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA
            or manifest.get("source") != builder.SOURCE or manifest.get("skill") != skill
            or not isinstance(manifest.get("version"), str)
            or not isinstance(manifest.get("files"), dict)):
        raise InstallError(f"Install source or manifest does not match WordAim: {directory}")
    previous = manifest["files"]
    if "SKILL.md" not in previous:
        raise InstallError(f"Incomplete install manifest: {manifest_path}")
    for relative, expected in previous.items():
        if not isinstance(relative, str) or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise InstallError(f"Invalid public file record: {manifest_path}")
        if relative == INSTALL_MANIFEST:
            raise InstallError(f"Install manifest cannot manage itself: {manifest_path}")
        path = installed_path(directory, relative)
        if not path.is_file() or digest(path.read_bytes()) != expected:
            raise InstallError(
                f"Public file changed or missing: {path}. Preserve your edits and review "
                "them before reinstalling; no installation files were changed."
            )
    for relative in incoming.keys() - previous.keys():
        path = installed_path(directory, relative)
        if path.exists():
            raise InstallError(f"New public file would overwrite an unmanaged path: {path}")
    return previous


def atomic_write(path: Path, data: bytes) -> None:
    builder.reject_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".wordaim-", dir=path.parent)
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
    """Preflight all three public installs, then replace only managed files."""
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
        for relative in previous[name].keys() - files.keys():
            installed_path(directory, relative).unlink()
        manifest = {
            "schema": SCHEMA, "source": builder.SOURCE, "skill": name,
            "version": version, "canonical": builder.NAME,
            "canonical_content_sha256": builder.content_sha256(skills[builder.NAME]),
            "skill_content_sha256": builder.content_sha256(files),
            "files": {relative: digest(data) for relative, data in sorted(files.items())},
        }
        atomic_write(directory / INSTALL_MANIFEST,
                     (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"source": builder.SOURCE, "version": version,
            "skills_dir": str(skills_dir), "skills": list(skills),
            "private_data_migrated": False}


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
