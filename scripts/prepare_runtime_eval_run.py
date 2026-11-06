#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import yaml


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fingerprint_target(root: Path) -> dict:
    files=[root/'custom-gpt/instructions.md'] + sorted((root/'custom-gpt/knowledge').glob('*.md'))
    rows=[]
    h=hashlib.sha256()
    for p in files:
        rel=p.relative_to(root).as_posix(); digest=sha256_bytes(p.read_bytes())
        rows.append({'path':rel,'sha256':digest})
        h.update(rel.encode()); h.update(b'\0'); h.update(digest.encode()); h.update(b'\n')
    return {'sha256':h.hexdigest(),'files':rows}


def main() -> int:
    ap=argparse.ArgumentParser(description='Förbered en reproducerbar manuell runtime-evalkörning mot faktisk GPT-runtime.')
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--target', required=True, help='Namn/version på den faktiska runtime som ska testas.')
    ap.add_argument('--run-dir', default='evals/runtime/runs/current')
    ap.add_argument('--run-id', default=None)
    args=ap.parse_args()
    root=Path(args.project_root).resolve(); run=root/args.run_dir
    suite=yaml.safe_load((root/'evals/eval-suite.yaml').read_text(encoding='utf-8'))
    run_id=args.run_id or datetime.now(timezone.utc).strftime('runtime-%Y%m%dT%H%M%SZ')
    (run/'prompts').mkdir(parents=True,exist_ok=True); (run/'responses').mkdir(parents=True,exist_ok=True); (run/'assessments').mkdir(parents=True,exist_ok=True)
    fp=fingerprint_target(root); manifest={'format':'ea-stodjare-runtime-eval-run','version':'1.0','run_id':run_id,'target':args.target,'suite_version':suite['version'],'created_at':datetime.now(timezone.utc).isoformat(),'target_fingerprint':fp,'cases':[]}
    for entry in suite['cases']:
        case=yaml.safe_load((root/'evals'/entry['file']).read_text(encoding='utf-8')); cid=case['id']
        prompt=(f"# {cid} – {case['title']}\n\n"
                "Kör följande prompt i en **ny separat konversation** mot den runtime som anges i run-manifestet. "
                "Lägg inte till evalkriterierna i GPT-konversationen. Spara hela assistentsvaret oförändrat i motsvarande response-fil.\n\n"
                "## Prompt\n\n" + case['prompt'].strip() + "\n")
        (run/'prompts'/f'{cid}.md').write_text(prompt,encoding='utf-8')
        response=run/'responses'/f'{cid}.md'
        if not response.exists(): response.write_text('',encoding='utf-8')
        assessment={'id':cid,'criteria':{c['id']:None for c in case['grading_criteria']},'critical_failures':[],'notes':''}
        (run/'assessments'/f'{cid}.yaml').write_text(yaml.safe_dump(assessment,allow_unicode=True,sort_keys=False),encoding='utf-8')
        manifest['cases'].append({'id':cid,'title':case['title'],'blocking':bool(entry['blocking']),'prompt_file':f'prompts/{cid}.md','response_file':f'responses/{cid}.md','assessment_file':f'assessments/{cid}.yaml'})
    (run/'run-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'OK: runtime-eval run {run_id} förberedd med {len(manifest["cases"])} separata fall i {run}')
    print(f'Target fingerprint: {fp["sha256"]}')
    return 0
if __name__=='__main__': raise SystemExit(main())
