from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
def load(rel): return yaml.safe_load((ROOT/rel).read_text(encoding="utf-8"))

def test_v2_platform_service_is_realization_neutral():
    d=load("schemas/object-types.yaml"); ps=d["object_types"]["platform_service"]
    text=(ps["definition"]+" "+ps["question"]).lower()
    assert "utan att låsa hur eller var realiseringen sker" in text
    assert "realization_pattern" in ps["optional_attributes"]
    assert "composition" in ps["allowed_values"]["realization_pattern"]
    assert "saas" in ps["allowed_values"]["realization_pattern"]

def test_v1_snapshot_retains_legacy_semantics():
    d=load("compatibility/ea-stodjare-v1/schemas/object-types.yaml")
    ps=d["object_types"]["platform_service"]
    assert "gemensamt" in ps["definition"].lower() or "gemensam" in ps["question"].lower()
    assert "realization_pattern" not in ps["optional_attributes"]

def test_platform_service_migration_is_non_destructive():
    d=load("compatibility/migration-rules/v1-to-v2-platform-service-semantics.yaml")["migration_rule_set"]
    assert d["automatic_rewrite_default"] is False
    assert any(r["id"]=="PLS-SEM-001" for r in d["rules"])
