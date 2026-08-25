from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCENARIO = ROOT / "examples" / "product-analysis-it-support"
sys.path.insert(0, str(ROOT / "scripts"))
from validate_project import ValidationContext, validate_model, validate_information_layers


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_scenario_is_structurally_valid_native_v2_model():
    manifest = {
        "model": {"root": "model", "metamodel_version": "2.0"},
        "information_layers": {
            "conceptual": "model",
            "market_reference": "market-reference",
            "actual_state": "actual-state",
        },
    }
    ctx = ValidationContext()
    validate_model(SCENARIO, ROOT, manifest, ctx)
    validate_information_layers(SCENARIO, ROOT, manifest, ctx)
    assert not ctx.errors, "\n".join(x.format() for x in ctx.errors)


def test_it_support_is_product_neutral_and_uses_embedded_functions():
    its = load_yaml(SCENARIO / "model" / "it-support.yaml")["objects"][0]
    assert its["id"] == "ITS-251"
    assert "product" not in its
    functions = {f["id"]: f for f in its["functions"]}
    assert set(functions) == {"create_document", "edit_format", "spelling_language", "collaborate"}
    assert {fid for fid, f in functions.items() if f.get("required")} == {
        "create_document", "edit_format", "spelling_language"
    }


def test_multiple_products_cover_primary_partial_and_supporting_roles():
    rels = load_yaml(SCENARIO / "model" / "relations.yaml")["relations"]
    can = {r["source"]: r for r in rels if r["type"] == "can_realize"}
    assert {p: r["realization_role"] for p, r in can.items()} == {
        "PRD-251": "primary",
        "PRD-252": "partial",
        "PRD-253": "supporting",
    }
    assert all(r["target"] == "ITS-251" for r in can.values())
    assert all(r["provenance"][0]["evidence_type"] == "external" for r in can.values())


def test_market_evidence_and_actual_usage_are_separate_layers():
    market = load_yaml(SCENARIO / "market-reference" / "assertions.yaml")["assertions"]
    actual = load_yaml(SCENARIO / "actual-state" / "assertions.yaml")["assertions"]
    assert {a["subject"] for a in market} == {"PRD-251", "PRD-252", "PRD-253"}
    assert {a["subject"] for a in actual if a["assertion_type"] == "product_in_use"} == {"PRD-252"}
    assert actual[0]["provenance"][0]["evidence_type"] == "explicit"
    assert actual[0]["provenance"][0]["source_id"] == "SRC-252"


def test_expected_analysis_explicitly_blocks_actual_use_inference():
    expected = load_yaml(SCENARIO / "expected-analysis.yaml")
    assert expected["product_neutral_need"] is True
    assert expected["actual_products_in_use"] == ["PRD-252"]
    assert set(expected["not_actual_by_inference"]) == {"PRD-251", "PRD-253"}
    assert "can_realize_does_not_imply_actual_use" in expected["guards"]
    assert "actual_use_requires_organization_specific_evidence" in expected["guards"]
