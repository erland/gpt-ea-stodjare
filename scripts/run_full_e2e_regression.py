#!/usr/bin/env python3
"""Run the twelve permanent end-to-end regression scenarios for EA Stödjare v2."""
from __future__ import annotations
import argparse, json, subprocess, sys, time
from pathlib import Path

def run(name, cmd, root):
    t=time.monotonic(); p=subprocess.run(cmd,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return {'id':name,'status':'passed' if p.returncode==0 else 'failed','returncode':p.returncode,'duration_seconds':round(time.monotonic()-t,3),'command':cmd,'stdout_tail':p.stdout.strip().splitlines()[-12:],'stderr_tail':p.stderr.strip().splitlines()[-12:]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',type=Path,default=Path.cwd()); ap.add_argument('--report-file',type=Path)
    a=ap.parse_args(); root=a.project_root.resolve(); py=sys.executable
    scenarios=[
      ('simple_v2_project',[py,'-m','pytest','-q','tests/compatibility/test_project_metamodel_format.py']),
      ('advanced_v2_extensions',[py,'-m','pytest','-q','tests/extensions/test_extension_mechanism.py','tests/extensions/test_optional_rev80_extensions.py']),
      ('open_v1_without_migration',[py,'-m','pytest','-q','tests/compatibility/test_project_profile_detection.py','tests/compatibility/test_v1_profile.py']),
      ('continue_editing_v1',[py,'-m','pytest','-q','tests/compatibility/test_legacy_edit_continuity.py']),
      ('migrate_v1',[py,'-m','pytest','-q','tests/compatibility/test_minimal_v1_migration_e2e.py']),
      ('open_rev80',[py,'-m','pytest','-q','tests/compatibility/test_rev80_reconstruction.py']),
      ('migrate_rev80',[py,'-m','pytest','-q','tests/compatibility/test_rev80_migration_step24.py']),
      ('product_analysis_it_support',[py,'-m','pytest','-q','tests/compatibility/test_it_support_product_analysis_scenario.py']),
      ('product_analysis_platform_service',[py,'-m','pytest','-q','tests/compatibility/test_platform_service_product_analysis_scenario.py']),
      ('research_model_proposal',[py,'-m','pytest','-q','tests/scenarios/test_research_model_proposal_v2.py','tests/scenarios/test_stress_scenarios.py']),
      ('derived_views',[py,'-m','pytest','-q','tests/compatibility/test_derived_views_v2.py']),
      ('export',[py,'scripts/run_generation_smoke.py']),
    ]
    report={'schema_version':'1.0','gate':'v2-full-end-to-end','required_scenarios':[x[0] for x in scenarios],'scenarios':[],'valid':False}
    def persist():
        if a.report_file:
            path=a.report_file if a.report_file.is_absolute() else root/a.report_file
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,cmd in scenarios:
        r=run(name,cmd,root); report['scenarios'].append(r); persist()
        if r['status']=='failed':
            report['failed_scenario']=name; persist(); break
    report['valid']=len(report['scenarios'])==len(scenarios) and all(x['status']=='passed' for x in report['scenarios'])
    report['summary']={'passed':sum(x['status']=='passed' for x in report['scenarios']),'failed':sum(x['status']=='failed' for x in report['scenarios']),'total_required':len(scenarios)}
    text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if a.report_file:
        path=a.report_file if a.report_file.is_absolute() else root/a.report_file; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8')
    print(text,end=''); return 0 if report['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
