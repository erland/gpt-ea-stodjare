#!/usr/bin/env python3
"""Regression gate: every packaged Skill must import in isolation.

Run after the canonical GPT Byggaren distribution build, not on source-only files.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RUNTIMES = {
    "plugin": "skills/",
    "claude-skills": "skills/",
    "opencode": ".opencode/skills/",
    "chat": "assistant/skills/",
}
SKILLS = ("modeling-and-research", "project-lifecycle", "quality-and-publication")


def probe(script: Path) -> str | None:
    code = ("import runpy,sys;"
            "sys.path.insert(0,sys.argv[1]);"
            "runpy.run_path(sys.argv[2],run_name='__ea_import_probe__')")
    result = subprocess.run(
        [sys.executable, "-c", code, str(script.parent), str(script)],
        capture_output=True, text=True, timeout=30, check=False, cwd=script.parent
    )
    return result.stderr[-600:] if result.returncode else None


def audit(archive: Path, skill_prefix: str, known_modules: set[str]) -> tuple[int, list[str]]:
    errors: list[str] = []
    checked = 0
    with zipfile.ZipFile(archive) as zf:
        if zf.testzip():
            return 0, [f"{archive.name}: corrupt ZIP"]
        entries = set(zf.namelist())
        with tempfile.TemporaryDirectory(prefix="ea-skill-audit-") as temporary:
            tmp = Path(temporary)
            for skill in SKILLS:
                prefix = f"{skill_prefix}{skill}/"
                candidates = sorted(p for p in entries
                                    if p.startswith(prefix + "scripts/") and p.endswith(".py"))
                if not candidates:
                    errors.append(f"{archive.name}: no scripts for {skill}")
                    continue
                for name in candidates:
                    data = zf.read(name)
                    try:
                        parsed = ast.parse(data.decode("utf-8"), filename=name)
                    except (UnicodeError, SyntaxError) as exc:
                        errors.append(f"{name}: {exc}")
                        continue
                    imported: set[str] = set()
                    for node in ast.walk(parsed):
                        if isinstance(node, ast.Import):
                            imported.update(item.name.split(".")[0] for item in node.names)
                        elif isinstance(node, ast.ImportFrom) and node.module:
                            imported.add(node.module.split(".")[0])
                    available = {Path(p).stem for p in candidates}
                    for module in sorted((imported & known_modules) - available):
                        errors.append(f"{name}: missing isolated script dependency {module}.py")

                    target = tmp / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                # Write all files before importing anything, to catch real runtime imports.
                for name in candidates:
                    script = tmp / name
                    if not script.exists():
                        continue
                    error = probe(script)
                    checked += 1
                    if error:
                        errors.append(f"{name}: import failed: {error}")
    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path("."))
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    root = args.project_root.resolve()
    dist = root / "dist"
    cfg_scripts = {p.stem for p in (root / "scripts").glob("*.py")}
    errors: list[str] = []
    checked = 0

    for runtime, prefix in RUNTIMES.items():
        archive = dist / f"ea-stodjare-{runtime}-{args.version}.zip"
        if not archive.is_file():
            errors.append(f"Missing distribution {archive.name}")
            continue
        count, issues = audit(archive, prefix, cfg_scripts)
        checked += count
        errors.extend(issues)

    engine = dist / f"ea-stodjare-engine-{args.version}.zip"
    if not engine.is_file():
        errors.append(f"Missing engine distribution {engine.name}")
    else:
        with zipfile.ZipFile(engine) as zf:
            if zf.testzip():
                errors.append(f"Corrupt engine {engine.name}")
            elif "engine-package.json" not in zf.namelist():
                errors.append("Missing engine-package.json")
            else:
                with tempfile.TemporaryDirectory(prefix="ea-runtime-engine-") as tmp:
                    zf.extractall(tmp)
                    test = Path(tmp) / "scripts/selftest_ea_engine.py"
                    if not test.is_file():
                        errors.append("Engine selftest file missing")
                    else:
                        result = subprocess.run([sys.executable, str(test)],
                                                cwd=tmp, capture_output=True, text=True,
                                                timeout=120, check=False)
                        if result.returncode:
                            errors.append(f"Engine selftest failed: {result.stdout[-700:]} {result.stderr[-700:]}")

    report = {"status": "PASS" if not errors else "FAIL",
              "isolated_script_imports": checked, "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
