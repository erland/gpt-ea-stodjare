from __future__ import annotations
import json, subprocess, sys, tempfile, shutil, hashlib
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'scripts/resolve_quality_rules.py'
VALIDATOR=ROOT/'scripts/validate_project.py'


def run_quality(project:Path):
    cp=subprocess.run([sys.executable,str(SCRIPT),'--project-root',str(project),'--repo-root',str(ROOT)],text=True,capture_output=True)
    assert cp.returncode==0, cp.stdout+cp.stderr
    return yaml.safe_load(cp.stdout)


def test_default_native_qa_uses_standard_model():
    q=run_quality(ROOT)
    assert q['qa_resolution']['mode']=='native_v2_default'
    assert 'product' in q['qa_resolution']['active_object_types']
    assert 'can_realize' in q['qa_resolution']['active_relation_types']


def test_project_metamodel_filters_disabled_layers():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)
        shutil.copy(ROOT/'examples/project-metamodel/minimal.yaml',p/'project-metamodel.yaml')
        q=run_quality(p)
        assert q['qa_resolution']['mode']=='native_v2_project'
        assert set(q['qa_resolution']['active_object_types'])=={'capability','it_support','platform_service','platform'}
        assert 'driver' not in q['object_quality']['object_type_rules']
        assert 'driver' not in q['model_quality']['coverage_profiles']['strategy_to_capability']['expected_layers']


def test_active_extension_contributes_qa_and_custom_type():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)
        shutil.copy(ROOT/'examples/extensions/project-metamodel.yaml',p/'project-metamodel.yaml')
        q=run_quality(p)
        assert 'ownership_domain' in q['qa_resolution']['active_object_types']
        assert 'stewarded_by' in q['qa_resolution']['active_relation_types']
        assert [r['id'] for r in q['extension_quality_rules']]==['EXT-OWN-001']
        assert 'ownership_domain' in q['object_quality']['common_rules'][0]['applies_to']


def test_extension_qa_disappears_when_extension_disabled():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td); data=yaml.safe_load((ROOT/'examples/extensions/project-metamodel.yaml').read_text())
        data['project_metamodel']['extensions'][0]['enabled']=False
        (p/'project-metamodel.yaml').write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False))
        q=run_quality(p)
        assert q['extension_quality_rules']==[]
        assert 'ownership_domain' not in q['qa_resolution']['active_object_types']


def test_legacy_uses_frozen_profile():
    q=run_quality(ROOT/'examples/minimal-model')
    assert q['qa_resolution']['mode']=='legacy_v1'
    assert 'product' not in q['qa_resolution']['active_object_types']
    assert 'provided_by' not in q['qa_resolution']['active_relation_types']


def _rehash_manifest(project:Path):
    mp=project/'project-manifest.json'; m=json.loads(mp.read_text())
    kept=[]
    for row in m['files']:
        f=project/row['path']
        if not f.is_file():
            if row.get('required'): continue
            kept.append(row); continue
        row['sha256']=hashlib.sha256(f.read_bytes()).hexdigest(); kept.append(row)
    m['files']=kept; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')


def test_validator_does_not_require_disabled_standard_object_files():
    # Convert a copy of the reference project to a native project subset with empty relations.
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'project'; shutil.copytree(ROOT,p,ignore=shutil.ignore_patterns('.git','.pytest_cache','__pycache__','docs/generated','build'))
        pm=yaml.safe_load((ROOT/'examples/project-metamodel/minimal.yaml').read_text())
        (p/'project-metamodel.yaml').write_text(yaml.safe_dump(pm,allow_unicode=True,sort_keys=False))
        # Remove disabled standard files; these must not be reported as gaps.
        disabled={'drivers.yaml','goals.yaml','principles.yaml','products.yaml','standards.yaml','solution-patterns.yaml','reference-architectures.yaml'}
        for f in disabled:
            (p/'model'/f).unlink(missing_ok=True)
        # Keep the active relation set structurally empty to isolate file applicability.
        (p/'model/relations.yaml').write_text("schema_version: '1.0'\nrelations: []\n")
        m=json.loads((p/'project-manifest.json').read_text()); m['model']['metamodel_version']='2.0'; (p/'project-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
        _rehash_manifest(p)
        cp=subprocess.run([sys.executable,str(VALIDATOR),'--project-root',str(p),'--repo-root',str(ROOT),'--no-generated','--json'],text=True,capture_output=True)
        payload=json.loads(cp.stdout)
        assert not any(x['code']=='STR-MODEL-001' and any(f in (x.get('path') or '') for f in disabled) for x in payload['errors'])
