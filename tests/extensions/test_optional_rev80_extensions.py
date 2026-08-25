from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from resolve_project_metamodel import resolve


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def extension_validator():
    schema = json.loads((ROOT / "schemas/project-extension.schema.json").read_text(encoding="utf-8"))
    pm_schema = json.loads((ROOT / "schemas/project-metamodel.schema.json").read_text(encoding="utf-8"))
    resource = Resource.from_contents(pm_schema)
    registry = Registry().with_resources([
        ("project-metamodel.schema.json", resource),
        ("https://example.invalid/ea-stodjare/project-metamodel.schema.json", resource),
    ])
    return Draft202012Validator(schema, registry=registry)


def test_all_optional_packages_validate():
    validator = extension_validator()
    for rel in [
        "extensions/product-deployment/extension.yaml",
        "extensions/product-openness/extension.yaml",
        "extensions/platform-maturity/extension.yaml",
    ]:
        errors = list(validator.iter_errors(load_yaml(ROOT / rel)))
        assert not errors, f"{rel}: " + "\n".join(e.message for e in errors)


def test_rev80_vocabularies_are_preserved():
    dep = load_yaml(ROOT / "extensions/product-deployment/extension.yaml")["extension"]["contributions"]
    value_sets = {x["id"]: x["values"] for x in dep["value_sets"]}
    assert value_sets["product_deployment.control_plane_location"] == [
        "customer_on_premises", "customer_private_cloud", "vendor_cloud", "vendor_edge_cloud",
        "mixed_or_configurable", "not_applicable", "unknown"
    ]
    assert "customer_edge" in value_sets["product_deployment.data_plane_location"]
    assert "hybrid_vendor_control_plane" in value_sets["product_deployment.deployment_posture"]

    openness = load_yaml(ROOT / "extensions/product-openness/extension.yaml")["extension"]["contributions"]
    assert openness["value_sets"][0]["values"] == ["open_source", "open_core", "source_available", "proprietary", "unknown"]

    maturity = load_yaml(ROOT / "extensions/platform-maturity/extension.yaml")["extension"]["contributions"]
    assert maturity["value_sets"][0]["values"] == [
        "cohesive_platform", "composite_platform", "specialized_platform", "conditional_platform", "boundary_watch"
    ]


def test_extensions_are_independent_and_optional():
    reg = load_yaml(ROOT / "extensions/registry.yaml")["extensions"]
    rows = {x["id"]: x for x in reg}
    for ext_id in ["ea.product-deployment", "ea.product-openness", "ea.platform-maturity"]:
        assert rows[ext_id]["status"] == "optional"
        package = load_yaml(ROOT / rows[ext_id]["path"])["extension"]
        assert package["requires"] == []
        assert package["conflicts_with"] == []


def test_combined_demo_resolves_all_three_extensions():
    resolved = resolve(ROOT / "examples/extensions/rev80-optional-extensions.yaml", ROOT)
    pm = resolved["project_metamodel"]
    attrs = {}
    for ext in pm["attribute_extensions"]:
        attrs.setdefault(ext["object_type"], set()).update(a["name"] for a in ext["attributes"])
    assert {"control_plane_location", "data_plane_location", "deployment_posture", "openness"}.issubset(attrs["product"])
    assert "maturity_class" in attrs["platform"]
    ids = {x["id"] for x in pm["value_sets"]}
    assert {
        "product_deployment.control_plane_location",
        "product_deployment.data_plane_location",
        "product_deployment.deployment_posture",
        "product_openness.openness",
        "platform_maturity.maturity_class",
    }.issubset(ids)
    assert {x["id"] for x in resolved["resolved_extensions"]} == {
        "ea.product-deployment", "ea.product-openness", "ea.platform-maturity"
    }
    assert resolved["source_of_truth"] is False


def test_reference_reconstruction_marks_these_as_extension_candidates_not_core():
    rev80 = load_yaml(ROOT / "compatibility/reference-projects/rev80/metamodel.yaml")
    ext = rev80["project_extensions"]
    assert ext["product_deployment"]["active"] is True
    assert ext["product_openness"]["active"] is True
    assert ext["platform_maturity"]["active"] is True
    assert "Deployment, openness och platform maturity lämpar sig som optional extensions." in rev80["migration_notes_for_future_steps"]
