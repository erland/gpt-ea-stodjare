from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from detect_project_profile import detect  # noqa: E402


def write_v1_manifest(root: Path, *, revision: int = 1, project_id: str = "legacy-project") -> None:
    manifest = {
        "format": "ea-stodjare-project",
        "format_version": "1.0",
        "project": {
            "id": project_id,
            "name": "Fixture",
            "kind": "ea_model",
            "language": "sv-SE",
            "revision": revision,
            "created_at": "2026-08-25T00:00:00+02:00",
            "updated_at": "2026-08-25T00:00:00+02:00",
            "lifecycle_status": "draft",
        },
        "model": {
            "root": "model",
            "serialization": "YAML",
            "model_format_version": "1.0",
            "metamodel_version": "1.0",
            "relation_model_version": "1.0",
            "provenance_model_version": "1.0",
        },
        "integrity": {"algorithm": "sha256", "manifest_self_hash": False},
        "files": [],
    }
    (root / "project-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def test_native_v2_explicit_wins(tmp_path: Path) -> None:
    shutil.copy(ROOT / "examples/project-metamodel/minimal.yaml", tmp_path / "project-metamodel.yaml")
    write_v1_manifest(tmp_path)
    out = detect(tmp_path, ROOT)
    assert out["classification"] == "native_v2"
    assert out["confidence"] == "high"
    assert out["selected_profile"] == "ea-stodjare-v2"


def test_invalid_explicit_model_blocks_fallback(tmp_path: Path) -> None:
    (tmp_path / "project-metamodel.yaml").write_text("schema_version: '2.0'\nproject_metamodel: {}\n", encoding="utf-8")
    write_v1_manifest(tmp_path)
    out = detect(tmp_path, ROOT)
    assert out["classification"] == "invalid_explicit_model"
    assert out["blockers"]


def test_explicit_legacy_marker(tmp_path: Path) -> None:
    marker = {"compatibility": {"profile": "ea-stodjare-v1", "mode": "legacy"}}
    (tmp_path / "project-compatibility.yaml").write_text(yaml.safe_dump(marker, sort_keys=False), encoding="utf-8")
    out = detect(tmp_path, ROOT)
    assert out["classification"] == "legacy_v1"
    assert out["selected_profile"] == "ea-stodjare-v1"


def test_v1_manifest_detection(tmp_path: Path) -> None:
    write_v1_manifest(tmp_path)
    out = detect(tmp_path, ROOT)
    assert out["classification"] == "legacy_v1"
    assert out["confidence"] == "high"


def test_generic_extended_legacy_detection(tmp_path: Path) -> None:
    write_v1_manifest(tmp_path)
    p = tmp_path / "supporting/market-product-catalog.yaml"
    p.parent.mkdir(parents=True)
    p.write_text("products: []\n", encoding="utf-8")
    out = detect(tmp_path, ROOT)
    assert out["classification"] == "extended_legacy"
    assert out["confidence"] == "medium"


def test_known_rev80_signature(tmp_path: Path) -> None:
    root = tmp_path / "it-formagemodell-del3-rev80"
    root.mkdir()
    write_v1_manifest(root, revision=80, project_id="it-formagemodell-del3-rev80")
    meta = yaml.safe_load((ROOT / "compatibility/reference-projects/rev80/metamodel.yaml").read_text(encoding="utf-8"))
    for rel in meta["detection_signature"]["required_paths"]:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("fixture: true\n", encoding="utf-8")
    out = detect(root, ROOT)
    assert out["classification"] == "extended_legacy"
    assert out["confidence"] == "high"
    assert "rev80-reconstruction" in out["selected_profile"]


def test_unknown_does_not_default_to_v2(tmp_path: Path) -> None:
    (tmp_path / "notes.md").write_text("okänt projekt", encoding="utf-8")
    out = detect(tmp_path, ROOT)
    assert out["classification"] == "unknown"
    assert out["selected_profile"] is None
