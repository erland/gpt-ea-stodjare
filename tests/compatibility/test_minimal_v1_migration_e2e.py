import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "examples/minimal-model"
MIGRATE = ROOT / "scripts/migrate_v1_to_v2.py"
VERIFY = ROOT / "scripts/verify_v1_v2_migration.py"
BASELINE = ROOT / "compatibility/reference-projects/minimal-v1-migration/verification-baseline.yaml"


def load_yaml(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_minimal_baseline_matches_source():
    baseline = load_yaml(BASELINE)["expected"]
    objects = []
    for p in (SRC / "model").glob("*.yaml"):
        data = load_yaml(p) or {}
        objects.extend(x for x in (data.get("objects") or []) if isinstance(x, dict) and x.get("id"))
    rels = (load_yaml(SRC / "model/relations.yaml") or {}).get("relations", [])
    sources = (load_yaml(SRC / "model/sources.yaml") or {}).get("sources", [])
    assert len(objects) == baseline["object_count"] == 11
    assert len(rels) == baseline["relation_count"] == 12
    assert len(sources) == baseline["source_count"] == 3
    assert {x["id"] for x in objects} == set(baseline["object_ids"])
    assert {x["id"] for x in rels} == set(baseline["relation_ids"])
    assert {x["id"] for x in sources} == set(baseline["source_ids"])


def test_minimal_v1_to_v2_end_to_end_semantic_equivalence():
    before_manifest = (SRC / "project-manifest.json").read_bytes()
    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "migrated"
        subprocess.run([sys.executable, str(MIGRATE), "--source", str(SRC), "--mode", "apply", "--output", str(target)], check=True, capture_output=True, text=True)
        result = subprocess.run([sys.executable, str(VERIFY), "--source", str(SRC), "--target", str(target)], check=True, capture_output=True, text=True)
        report = yaml.safe_load(result.stdout)["verification"]
        assert report["passed"] is True
        assert all(report["checks"].values())
        assert report["objects"] == 11 and report["relations"] == 12 and report["sources"] == 3
        assert report["target_revision"] == report["source_revision"] + 1
        manifest = json.loads((target / "project-manifest.json").read_text(encoding="utf-8"))
        assert manifest["model"]["metamodel_version"] == "2.0"
        rels = load_yaml(target / "model/relations.yaml")["relations"]
        assert next(r for r in rels if r["id"] == "REL-006")["type"] == "legacy_realized_by"
        assert next(r for r in rels if r["id"] == "REL-011")["type"] == "realized_by"
    assert (SRC / "project-manifest.json").read_bytes() == before_manifest
