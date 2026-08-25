from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def test_can_realize_schema():
    d = yaml.safe_load((ROOT / "schemas/relations.yaml").read_text())
    r = d["relation_types"]["can_realize"]
    assert r["allowed"] == [{"source": "product", "targets": ["it_support", "platform_service"]}]
    q = r["qualifiers"]["realization_role"]
    assert q["required"] is True
    assert set(q["allowed_values"]) == {"primary", "partial", "supporting"}
    assert q["extensible_by_project"] is True

def test_can_realize_not_actual_use():
    d = yaml.safe_load((ROOT / "schemas/relations.yaml").read_text())
    rules = d["relation_types"]["can_realize"]["evidence_rules"]
    assert "does_not_imply_actual_organizational_use_or_selection" in rules
    assert "proposed_only_provenance_is_not_sufficient" in rules

def test_legacy_relations_snapshot_has_no_can_realize():
    d = yaml.safe_load((ROOT / "compatibility/ea-stodjare-v1/schemas/relations.yaml").read_text())
    assert "can_realize" not in d["relation_types"]
