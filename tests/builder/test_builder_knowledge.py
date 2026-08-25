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

        instructions = (ROOT / "custom-gpt" / "instructions.md").read_text(encoding="utf-8")
        assert len(instructions) <= 8000, len(instructions)
        for required in [
            "Projektmetamodell först",
            "legacy v1",
            "extended legacy",
            "conceptual (`model/`)",
            "Produkt",
            "Boundary-first modeling",
            "Derived views",
            "Migration och change-control",
        ]:
            assert required in instructions, required

        domain = (out1 / "01-domain-model.md").read_text(encoding="utf-8")
        workflows = (out1 / "03-analysis-and-modeling-workflows.md").read_text(encoding="utf-8")
        quality = (out1 / "04-quality-assurance.md").read_text(encoding="utf-8")
        project = (out1 / "05-project-and-output.md").read_text(encoding="utf-8")
        assert "docs/v2-design-principles.md" in domain
        assert "docs/information-layers.md" in domain
        assert "knowledge/workflow-project-open.md" in workflows
        assert "knowledge/workflow-boundary-first.md" in workflows
        assert "docs/v1-to-v2-migration-engine.md" in workflows
        assert "knowledge/quality-metamodel-aware.md" in quality
        assert "knowledge/change-control.md" in quality
        assert "docs/backward-compatibility-contract.md" in project
        assert "docs/project-metamodel-format.md" in project
        assert "docs/derived-views.md" in project
        assert "docs/presentation-contract.md" in project
    print("OK: Builder Knowledge är komplett och deterministiskt.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
