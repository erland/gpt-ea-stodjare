from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def load(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))

def test_native_v2_uses_provided_by_for_platform_service_home():
    rels = load("schemas/relations.yaml")["relation_types"]
    assert "provided_by" in rels
    allowed = rels["provided_by"]["allowed"]
    assert any(x["source"] == "platform_service" and "platform" in x["targets"] for x in allowed)
    legacy_native = rels["realized_by"]["allowed"]
    assert not any(x["source"] == "platform_service" and "platform" in x["targets"] for x in legacy_native)

def test_v1_snapshot_keeps_legacy_realized_by():
    rels = load("compatibility/ea-stodjare-v1/schemas/relations.yaml")["relation_types"]
    assert "provided_by" not in rels
    assert any(x["source"] == "platform_service" and "platform" in x["targets"] for x in rels["realized_by"]["allowed"])

def test_migration_is_not_automatic():
    rule = load("compatibility/migration-rules/v1-to-v2-provided-by.yaml")["migration_rule"]
    assert rule["automatic"] is False
    assert rule["target_relation"] == "provided_by"
    assert rule["known_reference_cases"]["rev80"]["interpretation"] == "conceptual_home"
