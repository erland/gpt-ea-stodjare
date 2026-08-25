#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

CASES=[
 ('simple_native_v2','tests/compatibility/test_project_metamodel_format.py::test_minimal_can_disable_unused_standard_types'),
 ('project_extension','tests/extensions/test_extension_mechanism.py::test_resolver_merges_object_relation_enum_qa_and_presentation'),
 ('research_model_proposal','tests/scenarios/test_research_model_proposal_v2.py::test_research_model_proposal_keeps_external_and_organizational_claims_separate'),
 ('legacy_v1_edit','tests/compatibility/test_legacy_edit_continuity.py::test_legacy_v1_can_be_edited_without_migration'),
 ('v1_to_v2_migration','tests/compatibility/test_minimal_v1_migration_e2e.py::test_minimal_v1_to_v2_end_to_end_semantic_equivalence'),
]

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',default='.'); ap.add_argument('--report',default='compatibility/reports/workflow-conformance-baseline.json'); args=ap.parse_args()
    root=Path(args.project_root).resolve(); rows=[]; ok=True
    for name,node in CASES:
        p=subprocess.run([sys.executable,'-m','pytest','-q',node],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        passed=p.returncode==0; ok &= passed
        rows.append({'id':name,'status':'passed' if passed else 'failed','test_node':node,'output':p.stdout[-2000:]})
    report={'format':'ea-stodjare-workflow-conformance','version':'1.0','evidence_level':'deterministic_workflow_e2e_not_llm_runtime','passed':sum(r['status']=='passed' for r in rows),'total':len(rows),'cases':rows}
    out=root/args.report; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
