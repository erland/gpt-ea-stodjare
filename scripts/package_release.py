#!/usr/bin/env python3
"""Create a deterministic EA Stödjare release ZIP.

Version precedence:
1. --version
2. EA_STODJARE_VERSION
3. GitHub tag (GITHUB_REF_TYPE=tag + GITHUB_REF_NAME)
4. exact Git tag

The archive is byte-stable for identical source trees and version values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath

SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+]([0-9A-Za-z.-]+))?$")
FIXED_ZIP_DT = (1980, 1, 1, 0, 0, 0)
EXCLUDED_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", "dist", "build"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def normalize_version(raw: str) -> str:
    raw = raw.strip()
    match = SEMVER_RE.fullmatch(raw)
    if not match:
        raise ValueError(f"Version måste vara semver, exempelvis v1.0.0 eller 1.0.0: {raw!r}")
    core = ".".join(match.group(i) for i in (1, 2, 3))
    suffix = match.group(4)
    return f"{core}-{suffix}" if suffix and "-" in raw else (f"{core}+{suffix}" if suffix and "+" in raw else core)


def exact_git_tag(root: Path) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "describe", "--tags", "--exact-match"], cwd=root,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
        )
        tag = proc.stdout.strip()
        return tag if proc.returncode == 0 and tag else None
    except OSError:
        return None


def resolve_version(root: Path, explicit: str | None) -> tuple[str, str]:
    if explicit:
        return normalize_version(explicit), "argument"
    env = os.getenv("EA_STODJARE_VERSION")
    if env:
        return normalize_version(env), "EA_STODJARE_VERSION"
    if os.getenv("GITHUB_REF_TYPE") == "tag" and os.getenv("GITHUB_REF_NAME"):
        return normalize_version(os.environ["GITHUB_REF_NAME"]), "GitHub tag"
    tag = exact_git_tag(root)
    if tag:
        return normalize_version(tag), "Git tag"
    raise RuntimeError("Ingen releaseversion kunde fastställas. Använd Git-tag vX.Y.Z eller --version.")


def include_file(root: Path, path: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_entry(zf: zipfile.ZipFile, arcname: str, data: bytes, executable: bool = False) -> None:
    info = zipfile.ZipInfo(arcname, date_time=FIXED_ZIP_DT)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    mode = 0o755 if executable else 0o644
    info.external_attr = (mode & 0xFFFF) << 16
    zf.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--output-dir", default="dist")
    ap.add_argument("--version")
    ap.add_argument("--basename", default="ea-stodjare")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    out = Path(args.output_dir)
    if not out.is_absolute():
        out = root / out
    out.mkdir(parents=True, exist_ok=True)

    version, source = resolve_version(root, args.version)
    zip_path = out / f"{args.basename}-{version}.zip"
    metadata_path = out / f"{args.basename}-{version}.release.json"
    archive_root = f"{args.basename}-{version}"

    files = sorted((p for p in root.rglob("*") if include_file(root, p)), key=lambda p: p.relative_to(root).as_posix())
    # Never package an existing release output through an alternate output directory inside project root.
    files = [p for p in files if p != zip_path and p != metadata_path]

    with zipfile.ZipFile(zip_path, "w") as zf:
        for path in files:
            rel = path.relative_to(root).as_posix()
            executable = rel.startswith("scripts/") and path.suffix in {".py", ".sh"}
            arcname = str(PurePosixPath(archive_root) / rel)
            write_entry(zf, arcname, path.read_bytes(), executable=executable)

    metadata = {
        "product": "EA Stödjare",
        "version": version,
        "version_source": source,
        "archive": zip_path.name,
        "archive_sha256": sha256(zip_path),
        "file_count": len(files),
        "deterministic_zip": True,
    }
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
