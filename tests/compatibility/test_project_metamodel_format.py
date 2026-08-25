from pathlib import Path
import json
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "schemas/project-metamodel.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_examples_validate_against_schema():
    for name in ("minimal.yaml", "extended.yaml"):
        data = load_yaml(ROOT / "examples/project-metamodel" / name)
        errors = sorted(VALIDATOR.iter_errors(data), key=lambda e: list(e.path))
        assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors)


def test_minimal_can_disable_unused_standard_types():
    data = load_yaml(ROOT / "examples/project-metamodel/minimal.yaml")["project_metamodel"]
    assert "capability" in data["object_types"]["enabled"]
    assert "driver" in data["object_types"]["disabled"]
    assert data["object_types"]["custom"] == []


def test_extended_supports_custom_and_derived_view_without_making_view_canonical():
    data = load_yaml(ROOT / "examples/project-metamodel/extended.yaml")["project_metamodel"]
    assert any(x["type"] == "organization_unit" for x in data["object_types"]["custom"])
    assert any(x["type"] == "owned_by" for x in data["relations"]["custom"])
    assert all(view["source_of_truth"] is False for view in data["derived_views"])
    assert "product-deployment" in {x["id"] for x in data["extensions"] if x["enabled"]}


def test_no_overlap_in_enabled_and_disabled_examples():
    for name in ("minimal.yaml", "extended.yaml"):
        data = load_yaml(ROOT / "examples/project-metamodel" / name)["project_metamodel"]
        enabled = set(data["object_types"]["enabled"])
        disabled = set(data["object_types"]["disabled"])
        assert not enabled.intersection(disabled)
        enabled_rel = set(data["relations"]["enabled"])
        disabled_rel = set(data["relations"]["disabled"])
        assert not enabled_rel.intersection(disabled_rel)
