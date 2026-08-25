import json, hashlib
from pathlib import Path
import copy, subprocess, tempfile, shutil, yaml

ROOT = Path(__file__).resolve().parents[2]

def load_relations():
    return yaml.safe_load((ROOT / "schemas/relations.yaml").read_text(encoding="utf-8"))

def test_qualifier_catalog_and_applicability():
    data = load_relations()
    q = data["qualifier_definitions"]
    assert set(["relation_role","strength","mandatory","realization_role","verification_status","boundary_basis","notes"]).issubset(q)
    assert data["relation_types"]["can_realize"]["qualifiers"]["realization_role"]["required"] is True
    assert "realization_role" not in data["relation_types"]["related_to"]["qualifiers"]
    assert "relation_role" in data["relation_types"]["related_to"]["qualifiers"]

def test_legacy_snapshot_does_not_gain_v2_qualifiers():
    legacy = yaml.safe_load((ROOT / "compatibility/ea-stodjare-v1/schemas/relations.yaml").read_text(encoding="utf-8"))
    assert "qualifier_definitions" not in legacy
    assert "provided_by" not in legacy["relation_types"]
    assert "can_realize" not in legacy["relation_types"]

def test_validator_rejects_inapplicable_qualifier():
    src = ROOT / "examples/minimal-model"
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / "project"
        subprocess.run(["python3", str(ROOT / "scripts/migrate_v1_to_v2.py"), "--source", str(src), "--mode", "apply", "--output", str(dst)], check=True, capture_output=True, text=True)
        relp = dst / "model/relations.yaml"
        data = yaml.safe_load(relp.read_text(encoding="utf-8"))
        rel = next(r for r in data["relations"] if r["type"] not in {"can_realize", "legacy_realized_by"})
        rel["realization_role"] = "primary"
        relp.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        mp = dst / "project-manifest.json"
        manifest = json.loads(mp.read_text(encoding="utf-8"))
        for row in manifest["files"]:
            if row.get("path") == "model/relations.yaml":
                row["sha256"] = hashlib.sha256(relp.read_bytes()).hexdigest()
        mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        proc = subprocess.run(["python3", str(ROOT / "scripts/validate_project.py"), "--project-root", str(dst), "--repo-root", str(ROOT)], capture_output=True, text=True)
        assert "otillåten kvalificerare: realization_role" in proc.stdout + proc.stderr
