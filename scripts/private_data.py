#!/usr/bin/env python3
"""Initialize or explicitly connect a replaceable local writing bundle.

No account access, discovery scan, content upload or profile-body reads.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets/private-bundle-template"
CONFIG = ".local/config.json"


def regular_path(path: Path) -> None:
    current = Path(path.absolute().anchor)
    for part in path.absolute().parts[1:]:
        current /= part
        if current.is_symlink():
            raise ValueError(f"Refusing symlink in private connection: {current}")


def read_json(path: Path) -> dict:
    regular_path(path)
    with path.open("rb") as stream:
        raw = stream.read(16385)
    if len(raw) > 16384:
        raise ValueError(f"Private metadata is too large: {path}")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a metadata object: {path}")
    return value


def inspect_bundle(directory: Path) -> dict:
    regular_path(directory)
    manifest = read_json(directory / "bundle.json")
    if (set(manifest) != {"schema", "owner", "scope"}
            or type(manifest["schema"]) is not int or manifest["schema"] != 1
            or any(not isinstance(manifest[key], str) or not manifest[key].strip()
                   for key in ("owner", "scope"))):
        raise ValueError("Bundle requires schema=1 and nonempty owner/scope")
    for name in ("profile.md", "voice-notes.md", "corpus.jsonl", "reference-corpus.jsonl"):
        path = directory / name
        regular_path(path)
        if path.exists() and not path.is_file():
            raise ValueError(f"Bundle member must be a regular file: {path}")
    if not (directory / "profile.md").is_file():
        raise ValueError("Bundle requires profile.md; optional members may be absent")
    return manifest


def data_directory(skill_dir: Path, explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()
    path = skill_dir / CONFIG
    if not path.exists() and not path.is_symlink():
        return skill_dir / ".local"
    config = read_json(path)
    if (set(config) != {"schema", "data_dir"} or type(config["schema"]) is not int
            or config["schema"] != 1 or not isinstance(config["data_dir"], str)
            or not Path(config["data_dir"]).is_absolute()):
        raise ValueError("Connection requires schema=1 and an absolute data_dir")
    directory = Path(config["data_dir"])
    inspect_bundle(directory)
    return directory


def write_private(path: Path, value: dict) -> None:
    regular_path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(prefix=".writing-config-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def initialize(directory: Path, owner: str, scope: str) -> dict:
    if not owner.strip() or not scope.strip():
        raise ValueError("owner and scope must be nonempty")
    regular_path(directory)
    if directory.exists():
        raise ValueError("Refusing to overwrite an existing private directory")
    directory.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    stage = Path(tempfile.mkdtemp(prefix=".writing-bundle-", dir=directory.parent))
    try:
        for name in ("README.md", "profile.md", "voice-notes.md", "corpus.jsonl"):
            shutil.copyfile(TEMPLATE / name, stage / name)
            (stage / name).chmod(0o600)
        write_private(stage / "bundle.json", {"schema": 1, "owner": owner, "scope": scope})
        # Never replace a directory that appeared while the template was prepared.
        directory.mkdir(mode=0o700)
        for path in stage.iterdir():
            path.rename(directory / path.name)
    finally:
        shutil.rmtree(stage)
    return {"data_dir": str(directory), "initialized": True, "active_samples": 0}


def connect(skill_dir: Path, directory: Path) -> dict:
    regular_path(skill_dir)
    if "name: mob-write\n" not in (skill_dir / "SKILL.md").read_text(encoding="utf-8")[:2048]:
        raise ValueError("Target must be a Mob Write skill directory")
    manifest = inspect_bundle(directory)
    write_private(skill_dir / CONFIG, {"schema": 1, "data_dir": str(directory)})
    return {"connected": True, "data_dir": str(directory), **manifest}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create an empty private template; never overwrite")
    init.add_argument("--data-dir", type=Path, required=True)
    init.add_argument("--owner", required=True)
    init.add_argument("--scope", required=True)
    bind = commands.add_parser("connect", help="Explicitly select a private bundle")
    bind.add_argument("--data-dir", type=Path, required=True)
    bind.add_argument("--skill-dir", type=Path, default=ROOT)
    show = commands.add_parser("show", help="Show connection metadata only, not private prose")
    show.add_argument("--skill-dir", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.data_dir.expanduser().absolute(), args.owner, args.scope)
        elif args.command == "connect":
            result = connect(args.skill_dir.expanduser().absolute(), args.data_dir.expanduser().absolute())
        else:
            directory = data_directory(args.skill_dir.expanduser().absolute())
            connected = (args.skill_dir.expanduser().absolute() / CONFIG).exists()
            result = {"connected": connected, "data_dir": str(directory)}
            if connected:
                result.update(inspect_bundle(directory))
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
