from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]

def test_current_version_is_final_v2():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='2.0.0'

def test_workflow_conformance_report_is_5_of_5():
    report=json.loads((ROOT/'compatibility/reports/workflow-conformance-baseline.json').read_text(encoding='utf-8'))
    assert report['format']=='ea-stodjare-workflow-conformance'
    assert report['evidence_level']=='deterministic_workflow_e2e_not_llm_runtime'
    assert report['passed']==5 and report['total']==5
