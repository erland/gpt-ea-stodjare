from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "package_release.py"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_package(out: Path, version: str = "v1.2.3") -> tuple[Path, Path]:
    subprocess.run([
        "python3", str(SCRIPT), "--project-root", str(ROOT),
        "--output-dir", str(out), "--version", version,
    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return out / "ea-stodjare-1.2.3.zip", out / "ea-stodjare-1.2.3.release.json"


def test_release_zip_is_deterministic_and_clean():
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        zip_a, meta_a = run_package(Path(a))
        zip_b, meta_b = run_package(Path(b))
        assert digest(zip_a) == digest(zip_b)
        assert json.loads(meta_a.read_text(encoding="utf-8"))["archive_sha256"] == digest(zip_a)
        assert json.loads(meta_b.read_text(encoding="utf-8"))["archive_sha256"] == digest(zip_b)
        with zipfile.ZipFile(zip_a) as zf:
            names = zf.namelist()
            assert names == sorted(names)
            assert all("/.pytest_cache/" not in n for n in names)
            assert all("/__pycache__/" not in n for n in names)
            assert all(not n.endswith(".pyc") for n in names)
            assert all(n.startswith("ea-stodjare-1.2.3/") for n in names)
            assert any(n.endswith("/custom-gpt/instructions.md") for n in names)
            assert any(n.endswith("/.github/workflows/ci.yml") for n in names)


def test_release_version_requires_semver():
    proc = subprocess.run([
        "python3", str(SCRIPT), "--project-root", str(ROOT),
        "--output-dir", tempfile.mkdtemp(), "--version", "release-next",
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert proc.returncode != 0
