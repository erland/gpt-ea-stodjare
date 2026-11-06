"""Regression tests for isolated runtime scripts and the Engine ZIP contract."""
from __future__ import annotations

import ast
import io
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from check_packaged_skill_dependencies import audit


def test_all_skill_script_dependencies_are_declared() -> None:
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    declared = {x["id"]: x for x in config["skills"]["definitions"]}
    runtime_modules = {x.stem for x in (ROOT / "scripts").glob("*.py")}
    assert len(declared) == 3
    for skill in declared.values():
        names = {Path(p).stem for p in skill["scripts"]}
        for rel in skill["scripts"]:
            script = ROOT / rel
            assert script.is_file(), rel
            source = ast.parse(script.read_text(encoding="utf-8"))
            imports = set()
            for node in ast.walk(source):
                if isinstance(node, ast.Import):
                    imports.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.add(node.module.split(".")[0])
            assert not (imports & runtime_modules) - names, (skill["id"], rel, imports - names)


def test_runtime_engine_resources_are_explicit_and_selftest_exists() -> None:
    config = yaml.safe_load((ROOT / "gpt-project.yaml").read_text(encoding="utf-8"))
    engine = config["engine"]
    assert engine["enabled"] is True
    assert engine["release_repository"] == "erland/gpt-ea-stodjare"
    assert (ROOT / engine["selftest"]).is_file()
    for resource in engine["resources"]:
        target = ROOT / resource
        assert target.exists(), f"Missing Engine resource: {resource}"
        if target.is_dir():
            assert any(p.is_file() for p in target.rglob("*")), (
                f"Empty Engine resource directory: {resource}"
            )
        else:
            assert target.is_file(), f"Invalid Engine resource: {resource}"
    all_skill_scripts = {path for skill in config["skills"]["definitions"]
                         for path in skill["scripts"]}
    assert all_skill_scripts <= set(engine["resources"])


def test_isolated_audit_rejects_missing_transitive_import(tmp_path: Path) -> None:
    zip_path = tmp_path / "bad-plugin.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("skills/quality-and-publication/scripts/validate_project.py",
                    "import resolve_project_metamodel\n")
    checked, errors = audit(zip_path, "skills/", {"resolve_project_metamodel", "validate_project"})
    assert checked == 1
    assert any("missing isolated script dependency" in error for error in errors)
