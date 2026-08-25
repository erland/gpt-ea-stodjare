from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from resolve_project_metamodel import ExtensionResolutionError, resolve


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, data):
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def test_example_extension_validates_against_extension_schema():
    schema = json.loads((ROOT / "schemas/project-extension.schema.json").read_text(encoding="utf-8"))
    pm_schema = json.loads((ROOT / "schemas/project-metamodel.schema.json").read_text(encoding="utf-8"))
    resource = Resource.from_contents(pm_schema)
    registry = Registry().with_resources([
        ("project-metamodel.schema.json", resource),
        ("https://example.invalid/ea-stodjare/project-metamodel.schema.json", resource),
    ])
    validator = Draft202012Validator(schema, registry=registry)
    data = load_yaml(ROOT / "extensions/example-ownership/extension.yaml")
    errors = list(validator.iter_errors(data))
    assert not errors, "\n".join(e.message for e in errors)


def test_resolver_merges_object_relation_enum_qa_and_presentation():
    resolved = resolve(ROOT / "examples/extensions/project-metamodel.yaml", ROOT)
    pm = resolved["project_metamodel"]
    assert "ownership_domain" in {x["type"] for x in pm["object_types"]["custom"]}
    assert "stewarded_by" in {x["type"] for x in pm["relations"]["custom"]}
    roles = next(x for x in pm["value_sets"] if x["id"] == "realization_role")
    assert "integrated" in roles["values"]
    assert resolved["extension_qa_rules"][0]["id"] == "EXT-OWN-001"
    assert pm["presentation"]["labels"]["stewarded_by"] == "Förvaltas inom"
    assert resolved["source_of_truth"] is False


def test_disabled_extension_has_no_effect(tmp_path: Path):
    data = load_yaml(ROOT / "examples/extensions/project-metamodel.yaml")
    data["project_metamodel"]["extensions"][0]["enabled"] = False
    path = tmp_path / "project-metamodel.yaml"
    write_yaml(path, data)
    resolved = resolve(path, ROOT)
    assert resolved["resolved_extensions"] == []
    assert resolved["extension_qa_rules"] == []
    assert "ownership_domain" not in {x["type"] for x in resolved["project_metamodel"]["object_types"]["custom"]}


def test_unknown_active_extension_fails(tmp_path: Path):
    data = load_yaml(ROOT / "examples/extensions/project-metamodel.yaml")
    data["project_metamodel"]["extensions"][0]["id"] = "missing.extension"
    path = tmp_path / "project-metamodel.yaml"
    write_yaml(path, data)
    with pytest.raises(ExtensionResolutionError, match="saknas i registret"):
        resolve(path, ROOT)


def test_core_object_collision_is_rejected(tmp_path: Path):
    repo = tmp_path / "repo"
    import shutil
    shutil.copytree(ROOT, repo)
    ext_path = repo / "extensions/example-ownership/extension.yaml"
    ext = load_yaml(ext_path)
    ext["extension"]["contributions"]["object_types"][0]["type"] = "platform"
    write_yaml(ext_path, ext)
    with pytest.raises(ExtensionResolutionError, match="Objekttypskollision"):
        resolve(repo / "examples/extensions/project-metamodel.yaml", repo)


def test_duplicate_enum_value_is_rejected(tmp_path: Path):
    repo = tmp_path / "repo"
    import shutil
    shutil.copytree(ROOT, repo)
    ext_path = repo / "extensions/example-ownership/extension.yaml"
    ext = load_yaml(ext_path)
    ext["extension"]["contributions"]["value_set_extensions"][0]["add_values"] = ["primary"]
    write_yaml(ext_path, ext)
    with pytest.raises(ExtensionResolutionError, match="återdefiniera värden"):
        resolve(repo / "examples/extensions/project-metamodel.yaml", repo)


def test_missing_dependency_is_rejected(tmp_path: Path):
    repo = tmp_path / "repo"
    import shutil
    shutil.copytree(ROOT, repo)
    ext_path = repo / "extensions/example-ownership/extension.yaml"
    ext = load_yaml(ext_path)
    ext["extension"]["requires"] = ["missing.base-extension"]
    write_yaml(ext_path, ext)
    with pytest.raises(ExtensionResolutionError, match="saknar beroenden"):
        resolve(repo / "examples/extensions/project-metamodel.yaml", repo)
