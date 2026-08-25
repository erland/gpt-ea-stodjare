#!/usr/bin/env python3
"""Run the mandatory EA Stödjare v2 CI/release validation gate.

The gate makes the release contract explicit and machine-readable. It verifies:
- native v2/reference project validation,
- frozen v1 legacy fixture,
- extended-legacy/rev80 reconstruction and migration contract,
- v1->v2 migration,
- semantic eval definitions,
- Builder Knowledge reproducibility,
- metamodel/presentation-aware generators,
- GPT distributions,
- deterministic release package unpack-and-validate.

Use --full-pytest in CI/release to add the complete pytest suite after the focused gates.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Any


def run_step(name: str, command: list[str], root: Path, env: dict[str, str] | None = None) -> dict[str, Any]:
    started = time.monotonic()
    proc = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, **(env or {})},
        check=False,
    )
    result: dict[str, Any] = {
        "name": name,
        "status": "passed" if proc.returncode == 0 else "failed",
        "returncode": proc.returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "command": command,
    }
    if proc.stdout.strip():
        result["stdout_tail"] = proc.stdout.strip().splitlines()[-20:]
    if proc.stderr.strip():
        result["stderr_tail"] = proc.stderr.strip().splitlines()[-20:]
    return result


def write_report(path: Path | None, report: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_version(raw: str) -> str:
    return raw[1:] if raw.startswith("v") else raw


def main() -> int:
    ap = argparse.ArgumentParser(description="Kör obligatorisk EA Stödjare v2 CI/release-grind.")
    ap.add_argument("--project-root", type=Path, default=Path.cwd())
    ap.add_argument("--mode", choices=["ci", "release"], default="ci")
    ap.add_argument("--version", help="Release/distributionsversion. Default: VERSION-filen.")
    ap.add_argument("--report-file", type=Path)
    ap.add_argument("--full-pytest", action="store_true", help="Kör hela pytest-sviten som extra regressionsgrind.")
    args = ap.parse_args()

    root = args.project_root.resolve()
    version = normalize_version(args.version or (root / "VERSION").read_text(encoding="utf-8").strip())
    report_path = args.report_file
    if report_path is not None and not report_path.is_absolute():
        report_path = root / report_path

    report: dict[str, Any] = {
        "schema_version": "1.0",
        "gate": "ea-stodjare-v2",
        "mode": args.mode,
        "version": version,
        "project_root": str(root),
        "required_coverage": [
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
            "release_contract",
        ],
        "steps": [],
        "valid": False,
    }

    def step(name: str, cmd: list[str], env: dict[str, str] | None = None) -> bool:
        result = run_step(name, cmd, root, env)
        report["steps"].append(result)
        write_report(report_path, report)
        if result["status"] == "failed":
            report["failed_step"] = name
            return False
        return True

    py = sys.executable
    focused_steps: list[tuple[str, list[str]]] = [
        ("standard_project", [py, "scripts/validate_project.py", "--project-root", ".", "--report-file", "build/validation-report.json"]),
        ("legacy_v1_fixture", [py, "scripts/validate_project.py", "--project-root", "examples/minimal-model", "--no-generated"]),
        ("extended_legacy_fixture", [py, "-m", "pytest", "-q", "tests/compatibility/test_rev80_reconstruction.py", "tests/compatibility/test_rev80_migration_step24.py"]),
        ("migration", [py, "-m", "pytest", "-q", "tests/compatibility/test_v1_to_v2_migration_engine.py"]),
        ("eval_definitions", [py, "tests/evals/test_eval_suite.py"]),
        ("builder_knowledge", [py, "tests/builder/test_builder_knowledge.py"]),
        ("generators", [py, "scripts/run_generation_smoke.py"]),
        ("full_end_to_end_regression", [py, "scripts/run_full_e2e_regression.py", "--project-root", ".", "--report-file", "build/full-e2e-report.json"]),
        ("release_contract", [py, "-m", "pytest", "-q", "tests/release/test_release_contract.py"]),
    ]
    for name, cmd in focused_steps:
        if not step(name, cmd):
            report["valid"] = False
            write_report(report_path, report)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 1

    # Build and validate both end-user GPT distribution formats.
    if not step("build_gpt_distributions", [py, "scripts/build_distributions.py", "--version", version]):
        write_report(report_path, report); print(json.dumps(report, ensure_ascii=False, indent=2)); return 1
    if not step("gpt_distributions", [py, "scripts/validate_distributions.py", "--version", version]):
        write_report(report_path, report); print(json.dumps(report, ensure_ascii=False, indent=2)); return 1

    # Release package is always smoke-tested in CI as well as on tag releases.
    # Keep the temporary release-gate directory until process exit. Some document
    # toolchains may leave transient lock files; cleanup is not part of validation.
    out = Path(tempfile.mkdtemp(prefix="ea-stodjare-release-gate-"))
    if not step("release_package_build", [py, "scripts/package_release.py", "--project-root", ".", "--output-dir", str(out), "--version", version]):
        write_report(report_path, report); print(json.dumps(report, ensure_ascii=False, indent=2)); return 1
    archive = out / f"ea-stodjare-{version}.zip"
    unpack = out / "unpacked"
    try:
        with zipfile.ZipFile(archive) as zf:
            bad = zf.testzip()
            if bad:
                raise RuntimeError(f"Korrupt releasezip: {bad}")
            zf.extractall(unpack)
    except Exception as exc:
        report["steps"].append({"name": "release_unpack", "status": "failed", "returncode": 1, "error": str(exc)})
        report["failed_step"] = "release_unpack"
        write_report(report_path, report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1
    report["steps"].append({"name": "release_unpack", "status": "passed", "returncode": 0})
    released_root = unpack / f"ea-stodjare-{version}"
    if not step("release_unpack_and_validate", [py, str(released_root / "scripts" / "validate_project.py"), "--project-root", str(released_root), "--repo-root", str(released_root), "--no-generated"]):
        write_report(report_path, report); print(json.dumps(report, ensure_ascii=False, indent=2)); return 1

    if args.full_pytest:
        if not step("full_pytest", [py, "-m", "pytest", "-q"]):
            write_report(report_path, report); print(json.dumps(report, ensure_ascii=False, indent=2)); return 1

    report["valid"] = True
    report["summary"] = {
        "passed": sum(1 for x in report["steps"] if x.get("status") == "passed"),
        "failed": sum(1 for x in report["steps"] if x.get("status") == "failed"),
    }
    write_report(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
