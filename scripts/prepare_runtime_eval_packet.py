#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml


def main() -> int:
    ap=argparse.ArgumentParser(description='Skapa runtime-evalpaket för faktisk Custom GPT/portable-chat-körning.')
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--output', default='evals/runtime/runtime-eval-packet.json')
    args=ap.parse_args()
    root=Path(args.project_root).resolve()
    suite=yaml.safe_load((root/'evals/eval-suite.yaml').read_text(encoding='utf-8'))
    cases=[]
    for item in suite['cases']:
        data=yaml.safe_load((root/'evals'/item['file']).read_text(encoding='utf-8'))
        cases.append({
            'id': data['id'], 'title': data['title'], 'blocking': bool(item['blocking']),
            'prompt': data['prompt'], 'grading_criteria': data['grading_criteria'],
            'critical_failures': data['critical_failures'], 'expected_behaviors': data['expected_behaviors'],
            'forbidden_behaviors': data['forbidden_behaviors']
        })
    out=root/args.output; out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({'format':'ea-stodjare-runtime-eval-packet','version':'1.0','suite_version':suite['version'],'cases':cases}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'OK: {len(cases)} runtime-evalfall exporterade till {out}')
    return 0
if __name__=='__main__': raise SystemExit(main())
