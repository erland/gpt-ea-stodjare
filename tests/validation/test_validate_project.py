#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_project.py"
EXAMPLE = ROOT / "examples" / "minimal-model"


def run(project: Path, generated: bool = False) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, str(VALIDATOR), "--project-root", str(project), "--repo-root", str(ROOT), "--json"]
    if not generated:
        cmd.append("--no-generated")
    return subprocess.run(cmd, text=True, capture_output=True)


def clone_example() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    td = tempfile.TemporaryDirectory(prefix="ea-validator-test-")
    dst = Path(td.name) / "project"
    shutil.copytree(EXAMPLE, dst)
    return td, dst


def update_manifest_hash(project: Path, rel: str) -> None:
    import hashlib
    manifest_path = project / "project-manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    h = hashlib.sha256((project / rel).read_bytes()).hexdigest()
    for item in data["files"]:
        if item["path"] == rel:
            item["sha256"] = h
            break
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assert_code(result: subprocess.CompletedProcess[str], code: str) -> None:
    payload = json.loads(result.stdout)
    codes = {x["code"] for x in payload["errors"] + payload["warnings"]}
    assert code in codes, (code, result.stdout, result.stderr)


def test_valid_reference_project() -> None:
    result = run(ROOT, generated=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_valid_minimal_model_with_generated_outputs() -> None:
    result = run(EXAMPLE, generated=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_duplicate_id_is_rejected() -> None:
    td, p = clone_example()
    try:
        path = p / "model/goals.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["objects"][0]["id"] = "DRV-001"
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        update_manifest_hash(p, "model/goals.yaml")
        result = run(p)
        assert result.returncode != 0
        assert_code(result, "STR-ID-001")
    finally:
        td.cleanup()


def test_missing_relation_target_is_rejected() -> None:
    td, p = clone_example()
    try:
        path = p / "model/relations.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["relations"][0]["target"] = "GOAL-999"
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        update_manifest_hash(p, "model/relations.yaml")
        result = run(p)
        assert result.returncode != 0
        assert_code(result, "STR-REL-008")
    finally:
        td.cleanup()


def test_illegal_relation_combination_is_rejected() -> None:
    td, p = clone_example()
    try:
        path = p / "model/relations.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        data["relations"][0]["source"] = "PLT-001"
        data["relations"][0]["target"] = "GOAL-001"
        path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        update_manifest_hash(p, "model/relations.yaml")
        result = run(p)
        assert result.returncode != 0
        assert_code(result, "STR-REL-010")
    finally:
        td.cleanup()


def test_manifest_hash_mismatch_is_rejected() -> None:
    td, p = clone_example()
    try:
        path = p / "model/drivers.yaml"
        path.write_text(path.read_text(encoding="utf-8") + "\n# ändring utan manifestuppdatering\n", encoding="utf-8")
        result = run(p)
        assert result.returncode != 0
        assert_code(result, "STR-MAN-009")
    finally:
        td.cleanup()


def test_stale_markdown_is_rejected() -> None:
    td, p = clone_example()
    try:
        path = p / "docs/generated/formagor.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nMANUELL DRIFT\n", encoding="utf-8")
        update_manifest_hash(p, "docs/generated/formagor.md")
        result = run(p, generated=True)
        assert result.returncode != 0
        assert_code(result, "STR-GEN-001")
    finally:
        td.cleanup()


def main() -> int:
    tests = [name for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for name in sorted(tests):
        globals()[name]()
        print(f"OK {name}")
    print(f"OK {len(tests)} validation tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
