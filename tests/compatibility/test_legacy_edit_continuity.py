from __future__ import annotations
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]

def sha(path: Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def test_legacy_v1_can_be_edited_without_migration():
    with tempfile.TemporaryDirectory(prefix='ea-v1-edit-') as td:
        target=Path(td)/'project'; shutil.copytree(ROOT/'examples/minimal-model',target)
        model=target/'model/it-support.yaml'; data=yaml.safe_load(model.read_text(encoding='utf-8'))
        data['objects'][0]['description'] += ' Redaktionellt legacy-test.'
        model.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False),encoding='utf-8')
        manifest_path=target/'project-manifest.json'; manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        for row in manifest['files']:
            if row['path']=='model/it-support.yaml': row['sha256']=sha(model)
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        proc=subprocess.run([sys.executable,str(ROOT/'scripts/validate_project.py'),'--project-root',str(target),'--repo-root',str(ROOT),'--no-generated'],text=True,capture_output=True)
        assert proc.returncode==0, proc.stdout+proc.stderr
        assert '0 fel' in proc.stdout
