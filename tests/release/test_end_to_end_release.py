from __future__ import annotations

import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


def test_end_to_end_release_candidate():
    run("python3", "scripts/validate_project.py", "--project-root", ".")
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        run("python3", "scripts/package_release.py", "--project-root", ".", "--output-dir", str(out), "--version", "v1.0.0-rc1")
        archive = out / "ea-stodjare-1.0.0-rc1.zip"
        assert archive.exists()
        unpack = out / "unpacked"
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(unpack)
        released_root = unpack / "ea-stodjare-1.0.0-rc1"
        assert (released_root / "custom-gpt" / "instructions.md").exists()
        assert (released_root / "custom-gpt" / "knowledge" / "00-knowledge-index.md").exists()
        run("python3", "scripts/validate_project.py", "--project-root", str(released_root), cwd=released_root)
