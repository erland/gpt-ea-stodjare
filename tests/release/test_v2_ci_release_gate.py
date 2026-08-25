from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "scripts" / "run_v2_ci_gate.py"

REQUIRED_COVERAGE = {
    "standard_project",
    "legacy_v1_fixture",
    "extended_legacy_fixture",
    "migration",
    "builder_knowledge",
    "eval_definitions",
    "generators",
    "gpt_distributions",
    "release_unpack_and_validate",
    "full_end_to_end_regression",
}


def test_v2_gate_declares_all_plan_step_30_coverage():
    text = GATE.read_text(encoding="utf-8")
    for name in REQUIRED_COVERAGE:
        assert f'"{name}"' in text
    assert "--full-pytest" in text
    assert "package_release.py" in text
    assert "validate_distributions.py" in text
    assert "run_full_e2e_regression.py" in text


def test_workflows_use_central_gate_and_release_is_blocking():
    ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    dist = (ROOT / ".github/workflows/build-distributions.yml").read_text(encoding="utf-8")
    artifacts = (ROOT / ".github/workflows/build-artifacts.yml").read_text(encoding="utf-8")
    assert "run_v2_ci_gate.py" in ci and "--full-pytest" in ci
    assert "run_v2_ci_gate.py" in release and "--mode release" in release and "--full-pytest" in release
    assert release.index("run_v2_ci_gate.py") < release.index("package_release.py") < release.index("gh release create")
    assert "v2-release-gate.json" in release
    assert "run_v2_ci_gate.py" in dist
    assert "run_v2_ci_gate.py" in artifacts


def test_release_packager_has_structural_preflight_metadata():
    source = (ROOT / "scripts/package_release.py").read_text(encoding="utf-8")
    assert "validate_project.py" in source
    assert "structural_preflight" in source
    assert "project_revision" in source


def test_gate_help_is_runnable():
    proc = subprocess.run(["python3", str(GATE), "--help"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.returncode == 0
    assert "--mode" in proc.stdout
    assert "--report-file" in proc.stdout
