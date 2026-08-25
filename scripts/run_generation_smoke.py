#!/usr/bin/env python3
"""Fast mandatory smoke test for all four document generator families."""
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'examples/minimal-model'

def run(args):
    subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

with tempfile.TemporaryDirectory(prefix='ea-stodjare-generator-smoke-') as td:
    td=Path(td); md=td/'markdown'; cf=td/'confluence'; doc=td/'document'
    run([ROOT/'scripts/generate_markdown.py','--project-root',PROJECT,'--mode','published','--output-dir',md])
    run([ROOT/'scripts/generate_confluence.py','--project-root',PROJECT,'--mode','published','--output-dir',cf])
    run([ROOT/'scripts/export_documents.py','--project-root',PROJECT,'--mode','published','--output-dir',doc,'--basename','ea-smoke'])
    assert (md/'generation-manifest.json').is_file()
    assert (cf/'generation-manifest.json').is_file()
    assert json.loads((md/'generation-manifest.json').read_text())['catalogs']
    assert json.loads((cf/'generation-manifest.json').read_text())['catalogs']
    assert (doc/'ea-smoke.docx').stat().st_size>0
    assert (doc/'ea-smoke.pdf').stat().st_size>0
print('OK: Markdown, Confluence, DOCX och PDF generator-smoke godkänd.')
