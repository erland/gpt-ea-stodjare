#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator


def main() -> int:
    ap=argparse.ArgumentParser(description='Sammanställ fullständigt körda och manuellt bedömda runtime-evals till poängsättningsformat.')
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--output', default=None)
    args=ap.parse_args(); root=Path(args.project_root).resolve(); run=(root/args.run_dir).resolve()
    manifest=json.loads((run/'run-manifest.json').read_text(encoding='utf-8'))
    suite=yaml.safe_load((root/'evals/eval-suite.yaml').read_text(encoding='utf-8'))
    suite_by={e['id']:yaml.safe_load((root/'evals'/e['file']).read_text(encoding='utf-8')) for e in suite['cases']}
    result_cases=[]; problems=[]
    for row in manifest['cases']:
        cid=row['id']; response=(run/row['response_file']).read_text(encoding='utf-8').strip()
        if not response: problems.append(f'{cid}: response saknas')
        assessment=yaml.safe_load((run/row['assessment_file']).read_text(encoding='utf-8')) or {}
        expected_ids={c['id'] for c in suite_by[cid]['grading_criteria']}; criteria=assessment.get('criteria') or {}
        if set(criteria)!=expected_ids: problems.append(f'{cid}: kriterie-ID:n matchar inte evaldefinitionen')
        incomplete=[k for k in expected_ids if criteria.get(k) not in (True,False)]
        if incomplete: problems.append(f'{cid}: ej bedömda kriterier: {", ".join(sorted(incomplete))}')
        result_cases.append({'id':cid,'response':response,'criteria':criteria,'critical_failures':assessment.get('critical_failures') or [],'notes':assessment.get('notes','')})
    if problems:
        raise SystemExit('Runtime-run är inte komplett:\n- '+'\n- '.join(problems))
    payload={'format':'ea-stodjare-runtime-eval-result','version':'1.0','target':manifest['target']+f" [fingerprint {manifest['target_fingerprint']['sha256']}]",'executed_at':datetime.now(timezone.utc).isoformat(),'cases':result_cases}
    schema=json.loads((root/'schemas/runtime-eval-result.schema.json').read_text(encoding='utf-8'))
    errors=list(Draft202012Validator(schema).iter_errors(payload))
    if errors: raise SystemExit('Internt schemafel: '+'; '.join(e.message for e in errors))
    out=Path(args.output) if args.output else run/'runtime-eval-results.json'; out=out if out.is_absolute() else root/out
    out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'OK: {len(result_cases)} runtime-evalresultat sammanställda till {out}')
    return 0
if __name__=='__main__': raise SystemExit(main())
