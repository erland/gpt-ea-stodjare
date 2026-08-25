from __future__ import annotations
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]
VALIDATOR=ROOT/'scripts/validate_project.py'
HELPER=ROOT/'scripts/change_control.py'

def rehash(project:Path):
    mp=project/'project-manifest.json'; m=json.loads(mp.read_text())
    rows=[]
    listed={r['path'] for r in m['files']}
    # Add newly created files in a copied fixture if absent from its manifest.
    role_map={'.json':'schema','.yaml':'governance','.md':'documentation_source','.py':'support'}
    for f in project.rglob('*'):
        if not f.is_file() or '.git' in f.parts or '__pycache__' in f.parts or '.pytest_cache' in f.parts or f.name=='project-manifest.json': continue
        rel=f.relative_to(project).as_posix()
        if rel not in listed:
            m['files'].append({'path':rel,'role':role_map.get(f.suffix,'support'),'required':False,'sha256':''})
    for r in m['files']:
        f=project/r['path']
        if f.is_file():
            r['sha256']=hashlib.sha256(f.read_bytes()).hexdigest(); rows.append(r)
        elif not r.get('required'): rows.append(r)
    m['files']=sorted(rows,key=lambda x:x['path']); mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

def run_validator(project:Path):
    cp=subprocess.run([sys.executable,str(VALIDATOR),'--project-root',str(project),'--repo-root',str(ROOT),'--no-generated','--json'],text=True,capture_output=True)
    return cp, json.loads(cp.stdout)

def test_governance_files_validate_against_schemas():
    pairs=[('governance/change-control.yaml','schemas/change-control.schema.json'),('governance/retired-ids.yaml','schemas/retired-id-registry.schema.json'),('governance/model-changelog.yaml','schemas/change-log.schema.json'),('governance/metamodel-changelog.yaml','schemas/change-log.schema.json')]
    for data_path,schema_path in pairs:
        data=yaml.safe_load((ROOT/data_path).read_text()); schema=json.loads((ROOT/schema_path).read_text())
        assert list(Draft202012Validator(schema).iter_errors(data))==[]

def test_helper_classifies_metamodel_change_to_separate_log():
    cp=subprocess.run([sys.executable,str(HELPER),'--project-root',str(ROOT),'--change-class','metamodel_change','--json'],text=True,capture_output=True)
    assert cp.returncode==0, cp.stderr
    p=json.loads(cp.stdout); assert p['scope']=='metamodel'; assert p['target_changelog']=='governance/metamodel-changelog.yaml'

def test_frozen_baseline_requires_reopen_for_model_and_metamodel_change():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td); shutil.copytree(ROOT/'governance',p/'governance')
        d=yaml.safe_load((p/'governance/change-control.yaml').read_text()); d['change_control']['baseline']['freeze_status']='frozen'
        (p/'governance/change-control.yaml').write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False))
        for cls in ['controlled_model_change','breaking_model_change','metamodel_change']:
            cp=subprocess.run([sys.executable,str(HELPER),'--project-root',str(p),'--change-class',cls,'--json'],text=True,capture_output=True)
            assert json.loads(cp.stdout)['requires_reopen_now'] is True
        for cls in ['editorial','evidence_update']:
            cp=subprocess.run([sys.executable,str(HELPER),'--project-root',str(p),'--change-class',cls,'--json'],text=True,capture_output=True)
            assert json.loads(cp.stdout)['requires_reopen_now'] is False

def test_retired_id_cannot_be_reused_in_active_model():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'project'; shutil.copytree(ROOT,p,ignore=shutil.ignore_patterns('.git','.pytest_cache','__pycache__','docs/generated','build','exports'))
        # Derived-view IDs are active governed IDs even when the reference model has no object instances.
        views=yaml.safe_load((p/'derived-views/views.yaml').read_text())
        active=views['views'][0]['id']
        reg=yaml.safe_load((p/'governance/retired-ids.yaml').read_text()); reg['retired_ids']=[{'id':active,'entity_kind':'derived_view','retired_at_revision':44,'replacement_id':None,'reason':'test','change_ref':'CHG-MODEL-999'}]
        (p/'governance/retired-ids.yaml').write_text(yaml.safe_dump(reg,allow_unicode=True,sort_keys=False)); rehash(p)
        cp,payload=run_validator(p)
        assert cp.returncode!=0
        assert any(e['code']=='STR-GOV-008' for e in payload['errors'])

def test_metamodel_change_is_rejected_in_model_log():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'project'; shutil.copytree(ROOT,p,ignore=shutil.ignore_patterns('.git','.pytest_cache','__pycache__','docs/generated','build','exports'))
        log=yaml.safe_load((p/'governance/model-changelog.yaml').read_text()); log['changes']=[{'id':'CHG-MODEL-999','revision':44,'change_class':'metamodel_change','summary':'fel logg','status':'applied'}]
        (p/'governance/model-changelog.yaml').write_text(yaml.safe_dump(log,allow_unicode=True,sort_keys=False)); rehash(p)
        cp,payload=run_validator(p)
        assert cp.returncode!=0
        assert any(e['code']=='STR-GOV-013' for e in payload['errors'])

def test_legacy_project_does_not_require_v2_governance_files():
    cp,payload=run_validator(ROOT/'examples/minimal-model')
    assert not any(e['code'].startswith('STR-GOV-') for e in payload['errors'])
