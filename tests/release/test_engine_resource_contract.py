"""Contract tests for the *portable* EA Engine ZIP and integration preflight."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "gpt-project.yaml"

RUNTIME_RESOURCES = (
    "schemas",
    "extensions",
    "compatibility",
    "presentation",
    "derived-views",
    "templates/markdown",
    "examples/minimal-model",
)

def test_engine_ships_reference_data_not_just_scripts():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    engine = cfg["engine"]
    assert engine["enabled"] is True
    assert all(item in engine["resources"] for item in RUNTIME_RESOURCES)
    assert all((ROOT / path).exists() for path in engine["resources"])
    for path in (
        "schemas/project-metamodel.schema.json",
        "schemas/project-manifest.schema.json",
        "schemas/object-quality-rules.yaml",
        "presentation/presentation-contract.yaml",
        "extensions/registry.yaml",
        "compatibility/ea-stodjare-v1/profile.yaml",
        "derived-views/views.yaml",
        "examples/minimal-model/project-manifest.json",
    ):
        assert path in engine["required_files"]


def test_engine_selftest_runs_real_workflows():
    source = (ROOT / "scripts/selftest_ea_engine.py").read_text(encoding="utf-8")
    assert "TemporaryDirectory" in source
    assert "validate_project.py" in source
    assert "detect_project_profile.py" in source
    assert "resolve_quality_rules.py" in source
    assert "generate_markdown.py" in source
    assert "generate_confluence.py" in source
    assert "generate_derived_views.py" in source
    assert "migrate_v1_to_v2.py" in source
    assert "determinism_" in source
    assert "document_export" in source
    assert "BLOCKED" in source
