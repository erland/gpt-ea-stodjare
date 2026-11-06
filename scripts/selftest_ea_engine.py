#!/usr/bin/env python3
"""Integrity and functional integration self-test of the *unpacked* EA runtime Engine.

Uses only the bundled legacy fixture in a temporary copy. Never changes a user project.
Reports external document toolchain limitations separately from mandatory EA operations.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        h.update(path.relative_to(root).as_posix().encode("utf-8"))
        h.update(b"\\0")
        h.update(digest(path).encode("ascii"))
        h.update(b"\\n")
    return h.hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    stages: list[dict[str, str]] = []
    manifest_path = root / "engine-package.json"
    if not manifest_path.is_file():
        print("ENGINE SELFTEST FAILED: engine-package.json missing", file=sys.stderr)
        return 1
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("engine_id") != "ea-stodjare":
        print("ENGINE SELFTEST FAILED: incorrect engine_id", file=sys.stderr)
        return 1
    if not isinstance(data.get("version"), str) or not data["version"]:
        errors.append("Missing Engine version")
    files = data.get("files") or {}
    required = set(data.get("required_files") or [])
    if not isinstance(files, dict) or not required <= set(files):
        errors.append("Manifest missing declared required files")
    for name, expected in files.items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or "\\\\" in name:
            errors.append(f"Unsafe path: {name}")
            continue
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing: {name}")
        elif digest(path) != expected:
            errors.append(f"SHA-256 mismatch: {name}")
    stages.append({"name": "manifest_and_sha256", "status": "FAIL" if errors else "PASS"})

    scripts = sorted(name for name in files if name.startswith("scripts/") and name.endswith(".py")
                     and name != "scripts/selftest_ea_engine.py")
    if not errors:
        for name in scripts:
            script = root / name
            command = ("import runpy,sys;"
                       "sys.path.insert(0,sys.argv[1]);"
                       "runpy.run_path(sys.argv[2],run_name='__ea_import_probe__')")
            proc = subprocess.run([sys.executable, "-c", command, str(script.parent), str(script)],
                                  cwd=root, text=True, capture_output=True, timeout=30, check=False)
            if proc.returncode:
                errors.append(f"Import probe failed: {name}: {proc.stderr[-600:]}")
        stages.append({"name": "script_imports", "status": "FAIL" if errors else "PASS"})

    def run(label: str, args: list[str], cwd: Path) -> bool:
        try:
            proc = subprocess.run([sys.executable, *args], cwd=cwd, capture_output=True,
                                  text=True, check=False, timeout=90)
            if proc.returncode:
                errors.append(f"{label} failed (exit {proc.returncode}): "
                              f"{(proc.stderr + proc.stdout)[-1000:]}")
                stages.append({"name": label, "status": "FAIL"})
                return False
            stages.append({"name": label, "status": "PASS"})
            return True
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(f"{label} failed: {exc}")
            stages.append({"name": label, "status": "FAIL"})
            return False

    if not errors:
        fixture = root / "examples/minimal-model"
        if not (fixture / "project-manifest.json").is_file():
            errors.append("Bundled integration fixture missing")
        else:
            with tempfile.TemporaryDirectory(prefix="ea-engine-selftest-") as temporary:
                work = Path(temporary)
                sample = work / "sample"
                shutil.copytree(fixture, sample)
                run("detect_project_profile",
                    [str(root / "scripts/detect_project_profile.py"), "--project-root",
                     str(sample), "--repository-root", str(root)], root)
                run("validate_project",
                    [str(root / "scripts/validate_project.py"), "--project-root",
                     str(sample), "--repo-root", str(root), "--no-generated"], root)
                run("resolve_quality_rules",
                    [str(root / "scripts/resolve_quality_rules.py"), "--project-root",
                     str(sample), "--repo-root", str(root), "--output", str(work / "qa.yaml")], root)
                # Prove generation works with resources available solely within this Engine ZIP.
                for output, script, opts in [
                    ("markdown", "generate_markdown.py", ["--mode", "working"]),
                    ("confluence", "generate_confluence.py", ["--mode", "working"]),
                ]:
                    target = work / output
                    cmd = [str(root / "scripts" / script), "--project-root", str(sample),
                           "--output-dir", str(target), *opts]
                    if run("generate_" + output, cmd, root):
                        before = tree_digest(target)
                        if not list(target.rglob("*")) or not run("regenerate_" + output, cmd, root):
                            errors.append(f"{output}: regeneration failed or output missing")
                        elif before != tree_digest(target):
                            errors.append(f"{output}: output is not deterministic")
                        else:
                            stages.append({"name": "determinism_" + output, "status": "PASS"})
                run("generate_derived_views",
                    [str(root / "scripts/generate_derived_views.py"),
                     "--project-root", str(sample),
                     "--catalog", str(root / "derived-views/views.yaml"),
                     "--output-dir", str(work / "derived")], root)
                run("migration_plan",
                    [str(root / "scripts/migrate_v1_to_v2.py"), "--source", str(sample),
                     "--mode", "plan", "--report", str(work / "migration-plan.yaml")], root)
                if run("migration_apply",
                       [str(root / "scripts/migrate_v1_to_v2.py"), "--source", str(sample),
                        "--mode", "apply", "--output", str(work / "migrated")], root):
                    run("migrated_project_validation",
                        [str(root / "scripts/validate_project.py"),
                         "--project-root", str(work / "migrated"),
                         "--repo-root", str(root), "--no-generated"], root)
                if shutil.which("pandoc") and (shutil.which("libreoffice") or shutil.which("soffice")):
                    if run("document_export",
                           [str(root / "scripts/export_documents.py"),
                            "--project-root", str(sample), "--mode", "working",
                            "--output-dir", str(work / "documents"),
                            "--basename", "ea-engine-selftest"], root):
                        if not list((work / "documents").glob("*.pdf")) or not list(
                                (work / "documents").glob("*.docx")):
                            errors.append("document_export produced no PDF/DOCX")
                else:
                    stages.append({"name": "document_export", "status": "BLOCKED",
                                   "reason": "pandoc and libreoffice not available in host"})
    report = {"engine_id": data.get("engine_id"), "version": data.get("version"),
              "files_checked": len(files), "scripts_checked": len(scripts),
              "stages": stages,
              "status": "FAIL" if errors else "PASS", "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
