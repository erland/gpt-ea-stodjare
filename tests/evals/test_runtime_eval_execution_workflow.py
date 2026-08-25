from pathlib import Path
import json, subprocess, sys, tempfile, yaml
ROOT=Path(__file__).resolve().parents[2]

def test_prepare_run_is_complete_and_fingerprinted():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'
        subprocess.run([sys.executable,str(ROOT/'scripts/prepare_runtime_eval_run.py'),'--project-root',str(ROOT),'--target','test-target','--run-dir',str(run)],check=True)
        m=json.loads((run/'run-manifest.json').read_text(encoding='utf-8'))
        assert m['target']=='test-target'
        assert len(m['cases'])==29
        assert len(m['target_fingerprint']['sha256'])==64
        assert any(x['path']=='custom-gpt/instructions.md' for x in m['target_fingerprint']['files'])
        for c in m['cases']:
            assert (run/c['prompt_file']).is_file()
            assert (run/c['response_file']).is_file()
            a=yaml.safe_load((run/c['assessment_file']).read_text(encoding='utf-8'))
            assert a['id']==c['id'] and all(v is None for v in a['criteria'].values())

def test_assembler_refuses_incomplete_run():
    with tempfile.TemporaryDirectory() as td:
        run=Path(td)/'run'
        subprocess.run([sys.executable,str(ROOT/'scripts/prepare_runtime_eval_run.py'),'--project-root',str(ROOT),'--target','test-target','--run-dir',str(run)],check=True)
        cp=subprocess.run([sys.executable,str(ROOT/'scripts/assemble_runtime_eval_results.py'),'--project-root',str(ROOT),'--run-dir',str(run)],text=True,capture_output=True)
        assert cp.returncode!=0
        assert 'response saknas' in (cp.stderr+cp.stdout)
