#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "build_builder_knowledge.py"
EXPECTED = {
    "00-knowledge-index.md",
    "01-domain-model.md",
    "02-evidence-and-research.md",
    "03-analysis-and-modeling-workflows.md",
    "04-quality-assurance.md",
    "05-project-and-output.md",
}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(out: Path) -> None:
    subprocess.run([
        "python", str(SCRIPT), "--root", str(ROOT), "--output", str(out)
    ], check=True, cwd=ROOT)

def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        out1 = base / "a"
        out2 = base / "b"
        run(out1)
        run(out2)
        assert {p.name for p in out1.iterdir()} == EXPECTED
        assert {p.name for p in out2.iterdir()} == EXPECTED
        for name in EXPECTED:
            assert digest(out1 / name) == digest(out2 / name), name
        index = (out1 / "00-knowledge-index.md").read_text(encoding="utf-8")
        assert "Builder-instruktionen" in index
        assert "genererade distributionsartefakter" in index
    print("OK: Builder Knowledge är komplett och deterministiskt.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
