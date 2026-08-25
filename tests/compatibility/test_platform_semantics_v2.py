from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
def load(rel): return yaml.safe_load((ROOT/rel).read_text(encoding="utf-8"))

def test_v2_platform_is_conceptual_and_product_neutral():
    d=load("schemas/object-types.yaml"); p=d["object_types"]["platform"]
    txt=(p["definition"]+" "+p["question"]).lower()
    assert "produktneutral" in txt
    assert "konceptuell" in txt
    assert "platform_service" in p["not"]
    assert "product_neutral_boundary" in p["semantic_rules"]
    assert "singleton_platform_can_be_legitimate" in p["semantic_rules"]
    assert "composition_realization_is_legitimate" in p["semantic_rules"]

def test_v1_snapshot_retains_legacy_platform_semantics():
    d=load("compatibility/ea-stodjare-v1/schemas/object-types.yaml")
    p=d["object_types"]["platform"]
    txt=(p["definition"]+" "+p["question"]).lower()
    assert "teknisk grund" in txt or "realiserar" in txt
    assert "product_neutral_boundary" not in p.get("semantic_rules",[])

def test_platform_migration_is_non_destructive_and_relation_change_deferred():
    d=load("compatibility/migration-rules/v1-to-v2-platform-semantics.yaml")["migration_rule_set"]
    assert d["automatic_rewrite_default"] is False
    r={x["id"]:x for x in d["rules"]}
    assert r["PLT-SEM-003"]["action"] == "do not rewrite in step 8"
