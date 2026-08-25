from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from validate_project import ValidationContext, validate_information_layers


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_information_layer_schema_has_three_epistemic_layers():
    spec = load_yaml(ROOT / "schemas/information-layers.yaml")
    assert set(spec["layers"]) == {"conceptual", "market_reference", "actual_state"}
    rules = {x["id"]: x["rule"] for x in spec["cross_layer_rules"]}
    assert rules["LAYER-001"] == "conceptual need != product choice"
    assert rules["LAYER-002"] == "market capability != actual use"
    assert rules["LAYER-003"] == "actual use != organizational offering"
    assert "actual_platform_offering" in rules["LAYER-005"]


def test_project_manifest_declares_layer_paths():
    manifest = json.loads((ROOT / "project-manifest.json").read_text(encoding="utf-8"))
    assert manifest["information_layers"] == {
        "conceptual": "model",
        "market_reference": "market-reference",
        "actual_state": "actual-state",
    }


def _fixture(tmp_path: Path) -> tuple[Path, dict]:
    project = tmp_path / "project"
    (project / "model").mkdir(parents=True)
    (project / "market-reference").mkdir()
    (project / "actual-state").mkdir()
    (project / "model/products.yaml").write_text("""schema_version: '1.0'\nobject_type: product\nobjects:\n  - id: PRD-001\n    type: product\n    name: Example\n    description: Example\n    status: active\n    product_kind: application_product\n    provenance:\n      - evidence_type: external\n        source_id: SRC-EXT-001\n""", encoding="utf-8")
    (project / "model/sources.yaml").write_text("""schema_version: '1.0'\nsources:\n  - id: SRC-EXT-001\n    title: Vendor docs\n    source_type: vendor_documentation\n  - id: SRC-001\n    title: Internal register\n    source_type: internal_document\n""", encoding="utf-8")
    (project / "market-reference/assertions.yaml").write_text("schema_version: '1.0'\nlayer: market_reference\nassertions: []\n", encoding="utf-8")
    (project / "actual-state/assertions.yaml").write_text("schema_version: '1.0'\nlayer: actual_state\nassertions: []\n", encoding="utf-8")
    manifest = {"information_layers": {"conceptual": "model", "market_reference": "market-reference", "actual_state": "actual-state"}}
    return project, manifest


def test_actual_state_can_reference_product_directly(tmp_path: Path):
    project, manifest = _fixture(tmp_path)
    (project / "actual-state/assertions.yaml").write_text("""schema_version: '1.0'\nlayer: actual_state\nassertions:\n  - id: ACT-001\n    assertion_type: product_in_use\n    subject: PRD-001\n    statement: Produkten används i organisationen.\n    status: verified\n    provenance:\n      - evidence_type: explicit\n        source_id: SRC-001\n""", encoding="utf-8")
    ctx = ValidationContext()
    validate_information_layers(project, ROOT, manifest, ctx)
    assert not ctx.errors, "\n".join(x.format() for x in ctx.errors)


def test_external_market_evidence_alone_cannot_verify_actual_state(tmp_path: Path):
    project, manifest = _fixture(tmp_path)
    (project / "actual-state/assertions.yaml").write_text("""schema_version: '1.0'\nlayer: actual_state\nassertions:\n  - id: ACT-001\n    assertion_type: product_in_use\n    subject: PRD-001\n    statement: Produkten används i organisationen.\n    status: verified\n    provenance:\n      - evidence_type: external\n        source_id: SRC-EXT-001\n""", encoding="utf-8")
    ctx = ValidationContext()
    validate_information_layers(project, ROOT, manifest, ctx)
    assert any(x.code == "STR-LAYER-023" for x in ctx.errors)


def test_actual_use_and_organizational_offering_are_distinct_assertion_types():
    spec = load_yaml(ROOT / "schemas/information-layers.yaml")
    types = spec["actual_state_assertion"]["assertion_types"]
    assert "product_in_use" in types
    assert "organizational_offering" in types
    assert types.index("product_in_use") != types.index("organizational_offering")
