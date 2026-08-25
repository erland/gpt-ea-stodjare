from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[2]

def load(rel):
    return yaml.safe_load((ROOT/rel).read_text(encoding='utf-8'))

def test_six_boundary_first_workflows_exist_and_are_non_mutating():
    data=load('schemas/modeling-review-workflows.yaml')['review_workflows']
    assert data['source_of_truth'] is False
    expected={'boundary_review','decomposition_review','merge_review','singleton_sanity_review','product_stress_test','composition_sanity_review'}
    assert set(data['workflows']) == expected
    assert 'reviews_are_diagnostic_not_mutating' in data['principles']

def test_workflows_are_linked_to_qa():
    data=load('schemas/modeling-review-workflows.yaml')['review_workflows']['workflows']
    qa=load('schemas/model-quality-rules.yaml')['quality_rules']['rules']['boundary_first_modeling']
    ids={r['id'] for r in qa}
    for wf in data.values():
        assert wf['qa_links']
        assert set(wf['qa_links']).issubset(ids | {'QM-DUP-001','QM-DUP-002','QM-CON-002','QO-PLT-006','QO-PLT-007','QO-PLT-008','QO-PRD-004','QO-PRD-005'})

def test_singleton_and_product_stress_semantics_are_preserved():
    w=load('schemas/modeling-review-workflows.yaml')['review_workflows']['workflows']
    assert w['singleton_sanity_review']['applies_to']==['platform']
    assert 'valid_singleton' in w['singleton_sanity_review']['decision_options']
    assert set(w['product_stress_test']['applies_to'])=={'it_support','platform_service','platform'}
    assert w['product_stress_test']['evidence_required_for_change'] is False

def test_legacy_v1_snapshot_has_no_step19_rules():
    legacy=(ROOT/'compatibility/ea-stodjare-v1/schemas/object-types.yaml').read_text(encoding='utf-8')
    assert 'QM-BND-' not in legacy
    assert 'product_stress_test' not in legacy
