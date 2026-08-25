import json, subprocess, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]

def test_catalog_valid_and_noncanonical():
    schema=json.loads((ROOT/'schemas/derived-view.schema.json').read_text())
    data=yaml.safe_load((ROOT/'derived-views/views.yaml').read_text())
    errs=list(Draft202012Validator(schema).iter_errors(data))
    assert not errs, [e.message for e in errs]
    assert data['source_of_truth'] is False
    assert len(data['views']) == 7
    assert all(v['source_of_truth'] is False for v in data['views'])

def test_expected_standard_views_exist():
    data=yaml.safe_load((ROOT/'derived-views/views.yaml').read_text())
    ids={v['id'] for v in data['views']}
    assert {'capability-service-platform','platform-service-capability','product-it-support','product-service-platform','platform-dependencies','shared-realization','product-coverage'} <= ids

def test_generator_is_deterministic_on_empty_reference_model(tmp_path):
    out1=tmp_path/'a'; out2=tmp_path/'b'
    cmd=[sys.executable,str(ROOT/'scripts/generate_derived_views.py'),'--project-root',str(ROOT)]
    subprocess.run(cmd+['--output-dir',str(out1)],check=True,capture_output=True,text=True)
    subprocess.run(cmd+['--output-dir',str(out2)],check=True,capture_output=True,text=True)
    a={p.name:p.read_bytes() for p in out1.glob('*.yaml')}; b={p.name:p.read_bytes() for p in out2.glob('*.yaml')}
    assert a == b and len(a)==7
    for raw in a.values():
        d=yaml.safe_load(raw); assert d['source_of_truth'] is False; assert d['rows']==[]

def test_market_semantics_are_preserved_in_product_views():
    data=yaml.safe_load((ROOT/'derived-views/views.yaml').read_text())
    by={v['id']:v for v in data['views']}
    assert 'inte' in by['product-it-support']['presentation_semantics']['epistemic_note'].lower()
    assert 'actual state' in by['product-service-platform']['presentation_semantics']['epistemic_note'].lower()

def test_generator_traverses_relations(tmp_path):
    project=tmp_path/'project'; (project/'model').mkdir(parents=True); (project/'derived-views').mkdir()
    (project/'derived-views/views.yaml').write_bytes((ROOT/'derived-views/views.yaml').read_bytes())
    def dump(name, typ, objs):
        (project/'model'/name).write_text(yaml.safe_dump({'schema_version':'1.0','object_type':typ,'objects':objs},sort_keys=False,allow_unicode=True))
    dump('products.yaml','product',[{'id':'PRD-001','name':'Writer'}])
    dump('it-support.yaml','it_support',[{'id':'ITS-001','name':'Ordbehandling'}])
    dump('platform-services.yaml','platform_service',[]); dump('platforms.yaml','platform',[]); dump('capabilities.yaml','capability',[])
    (project/'model/relations.yaml').write_text(yaml.safe_dump({'schema_version':'1.0','relations':[{'id':'REL-001','type':'can_realize','source_id':'PRD-001','target_id':'ITS-001'}]},sort_keys=False))
    out=tmp_path/'out'
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_derived_views.py'),'--project-root',str(project),'--output-dir',str(out)],check=True,capture_output=True,text=True)
    data=yaml.safe_load((out/'product-it-support.yaml').read_text())
    assert data['rows']==[{'product.id':'PRD-001','product.name':'Writer','product.object_type':'product','it_support.id':'ITS-001','it_support.name':'Ordbehandling','it_support.object_type':'it_support'}]
