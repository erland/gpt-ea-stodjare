from pathlib import Path
import sys, yaml
ROOT=Path(__file__).resolve().parents[2]
SCENARIO=ROOT/'examples/product-analysis-platform-service'
sys.path.insert(0,str(ROOT/'scripts'))
from validate_project import ValidationContext, validate_model, validate_information_layers

def load(path): return yaml.safe_load(path.read_text(encoding='utf-8'))

def test_platform_service_product_scenario_is_valid_v2_model():
    manifest={'model':{'root':'model','metamodel_version':'2.0'},'information_layers':{'conceptual':'model','market_reference':'market-reference','actual_state':'actual-state'}}
    ctx=ValidationContext(); validate_model(SCENARIO,ROOT,manifest,ctx); validate_information_layers(SCENARIO,ROOT,manifest,ctx)
    assert not ctx.errors, '\n'.join(x.format() for x in ctx.errors)

def test_platform_service_is_realization_neutral_and_products_use_all_roles():
    pls=load(SCENARIO/'model/platform-services.yaml')['objects'][0]
    assert pls['id']=='PLS-261' and pls['realization_pattern']=='mixed'
    assert 'product' not in pls
    rels=load(SCENARIO/'model/relations.yaml')['relations']
    can={r['source']:r for r in rels if r['type']=='can_realize'}
    assert {k:v['realization_role'] for k,v in can.items()}=={'PRD-261':'primary','PRD-262':'partial','PRD-263':'supporting'}
    assert all(r['target']=='PLS-261' for r in can.values())

def test_market_products_do_not_become_actual_state():
    market=load(SCENARIO/'market-reference/assertions.yaml')['assertions']
    actual=load(SCENARIO/'actual-state/assertions.yaml')['assertions']
    assert {x['subject'] for x in market}=={'PRD-261','PRD-262','PRD-263'}
    assert actual==[]
    expected=load(SCENARIO/'expected-analysis.yaml')
    assert 'can_realize_does_not_imply_actual_use' in expected['guards']
