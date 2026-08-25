import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_project import ValidationContext, validate_derived_views, validate_project


def test_reference_repository_is_recognized_as_native_v2():
    ctx = validate_project(ROOT, ROOT, check_generated=False)
    assert ctx.profile["classification"] == "native_v2"
    # Integrity may be temporarily red while a revision is being edited; profile selection may not.
    assert not any(f.code.startswith("STR-PROFILE-") for f in ctx.errors)


def test_legacy_v1_uses_frozen_profile():
    ctx = validate_project(ROOT / "examples/minimal-model", ROOT, check_generated=False)
    assert ctx.profile["classification"] == "legacy_v1"
    assert not ctx.errors


def test_unmigrated_rev80_routes_around_modern_manifest_schema():
    sig = yaml.safe_load((ROOT / "compatibility/reference-projects/rev80/metamodel.yaml").read_text(encoding="utf-8"))["detection_signature"]
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "it-formagemodell-del3-rev80"
        p.mkdir()
        (p / "project-manifest.json").write_text(json.dumps({
            "schema_version": "1.0", "revision": 80,
            "root_directory": "it-formagemodell-del3-rev80", "file_count": 245, "files": []
        }), encoding="utf-8")
        # Create only signature files. Their deliberately empty contents should yield rev80-specific
        # count findings, never a modern project-manifest schema finding.
        for rel in sig["required_paths"]:
            f = p / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("{}\n", encoding="utf-8")
        ctx = validate_project(p, ROOT, check_generated=False)
        assert ctx.profile["classification"] == "extended_legacy"
        assert not any(f.code.startswith("STR-MAN-") for f in ctx.errors)
        assert any(f.code.startswith("STR-REV80U-") for f in ctx.errors)


def test_materialized_derived_views_must_be_reproducible():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "project"
        shutil.copytree(ROOT, p, ignore=shutil.ignore_patterns(".pytest_cache", "__pycache__", "build"))
        out = p / "build/derived-views"
        subprocess.run([sys.executable, str(p / "scripts/generate_derived_views.py"), "--project-root", str(p), "--output-dir", str(out)], check=True)
        first = sorted(out.glob("*.yaml"))[0]
        first.write_text(first.read_text(encoding="utf-8") + "tampered: true\n", encoding="utf-8")
        manifest = json.loads((p / "project-manifest.json").read_text(encoding="utf-8"))
        ctx = ValidationContext()
        validate_derived_views(p, p, manifest, ctx)
        assert any(f.code == "STR-VIEW-007" for f in ctx.errors)


def test_validation_report_schema_accepts_cli_report(tmp_path):
    report = tmp_path / "report.json"
    cp = subprocess.run([
        sys.executable, str(ROOT / "scripts/validate_project.py"),
        "--project-root", str(ROOT / "examples/minimal-model"),
        "--repo-root", str(ROOT), "--no-generated", "--report-file", str(report)
    ], check=False)
    assert cp.returncode == 0
    data = json.loads(report.read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/validation-report.schema.json").read_text(encoding="utf-8"))
    assert not list(Draft202012Validator(schema).iter_errors(data))
    assert data["profile"]["classification"] == "legacy_v1"
    assert data["stages"][0]["name"] == "profile_detection"
