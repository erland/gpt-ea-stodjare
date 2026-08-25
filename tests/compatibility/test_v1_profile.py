from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROFILE_ROOT = ROOT / "compatibility" / "ea-stodjare-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v1_profile_is_self_consistent() -> None:
    profile = yaml.safe_load((PROFILE_ROOT / "profile.yaml").read_text(encoding="utf-8"))
    data = profile["compatibility_profile"]
    assert data["id"] == "ea-stodjare-v1"
    assert data["compatibility_class"] == "legacy_v1"
    assert data["status"] == "frozen_snapshot"
    assert data["immutable_semantics"] is True

    for rel, meta in profile["snapshot_files"].items():
        path = PROFILE_ROOT / rel
        assert path.is_file(), rel
        assert sha256(path) == meta["sha256"], rel


def test_v1_profile_captures_required_legacy_semantics() -> None:
    profile = yaml.safe_load((PROFILE_ROOT / "profile.yaml").read_text(encoding="utf-8"))
    types = yaml.safe_load((PROFILE_ROOT / "schemas/object-types.yaml").read_text(encoding="utf-8"))
    relations = yaml.safe_load((PROFILE_ROOT / "schemas/relations.yaml").read_text(encoding="utf-8"))
    model_format = yaml.safe_load((PROFILE_ROOT / "schemas/model-format.yaml").read_text(encoding="utf-8"))
    provenance = yaml.safe_load((PROFILE_ROOT / "schemas/provenance.yaml").read_text(encoding="utf-8"))
    manifest_schema = json.loads((PROFILE_ROOT / "schemas/project-manifest.schema.json").read_text(encoding="utf-8"))

    assert set(types["object_types"]) == {
        "driver", "goal", "principle", "capability", "it_support",
        "platform_service", "platform", "standard", "solution_pattern", "reference_architecture"
    }
    assert types["object_types"]["capability"]["optional_attributes"] == ["scope", "consumer_scope"]
    assert "product" in types["explicitly_out_of_core_v1"]
    assert model_format["function_instance"]["rules"][0] == "function_has_no_global_id_in_v1"
    assert set(relations["relation_types"]) == {
        "influences", "supports", "uses", "realized_by", "governed_by",
        "constrains", "depends_on", "derived_from", "related_to"
    }
    assert set(provenance["evidence_types"]) == {"explicit", "derived", "proposed", "external"}
    assert manifest_schema["properties"]["format_version"]["const"] == "1.0"

    guards = {g["concept"] for g in profile["legacy_semantic_guards"]}
    assert {"capability.scope", "platform_service", "platform", "realized_by", "product", "function"} <= guards
