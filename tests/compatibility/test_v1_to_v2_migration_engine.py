import copy, json, subprocess, sys, tempfile
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'examples/minimal-model'
SCRIPT=ROOT/'scripts/migrate_v1_to_v2.py'

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def test_plan_is_deterministic_and_non_destructive():
    before=(SRC/'project-manifest.json').read_bytes()
    a=subprocess.check_output([sys.executable,str(SCRIPT),'--source',str(SRC),'--mode','plan'])
    b=subprocess.check_output([sys.executable,str(SCRIPT),'--source',str(SRC),'--mode','plan'])
    assert a==b
    assert (SRC/'project-manifest.json').read_bytes()==before
    r=yaml.safe_load(a)['migration']
    assert r['status']=='planned' and r['information_preservation']['original_overwritten'] is False
    assert any(x['code']=='MIG-REALIZED-BY' for x in r['issues'])

def test_apply_creates_new_valid_v2_copy_and_preserves_ids():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'migrated'
        subprocess.run([sys.executable,str(SCRIPT),'--source',str(SRC),'--mode','apply','--output',str(out)],check=True,capture_output=True,text=True)
        manifest=json.loads((out/'project-manifest.json').read_text())
        assert manifest['model']['metamodel_version']=='2.0'
        assert manifest['project']['revision']==json.loads((SRC/'project-manifest.json').read_text())['project']['revision']+1
        pm=load(out/'project-metamodel.yaml')['project_metamodel']
        assert pm['base_profile']['id']=='ea-stodjare-v2'
        rels=load(out/'model/relations.yaml')['relations']
        r6=next(x for x in rels if x['id']=='REL-006')
        assert r6['type']=='legacy_realized_by'
        assert next(x for x in rels if x['id']=='REL-011')['type']=='realized_by'
        source_ids={x['id'] for p in (SRC/'model').glob('*.yaml') for x in (load(p).get('objects') or []) if isinstance(x,dict) and x.get('id')}
        target_ids={x['id'] for p in (out/'model').glob('*.yaml') for x in (load(p).get('objects') or []) if isinstance(x,dict) and x.get('id')}
        assert source_ids==target_ids
        report=load(out/'migration/migration-report.yaml')['migration']
        assert report['status']=='applied_with_review_required'

def test_apply_refuses_overwrite():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'exists'; out.mkdir()
        p=subprocess.run([sys.executable,str(SCRIPT),'--source',str(SRC),'--mode','apply','--output',str(out)],capture_output=True,text=True)
        assert p.returncode==2 and 'skrivs inte över' in p.stderr
