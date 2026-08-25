import json, tempfile
from pathlib import Path
import yaml
from scripts.detect_project_profile import detect

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'compatibility/reference-projects/rev80/migration-baseline.yaml'
RES=ROOT/'compatibility/reference-projects/rev80/migration-verification-result.yaml'

def load(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))

def test_rev80_step24_baseline_and_result_are_consistent():
    b=load(BASE)['expected']; r=load(RES)['verification']
    assert r['status']=='passed_extended_legacy_migration'
    assert r['counts']['capabilities']==b['capabilities']==13
    assert r['counts']['platform_services']==b['platform_services']==92
    assert r['counts']['platforms']==b['platforms']==35
    assert r['counts']['relations']==b['relations']==385
    assert r['counts']['products']==b['market_products']==295
    assert r['counts']['supporting_yaml']==b['supporting_yaml']==92
    assert r['counts']['provided_by_converted']==b['provided_by_after_migration']==92
    assert r['counts']['relation_roles_applied']==b['relation_roles']==55
    assert r['governance']['baseline_id']==b['baseline_id']
    assert r['governance']['freeze_status']==b['freeze_status']=='frozen'
    assert r['checks']['information_loss_hidden'] is False
    assert all(v for k,v in r['checks'].items() if k != 'information_loss_hidden')

def test_flat_rev80_manifest_is_detected_as_extended_legacy():
    sig=load(ROOT/'compatibility/reference-projects/rev80/metamodel.yaml')['detection_signature']
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'it-formagemodell-del3-rev80'; p.mkdir()
        (p/'project-manifest.json').write_text(json.dumps({'schema_version':'1.0','revision':80,'root_directory':'it-formagemodell-del3-rev80','file_count':245,'files':[]}),encoding='utf-8')
        for rel in sig['required_paths']:
            f=p/rel; f.parent.mkdir(parents=True,exist_ok=True); f.write_text('{}\n',encoding='utf-8')
        result=detect(p,ROOT)
        assert result['classification']=='extended_legacy'
        assert result['confidence']=='high'
        assert 'rev80-reconstruction' in result['selected_profile']
