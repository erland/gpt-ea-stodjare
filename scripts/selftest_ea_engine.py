#!/usr/bin/env python3
"""Self-test for the standalone EA Stödjare runtime Engine ZIP.

Does not mutate user projects and does not run a migration.
"""
from __future__ import annotations

import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    manifest_path = root / "engine-package.json"
    if not manifest_path.is_file():
        print("ENGINE SELFTEST FAILED: engine-package.json missing", file=sys.stderr)
        return 1
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("engine_id") != "ea-stodjare":
        print("ENGINE SELFTEST FAILED: incorrect engine_id", file=sys.stderr)
        return 1

    files = data.get("files") or {}
    errors: list[str] = []
    for name, expected in files.items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Unsafe path: {name}")
            continue
        path = root / relative
        if not path.is_file():
            errors.append(f"Missing: {name}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f"SHA-256 mismatch: {name}")

    script_names = sorted(name for name in files if name.startswith("scripts/") and name.endswith(".py")
                          and name != "scripts/selftest_ea_engine.py")
    for name in script_names:
        script = root / name
        if not script.is_file():
            continue
        probe = (
            "import runpy,sys;"
            "sys.path.insert(0,sys.argv[1]);"
            "runpy.run_path(sys.argv[2],run_name='__ea_import_probe__')"
        )
        result = subprocess.run(
            [sys.executable, "-c", probe, str(script.parent), str(script)],
            text=True, capture_output=True, check=False, timeout=30,
            cwd=root,
        )
        if result.returncode:
            errors.append(f"Import probe failed: {name}: {result.stderr[-700:]}")

    report = {"engine_id": data.get("engine_id"), "version": data.get("version"),
              "files_checked": len(files), "scripts_checked": len(script_names),
              "status": "PASS" if not errors else "FAIL", "errors": errors}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
