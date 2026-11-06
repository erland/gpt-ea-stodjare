#!/usr/bin/env python3
"""Inspect EA Stödjare v2 change-control state."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml

CLASSES = {"editorial","evidence_update","controlled_model_change","breaking_model_change","metamodel_change"}

def load(root: Path):
    p=root/'governance/change-control.yaml'
    if not p.is_file(): raise SystemExit(f'Change-control saknas: {p}')
    return yaml.safe_load(p.read_text(encoding='utf-8'))['change_control']

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root', type=Path, default=Path.cwd())
    ap.add_argument('--change-class', choices=sorted(CLASSES))
    ap.add_argument('--json', action='store_true')
    a=ap.parse_args(); cc=load(a.project_root.resolve()); b=cc['baseline']
    out={'baseline':b,'change_control_enabled':cc['enabled']}
    if a.change_class:
        c=cc['change_classes'][a.change_class]; frozen=cc['policies']['frozen_baseline']
        out['change_class']=a.change_class; out['scope']=c['scope']; out['requires_evidence']=bool(c.get('requires_evidence'))
        out['requires_approval']=bool(c.get('requires_approval')); out['requires_new_baseline']=bool(c.get('requires_new_baseline'))
        out['requires_reopen_now']=b['freeze_status']=='frozen' and a.change_class in frozen['requires_reopen']
        out['target_changelog']='governance/metamodel-changelog.yaml' if c['scope']=='metamodel' else 'governance/model-changelog.yaml'
    if a.json: print(json.dumps(out,ensure_ascii=False,indent=2))
    else:
        print(f"Baseline: {b['id']}@{b['version']} ({b['freeze_status']})")
        if a.change_class: print(f"{a.change_class}: {out['scope']}, reopen={out['requires_reopen_now']}, log={out['target_changelog']}")
    return 0
if __name__=='__main__': raise SystemExit(main())
