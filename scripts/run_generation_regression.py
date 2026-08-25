#!/usr/bin/env python3
"""Run all script-style document generation regression checks."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
    'tests/generation/test_generate_markdown.py',
    'tests/generation/test_generate_confluence.py',
    'tests/generation/test_export_documents.py',
    'tests/generation/test_metamodel_presentation_generation_v2.py',
]
for rel in SCRIPTS:
    print(f'== {rel} ==', flush=True)
    subprocess.run([sys.executable, str(ROOT/rel)], cwd=ROOT, check=True)
print(f'OK: {len(SCRIPTS)} generatorregressioner godkända.')
