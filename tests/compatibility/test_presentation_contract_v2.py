import json, subprocess, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from presentation_contract import load_contract, object_display, field_label, relation_label, navigation_sections


def test_contract_schema_and_noncanonical():
    data=yaml.safe_load((ROOT/'presentation/presentation-contract.yaml').read_text())
    schema=json.loads((ROOT/'schemas/presentation-contract.schema.json').read_text())
    errs=list(Draft202012Validator(schema).iter_errors(data))
    assert not errs, [e.message for e in errs]
    assert data['source_of_truth'] is False
    assert data['object_display']['default_pattern']=='{name} ({id})'


def test_contextual_capability_boundary_labels():
    c=load_contract(ROOT)
    assert field_label(c,'capability','in_scope',{'capability_type':'it'})=='Stödjer'
    assert field_label(c,'capability','in_scope',{'capability_type':'business'})=='Omfattar'
    assert field_label(c,'capability','out_of_scope',{})=='Omfattar inte'


def test_relation_labels_and_object_display():
    c=load_contract(ROOT)
    assert relation_label(c,'provided_by','forward')=='Tillhandahålls av'
    assert relation_label(c,'provided_by','reverse')=='Tillhandahåller'
    assert object_display(c,{'type':'platform','name':'Containerplattform','id':'PLT-001'})=='Containerplattform (PLT-001)'


def test_navigation_sections_reference_derived_views_and_preserve_epistemics():
    c=load_contract(ROOT)
    views=yaml.safe_load((ROOT/'derived-views/views.yaml').read_text())
    ids={v['id'] for v in views['views']}
    all_sections=[s for sections in c['navigation_sections'].values() for s in sections]
    assert all(s['derived_view'] in ids and s['source_of_truth'] is False for s in all_sections)
    prod=navigation_sections(c,'product')
    assert any('inte' in (s.get('epistemic_note') or '').lower() for s in prod)


def test_validator_checks_contract():
    r=subprocess.run([sys.executable,str(ROOT/'scripts/validate_project.py'),'--project-root',str(ROOT),'--no-generated'],capture_output=True,text=True)
    assert r.returncode==0, r.stdout+r.stderr
    assert '0 fel' in r.stdout
