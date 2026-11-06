#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator


def main() -> int:
    ap=argparse.ArgumentParser(description='Poängsätt redan exekvererade runtime-evals.')
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--results', required=True)
    ap.add_argument('--report', default='evals/runtime/runtime-eval-score.json')
    args=ap.parse_args(); root=Path(args.project_root).resolve()
    results=json.loads(Path(args.results).read_text(encoding='utf-8'))
    schema=json.loads((root/'schemas/runtime-eval-result.schema.json').read_text(encoding='utf-8'))
    errs=list(Draft202012Validator(schema).iter_errors(results))
    if errs: raise SystemExit('Ogiltig runtime-resultatfil: '+'; '.join(e.message for e in errs))
    suite=yaml.safe_load((root/'evals/eval-suite.yaml').read_text(encoding='utf-8'))
    by_id={c['id']:c for c in results['cases']}
    total=earned=0.0; blocking_fail=[]; rows=[]
    for entry in suite['cases']:
        case=yaml.safe_load((root/'evals'/entry['file']).read_text(encoding='utf-8'))
        r=by_id.get(case['id'])
        if r is None:
            rows.append({'id':case['id'],'status':'NOT_EXECUTED','score_percent':0});
            if entry['blocking']: blocking_fail.append(case['id'])
            total += sum(c['weight'] for c in case['grading_criteria']); continue
        case_total=sum(c['weight'] for c in case['grading_criteria']); total += case_total
        case_earned=sum(c['weight'] for c in case['grading_criteria'] if r['criteria'].get(c['id']) is True)
        earned += case_earned
        critical=bool(r['critical_failures'])
        pct=100*case_earned/case_total if case_total else 0
        status='FAIL' if critical or pct < 65 else ('PASS_WITH_WARNINGS' if pct < 80 else 'PASS')
        if entry['blocking'] and status!='PASS': blocking_fail.append(case['id'])
        rows.append({'id':case['id'],'status':status,'score_percent':round(pct,2),'critical_failures':r['critical_failures']})
    weighted=100*earned/total if total else 0
    release_pass=(not blocking_fail and weighted >= suite['release_gate']['minimum_weighted_score_percent'])
    report={'format':'ea-stodjare-runtime-eval-score','version':'1.0','target':results['target'],'executed_at':results['executed_at'],'weighted_score_percent':round(weighted,2),'blocking_failures':blocking_fail,'release_gate_passed':release_pass,'cases':rows}
    out=root/args.report; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if release_pass else 2
if __name__=='__main__': raise SystemExit(main())
