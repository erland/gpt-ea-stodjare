from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
def load(rel): return yaml.safe_load((ROOT/rel).read_text(encoding='utf-8'))
def test_v2_capability_fields():
    d=load('schemas/object-types.yaml'); cap=d['object_types']['capability']
    assert d['metamodel']['version']=='2.0-draft'
    assert cap['optional_attributes']==['in_scope','out_of_scope','consumer_scope']
    assert 'scope' not in cap['optional_attributes']
    assert cap['presentation_semantics']['it.in_scope']=='Stödjer'
    assert cap['presentation_semantics']['out_of_scope']=='Omfattar inte'
def test_v1_snapshot_stays_legacy():
    d=load('compatibility/ea-stodjare-v1/schemas/object-types.yaml'); cap=d['object_types']['capability']
    assert 'scope' in cap['optional_attributes']
    assert 'in_scope' not in cap['optional_attributes'] and 'out_of_scope' not in cap['optional_attributes']
def test_migration_is_conservative():
    d=load('compatibility/migration-rules/v1-to-v2-capability-boundary.yaml')['migration_rule_set']
    assert d['automatic_rewrite_default'] is False
    r=next(x for x in d['rules'] if x['id']=='CAP-BND-001')
    assert set(r['target_fields'])=={'in_scope','out_of_scope'}
    assert r['ambiguous_action']=='preserve legacy scope and record migration issue'
