#!/usr/bin/env python3
"""Keep local social-writing examples as data, and retrieve them without posting.

No dependencies, credentials, model calls, or execution of corpus content.
Run ``python3 scripts/corpus.py --help`` for the command interface.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request

import private_data


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = SKILL_ROOT / ".local"
REFERENCE_REVISION = "321c769739b823de5eb94eb3a52aa1974fe783a2"
REFERENCE_URL = (
    "https://raw.githubusercontent.com/MengTo/Skills/"
    + REFERENCE_REVISION
    + "/agent-skills/codex/write-like-meng-on-x/references/tweet-corpus.jsonl"
)
REFERENCE_SHA256 = "8b7b1657e039f443ac11d0a1149c676300d3a336c3117bd7de8091f5ee34c5b6"
MAX_DOWNLOAD_BYTES = 1024 * 1024
DOWNLOAD_TIMEOUT_SECONDS = 15
MAX_FILE_BYTES = 5 * 1024 * 1024
FORMATS = {"reply", "post", "quote"}
ORIGINS = {"human_authored", "ai_draft", "external_reference"}
FEEDBACK = {"unreviewed", "approved", "rejected"}
REQUIRED_FIELDS = {
    "id", "platform", "format", "intent", "author", "origin", "feedback",
    "feedback_note", "text", "parent_text", "source_url",
}
OPTIONAL_FIELDS = {"source_revision", "external_context"}


class CorpusError(ValueError):
    """A bounded, user-readable corpus validation error."""


def validate_record(record: object) -> dict:
    if not isinstance(record, dict):
        raise CorpusError("Each sample must be a JSON object")
    missing = REQUIRED_FIELDS - record.keys()
    unknown = record.keys() - REQUIRED_FIELDS - OPTIONAL_FIELDS
    if missing:
        raise CorpusError("Missing fields: " + ", ".join(sorted(missing)))
    if unknown:
        raise CorpusError("Unknown fields: " + ", ".join(sorted(unknown)))
    result = dict(record)
    for key in ("id", "platform", "format", "intent", "author", "origin", "feedback", "text"):
        if not isinstance(result[key], str) or not result[key].strip():
            raise CorpusError(f"{key} must be a nonempty string")
    for key, choices in (("format", FORMATS), ("origin", ORIGINS), ("feedback", FEEDBACK)):
        if result[key] not in choices:
            raise CorpusError(f"Invalid {key}: expected one of {', '.join(sorted(choices))}")
    if not isinstance(result["feedback_note"], str):
        raise CorpusError("feedback_note must be a string")
    if result["feedback"] != "unreviewed" and not result["feedback_note"].strip():
        raise CorpusError("approved/rejected samples require a nonempty feedback_note")
    for key in ("parent_text", "source_url"):
        if result[key] is not None and (not isinstance(result[key], str) or not result[key].strip()):
            raise CorpusError(f"{key} must be null or a nonempty string")
    if result["source_url"] is not None and not result["source_url"].startswith(("https://", "http://")):
        raise CorpusError("source_url must be an http(s) URL or null")
    for key in OPTIONAL_FIELDS & result.keys():
        if not isinstance(result[key], str) or not result[key].strip():
            raise CorpusError(f"{key} must be a nonempty string when present")
    if result["origin"] == "external_reference":
        result["external_context"] = (
            "parent_missing" if result["parent_text"] is None else "parent_provided_unverified"
        )
    return result


def parse_jsonl(raw: bytes, label: str) -> list[dict]:
    if len(raw) > MAX_FILE_BYTES:
        raise CorpusError(f"{label}: file exceeds {MAX_FILE_BYTES} bytes")
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CorpusError(f"{label}: expected UTF-8") from exc
    rows = []
    for number, line in enumerate(content.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(validate_record(json.loads(line)))
        except (CorpusError, json.JSONDecodeError) as exc:
            raise CorpusError(f"{label}, line {number}: {exc}") from exc
    return rows


def read_records(path: Path, *, missing_ok: bool = True) -> list[dict]:
    try:
        with path.open("rb") as source:
            raw = source.read(MAX_FILE_BYTES + 1)
    except FileNotFoundError:
        if missing_ok:
            return []
        raise CorpusError(f"File does not exist: {path}") from None
    return parse_jsonl(raw, str(path))


def normalize_text(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).split())


def context_key(record: dict) -> tuple:
    author = unicodedata.normalize("NFKC", record["author"]).strip().casefold().lstrip("@")
    parent = None if record["parent_text"] is None else normalize_text(record["parent_text"])
    return (record["platform"].strip().casefold(), author, record["origin"],
            record["format"], normalize_text(record["text"]), parent)


def sample_key(record: dict) -> tuple:
    return context_key(record) + (record["feedback"], normalize_text(record["feedback_note"]))


def without_feedback(record: dict) -> dict:
    return {key: value for key, value in record.items() if key not in {"feedback", "feedback_note"}}


def merge_unique(existing: list[dict], incoming: list[dict]) -> tuple[list[dict], int]:
    by_id = {}
    by_content = set()
    merged = []
    duplicates = 0
    for record in existing + incoming:
        identifier = record["id"]
        if identifier in by_id and by_id[identifier] != record:
            raise CorpusError(f"Conflicting content for id {identifier!r}; use a new id for a revision")
        same_id = identifier in by_id
        by_id[identifier] = record
        key = sample_key(record)
        if same_id or key in by_content:
            duplicates += 1
            continue
        by_content.add(key)
        merged.append(record)
    return merged, duplicates


def write_atomic(path: Path, records: list[dict]) -> None:
    raw = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records).encode("utf-8")
    if len(raw) > MAX_FILE_BYTES:
        raise CorpusError(f"Output exceeds {MAX_FILE_BYTES} bytes; existing local corpus was not changed")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temp_name = tempfile.mkstemp(prefix=".corpus-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(raw)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def download_reference() -> bytes:
    deadline = time.monotonic() + DOWNLOAD_TIMEOUT_SECONDS
    request = urllib.request.Request(REFERENCE_URL, headers={"User-Agent": "social-writing-corpus/1"})
    with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
        chunks = []
        count = 0
        while True:
            if time.monotonic() >= deadline:
                raise CorpusError("Reference download exceeded its time limit")
            chunk = response.read(min(65536, MAX_DOWNLOAD_BYTES + 1 - count))
            if time.monotonic() >= deadline:
                raise CorpusError("Reference download exceeded its time limit")
            if not chunk:
                return b"".join(chunks)
            count += len(chunk)
            if count > MAX_DOWNLOAD_BYTES:
                raise CorpusError("Reference download exceeded its size limit")
            chunks.append(chunk)


def convert_reference(raw: bytes) -> list[dict]:
    if len(raw) > MAX_DOWNLOAD_BYTES or hashlib.sha256(raw).hexdigest() != REFERENCE_SHA256:
        raise CorpusError("Reference SHA256 mismatch; existing local corpus was not changed")
    try:
        source_rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
        if len(source_rows) != 40:
            raise CorpusError("Expected exactly 40 pinned reference samples")
        records = []
        for row in source_rows:
            records.append(validate_record({
                "id": "mengto:" + row["id"], "platform": "x",
                "format": "post" if row["format"] == "original" else row["format"],
                "intent": "unknown", "author": "MengTo", "origin": "external_reference",
                "feedback": "unreviewed", "feedback_note": "", "text": row["text"],
                "parent_text": None, "source_url": row["url"],
                "source_revision": REFERENCE_REVISION, "external_context": "parent_missing",
            }))
    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CorpusError("Pinned reference data has an unexpected schema") from exc
    # Do not silently discard anything in this pinned source.
    unique, _ = merge_unique([], records)
    if len(unique) != 40:
        raise CorpusError("Pinned reference has duplicate samples")
    return records


def load_all(data_dir: Path) -> list[dict]:
    local = read_records(data_dir / "corpus.jsonl")
    reference = read_records(data_dir / "reference-corpus.jsonl")
    return combine_local_reference(local, reference)


def combine_local_reference(local: list[dict], reference: list[dict]) -> list[dict]:
    local, _ = merge_unique([], local)
    reference, _ = merge_unique([], reference)
    reference_by_id = {row["id"]: row for row in reference}
    local_ids = set()
    for row in local:
        local_ids.add(row["id"])
        source = reference_by_id.get(row["id"])
        if source is not None and without_feedback(row) != without_feedback(source):
            raise CorpusError(f"Local override for {row['id']!r} may change only feedback and feedback_note")
    return merge_unique(local, [row for row in reference if row["id"] not in local_ids])[0]


def select_samples(records: list[dict], *, intent: str | None = None, query: str | None = None,
                   approved: bool = False, rejected: bool = False, limit: int = 5) -> list[dict]:
    selected = []
    words = query.casefold().split() if query else []
    # Preserve history on disk, but use the last explicit judgment for a given context.
    # Unreviewed source records cannot undo a later local approval/rejection.
    effective = {}
    for row in records:
        key = context_key(row)
        previous = effective.get(key)
        if previous is None or row["feedback"] != "unreviewed" or row["feedback_note"].strip():
            effective[key] = row
    for row in effective.values():
        if rejected:
            if row["feedback"] != "rejected":
                continue
        elif approved:
            if row["feedback"] != "approved":
                continue
        elif row["feedback"] == "rejected" or (row["origin"] == "ai_draft" and row["feedback"] == "unreviewed"):
            continue
        if intent and row["intent"].casefold() != intent.casefold():
            continue
        searchable = " ".join((row["text"], row["parent_text"] or "", row["intent"], row["feedback_note"])).casefold()
        if words and not all(word in searchable for word in words):
            continue
        selected.append(row)
    # Stable within each group: approved author examples, human writing, external examples.
    def priority(row: dict) -> tuple[int, int]:
        return (
            2 if row["origin"] == "external_reference" else (0 if row["feedback"] == "approved" else 1),
            0 if row["feedback"] == "approved" else 1,
        )
    selected.sort(key=priority)
    return [dict(row, parent_missing=row["parent_text"] is None) for row in selected[:limit]]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path,
                        help="Explicit data directory; otherwise connected bundle or skill root/.local")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("fetch-reference", help="Fetch the fixed, hash-verified public reference corpus")
    add = commands.add_parser("add", help="Validate and atomically import a JSONL file")
    add.add_argument("--file", type=Path, required=True)
    search = commands.add_parser("search", help="Return matching samples with provenance")
    search.add_argument("--intent")
    search.add_argument("--query")
    feedback = search.add_mutually_exclusive_group()
    feedback.add_argument("--approved", action="store_true")
    feedback.add_argument("--rejected", action="store_true")
    search.add_argument("--limit", type=int, default=5)
    feedback_command = commands.add_parser("feedback", help="Persist a judgment without changing text or provenance")
    feedback_command.add_argument("--id", required=True)
    feedback_command.add_argument("--status", choices=sorted(FEEDBACK), required=True)
    feedback_command.add_argument("--note", required=True)
    commands.add_parser("stats", help="Count local examples without changing them")
    args = parser.parse_args(argv)
    if args.command == "search" and args.limit < 1:
        parser.error("--limit must be positive")
    try:
        data_dir = private_data.data_directory(SKILL_ROOT, args.data_dir)
        if args.command == "fetch-reference":
            rows = convert_reference(download_reference())
            combine_local_reference(read_records(data_dir / "corpus.jsonl"), rows)
            path = data_dir / "reference-corpus.jsonl"
            write_atomic(path, rows)
            result = {"count": len(rows), "path": str(path), "source_revision": REFERENCE_REVISION,
                      "sha256": REFERENCE_SHA256, "origin": "external_reference", "feedback": "unreviewed"}
        elif args.command == "add":
            incoming = read_records(args.file, missing_ok=False)
            local = read_records(data_dir / "corpus.jsonl")
            reference = read_records(data_dir / "reference-corpus.jsonl")
            existing = combine_local_reference(local, reference)
            merged, _ = merge_unique(existing, incoming)
            additions = merged[len(existing):]
            path = data_dir / "corpus.jsonl"
            write_atomic(path, local + additions)
            result = {"added": len(additions), "duplicates": len(incoming) - len(additions),
                      "total_local": len(local) + len(additions), "path": str(path)}
        elif args.command == "feedback":
            rows = load_all(data_dir)
            matching = [row for row in rows if row["id"] == args.id]
            if not matching:
                raise CorpusError(f"Unknown sample id: {args.id!r}")
            if not args.note.strip():
                raise CorpusError("feedback requires a nonempty --note")
            revised = validate_record(dict(matching[0], feedback=args.status, feedback_note=args.note))
            path = data_dir / "corpus.jsonl"
            local = read_records(path)
            # Appending the revision also makes it the latest explicit judgment.
            local = [row for row in local if row["id"] != args.id] + [revised]
            combine_local_reference(local, read_records(data_dir / "reference-corpus.jsonl"))
            write_atomic(path, local)
            result = {"id": args.id, "feedback": args.status, "origin": revised["origin"],
                      "author": revised["author"], "path": str(path)}
        elif args.command == "search":
            result = {"samples": select_samples(load_all(data_dir), intent=args.intent, query=args.query,
                       approved=args.approved, rejected=args.rejected, limit=args.limit)}
        else:
            rows = load_all(data_dir)
            result = {"data_dir": str(data_dir), "total": len(rows),
                      "by_origin": dict(Counter(row["origin"] for row in rows)),
                      "by_feedback": dict(Counter(row["feedback"] for row in rows)),
                      "by_format": dict(Counter(row["format"] for row in rows)),
                      "missing_parent": sum(row["parent_text"] is None for row in rows)}
    except (ValueError, OSError, urllib.error.URLError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
