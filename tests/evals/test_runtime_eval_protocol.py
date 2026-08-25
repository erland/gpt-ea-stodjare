from pathlib import Path
import json, subprocess, sys, tempfile
import yaml
ROOT=Path(__file__).resolve().parents[2]

def test_runtime_eval_status_is_honest_and_packet_complete():
    status=yaml.safe_load((ROOT/'evals/runtime/runtime-eval-status.yaml').read_text(encoding='utf-8'))
    assert status['status']=='not_executed_external_runtime_required'
    assert status['runtime_cases_executed']==0
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'packet.json'
        subprocess.run([sys.executable,str(ROOT/'scripts/prepare_runtime_eval_packet.py'),'--project-root',str(ROOT),'--output',str(out)],check=True)
        packet=json.loads(out.read_text(encoding='utf-8'))
        assert len(packet['cases'])==29
        assert len({c['id'] for c in packet['cases']})==29

def test_release_text_does_not_claim_runtime_eval_pass():
    texts=[(ROOT/'PROJECT_STATUS.md').read_text(encoding='utf-8')]
    texts += [(ROOT/'docs/final-release-review-v2.0.0.md').read_text(encoding='utf-8')]
    joined='\n'.join(texts).lower()
    assert '29/29 runtime' not in joined
